import argparse
import json
import logging
import os
import sys
from datetime import datetime

from . import config
from .classes.nodes import ChannelNode
from .commands import uploadchannel_wrapper
from .exceptions import InvalidUsageException
from .exceptions import raise_for_invalid_channel
from .managers.progress import Status
from .utils.jsontrees import build_tree_from_json
from .utils.jsontrees import get_channel_node_from_json
from .utils.jsontrees import read_tree_from_json
from .utils.linecook import build_ricecooker_json_tree
from .utils.linecook import FolderExistsAction
from .utils.metadata_provider import CsvMetadataProvider
from .utils.metadata_provider import DEFAULT_CHANNEL_INFO_FILENAME
from .utils.metadata_provider import DEFAULT_CONTENT_INFO_FILENAME
from .utils.metadata_provider import DEFAULT_EXERCISE_QUESTIONS_INFO_FILENAME
from .utils.metadata_provider import DEFAULT_EXERCISES_INFO_FILENAME
from .utils.tokens import get_content_curation_token





# SUSHI CHEF BASE CLASS
################################################################################

class SushiChef(object):
    """
    This is the base class that all content integration scripts should subclass.
    Sushi chef scripts call the `main` method as the entry point, which in turn
    calls the `run` method to do the work (see `uploadchannel` in `commands.py`).
    """
    CHEF_RUN_DATA = config.CHEF_DATA_DEFAULT  # loaded from chefdata/chef_data.json
    TREES_DATA_DIR = config.TREES_DATA_DIR    # tree archives and JsonTreeChef inputs


    def __init__(self, *args, **kwargs):
        """
        The SushiChef initialization concerns maintly parsing command line args.
        Overrride this method in your sushi chef class to add custom arguments.
        """

        # ARGPARSE SETUP
        # We don't want to add argparse help if subclass has an __init__ method
        subclasses = self.__class__.__mro__[:-2]     # all subclasses after this
        if any(['__init__' in c.__dict__.keys() for c in subclasses]):
            add_parser_help = False    # assume subclass' __init__ will add help
        else:
            add_parser_help = True
        parser = argparse.ArgumentParser(
            description="Chef script for uploading content to Kolibri Studio.",
            add_help=add_parser_help,
        )
        self.arg_parser = parser  # save as class attr. for subclasses to extend
        # ARGS
        parser.add_argument('command', nargs='?', default='uploadchannel', help='Desired action: dryrun or uploadchannel (default).')
        parser.add_argument('--token', default='#',                   help='Studio API Access Token (specify wither the token value or the path of a file that contains the token).')
        parser.add_argument('-u', '--update', action='store_true',    help='Force file re-download (skip .ricecookerfilecache/).')
        parser.add_argument('--debug', action='store_true',           help='Print extra debugging infomation.')
        parser.add_argument('-v', '--verbose', action='store_true', default=True, help='Verbose mode (default).')
        parser.add_argument('--warn', action='store_true',            help='Print errors and warnings.')
        parser.add_argument('--quiet', action='store_true',           help='Print only errors.')
        parser.add_argument('--compress', action='store_true',        help='Compress videos using ffmpeg -crf=32 -b:a 32k mono.')
        parser.add_argument('--thumbnails', action='store_true',      help='Automatically generate thumbnails for content nodes.')
        parser.add_argument('--download-attempts',type=int,default=3, help='Maximum number of times to retry downloading files.')
        parser.add_argument('--resume', action='store_true',          help='Resume chef session from a specified step.')
        allsteps = [step.name.upper() for step in Status]
        parser.add_argument('--step',choices=allsteps,default='LAST', help='Step to resume progress from (use with the --resume).')
        parser.add_argument('--prompt', action='store_true',          help='Prompt user to open the channel after the chef run.')
        parser.add_argument('--deploy', dest='stage', action='store_false',
                                                                      help='Immediately deploy changes to channel\'s main tree. This operation will overwrite the previous channel content. Use only during development.')
        parser.add_argument('--publish', action='store_true',         help='Publish newly uploaded version of the channel.')
        parser.add_argument('--sample', type=int, metavar='SIZE',     help='Upload a sample of SIZE nodes from the channel.')
        parser.add_argument('--reset', dest="reset_deprecated", action='store_true',
                                                                      help='(deprecated) Restarting the chef run is the default.')
        parser.add_argument('--stage', dest='stage_deprecated', action='store_true',
                                                                      help='(deprecated) Stage updated content for review. Uploading a staging tree is now the default behavior. Use --deploy to upload to the main tree.')

        # [OPTIONS] --- extra key=value options are supported, but do not appear in help

        self.load_chef_data()


    def parse_args_and_options(self):
        """
        Parses all known command line args and also additional key=value options.
        NOTE: this should be the only place cli args are parsed in order to have
        a single consistent interface for all chef scripts.

        Args: None, but implicitly depends on `self.arg_parser` and `sys.argv`
        Returns:
          tuple (`args`, `options`)
            args (dict): chef command line arguments
            options (dict): extra key=value options given on command line
        """
        args_namespace, options_list = self.arg_parser.parse_known_args()
        args = args_namespace.__dict__

        # Handle case when command is not specified but key=value options are
        allcommands = [
            'uploadchannel',  # Whole pipeline: pre_run > run > [deploy,publish]
            'dryrun',         # Do pre_run and run but do not upload to Studio
        ]
        command_arg = args['command']
        if command_arg not in allcommands and '=' in command_arg:
            # a key=value options pair was incorrectly recognized as the command
            args['command'] = 'uploadchannel'
            options_list.append(command_arg)  # put command_arg where it belongs

        # Print CLI deprecation warnings info
        if args['stage_deprecated']:
            config.LOGGER.warning('DEPRECATION WARNING: --stage is now the default bevavior. The --stage flag has been deprecated and will be removed in ricecooker 1.0.')
        if args['reset_deprecated']:
            config.LOGGER.warning(
                'DEPRECATION WARNING: --reset is now the default bevavior. The --reset flag has been deprecated and will be removed in ricecooker 1.0.')
        if args['publish'] and args['stage']:
            raise InvalidUsageException('The --publish argument must be used together with --deploy argument.')
        logging_args = [key for key in ['quiet', 'warn', 'debug'] if args[key]]
        if len(logging_args) > 1:
            raise InvalidUsageException('Agruments --quiet, --warn, and --debug cannot be used together.')

        if args['command'] == 'uploadchannel':
            # Make sure token is provided. There are four ways to specify:
            #  1. --token=path to token-containing file
            #  2. --token=140fefe...1f3
            # when --token is not given on the command line, it default to # and
            #  3. we look for environment variable STUDIO_TOKEN
            #  4. else prompt user
            # If ALL of these fail, this call will raise and chef run will stop.
            args['token'] = get_content_curation_token(args['token'])

        # Parse additional keyword arguments from `options_list`
        options = {}
        for preoption in options_list:
            try:
                option_key, option_value = preoption.split('=')
                options.update({option_key.strip(): option_value.strip()})
            except IndexError:
                msg = "Invalid option '{0}': use [key]=[value] format (no whitespace)".format(preoption)
                raise InvalidUsageException(msg)

        return args, options


    def config_logger(self, args, options):
        """
        Set up stream (stderr), local file logging (logs/yyyy-mm-dd__HHMM.log).
        This method is called as soon as we parse args so we can apply the
        user-preferred logging level settings.
        """
        # Set desired logging level based on command line arguments
        level = logging.INFO
        if args['debug']:
            level = logging.DEBUG
        elif args['warn']:
            level = logging.WARNING
        elif args['quiet']:
            level = logging.ERROR

        # 2. File handler (logs/yyyy-mm-dd__HHMM.log)
        try:
            # FIXME: This code assumes we run chefs from the chef's root directory.
            # We probably want to have chefs set a root directory for files like this.
            if not os.path.exists("logs"):
                os.makedirs("logs")
            logfile_main = datetime.now().strftime("%Y-%m-%d__%H%M") + ".log"
            logfile_error = datetime.now().strftime("%Y-%m-%d__%H%M") + ".err.log"
            main_log = os.path.join("logs", logfile_main)
            error_log = os.path.join("logs", logfile_error)

            config.setup_logging(level=level, main_log=main_log, error_log=error_log)

        except Exception as e:
            config.LOGGER.warning('Unable to setup file logging due to %s' % e)


    def get_channel(self, **kwargs):
        """
        This method creates an empty `ChannelNode` object based on info from the
        chef class' `channel_info` attribute. A subclass can ovveride this method
        in cases where channel metadata is dynamic and depends on `kwargs`.
        Args:
            kwargs (dict): additional keyword arguments given to `uploadchannel`
        Returns: an empty `ChannelNode` that contains all the channel metadata
        """
        if hasattr(self, 'channel_info'):
            # Make sure we're not using the template id values in `channel_info`
            template_domains = ['<yourdomain.org>']
            using_template_domain = self.channel_info['CHANNEL_SOURCE_DOMAIN'] in template_domains
            if using_template_domain:
                config.LOGGER.error("Template source domain detected. Please change CHANNEL_SOURCE_DOMAIN before running this chef.")

            template_ids = ['<unique id for the channel>', '<yourid>']
            using_template_source_id = self.channel_info['CHANNEL_SOURCE_ID'] in template_ids
            if using_template_source_id:
                config.LOGGER.error("Template channel source ID detected. Please change CHANNEL_SOURCE_ID before running this chef.")

            if using_template_domain or using_template_source_id:
               sys.exit(1)

            # If a sublass has an `channel_info` attribute (dict) it doesn't need
            # to define a `get_channel` method and instead rely on this code:
            channel = ChannelNode(
                source_domain=self.channel_info['CHANNEL_SOURCE_DOMAIN'],
                source_id=self.channel_info['CHANNEL_SOURCE_ID'],
                title=self.channel_info['CHANNEL_TITLE'],
                tagline=self.channel_info.get('CHANNEL_TAGLINE'),
                thumbnail=self.channel_info.get('CHANNEL_THUMBNAIL'),
                language=self.channel_info.get('CHANNEL_LANGUAGE'),
                description=self.channel_info.get('CHANNEL_DESCRIPTION'),
            )
            return channel
        else:
            raise NotImplementedError('Subclass must define get_channel method or have a channel_info (dict) attribute.')


    def construct_channel(self, **kwargs):
        """
        This should be overriden by the chef script's construct_channel method.
        Args:
            kwargs (dict): additional keyword arguments given to `uploadchannel`
        Returns: a `ChannelNode` object representing the populated topic tree
        """
        raise NotImplementedError('Chef subclass must implement this method')


    def load_chef_data(self):
        if os.path.exists(config.DATA_PATH):
            self.CHEF_RUN_DATA = json.load(open(config.DATA_PATH))


    def save_channel_tree_as_json(self, channel):
        filename = os.path.join(self.TREES_DATA_DIR, '{}.json'.format(self.CHEF_RUN_DATA['current_run']))
        os.makedirs(self.TREES_DATA_DIR, exist_ok=True)
        json.dump(channel.get_json_tree(), open(filename, 'w'), indent=2)
        self.CHEF_RUN_DATA['tree_archives']['previous'] = self.CHEF_RUN_DATA['tree_archives']['current']
        self.CHEF_RUN_DATA['tree_archives']['current'] = filename.replace(os.getcwd() + '/', '')
        self.save_chef_data()


    def save_chef_data(self):
        json.dump(self.CHEF_RUN_DATA, open(config.DATA_PATH, 'w'), indent=2)


    def pre_run(self, args, options):
        """
        This function is called before the Chef's `run` mehod is called.
        By default this function does nothing, but subclass can use this hook to
        run prerequisite tasks.
        Args:
            args (dict): chef command line arguments
            options (dict): extra key=value options given on command line
        """
        pass


    def run(self, args, options):
        """
        This function calls uploadchannel which performs all the run steps:
        Args:
            args (dict): chef command line arguments
            options (dict): additional key=value options given on command line
        """
        args_copy = args.copy()
        args_copy['token'] = args_copy['token'][0:6] + '...'
        config.LOGGER.info('In SushiChef.run method. args=' + str(args_copy) + ' options=' + str(options))

        run_id = datetime.now().strftime("%Y-%m-%d__%H%M")
        self.CHEF_RUN_DATA['current_run'] = run_id
        self.CHEF_RUN_DATA['runs'].append({'id': run_id})

        # TODO(Kevin): move self.download_content() call here
        self.pre_run(args, options)
        uploadchannel_wrapper(self, args, options)


    def main(self):
        """
        Main entry point that content integration scripts should call.
        """
        args, options = self.parse_args_and_options()
        self.config_logger(args, options)
        self.run(args, options)




# JSON TREE CHEF
################################################################################

class JsonTreeChef(SushiChef):
    """
    This sushi chef loads the data from a channel from a ricecooker json tree file
    which conatins the json representation of a full ricecooker node tree.
    For example the content hierarchy with two levels of subfolders and a PDF
    content node looks like this::

        {
          "title": "Open Stax",
          "source_domain": "openstax.org",
          "source_id": "open-stax",
          "language": "en",
          "children": [
            {
              "kind": "topic",
              "title": "Humanities",
              "children": [
                {
                  "kind": "topic",
                  "title": "U.S. History",
                  "children": [
                    {
                      "kind": "document",
                      "source_id": "Open Stax/Humanities/U.S. History/Student Handbook.pdf",
                      "title": "Student Handbook",
                      "author": "P. Scott Corbett, Volker Janssen, ..."",
                      "license": {
                        "license_id": "CC BY"
                      },
                      "files": [
                        {
                          "file_type": "document",
                          "path": "content/open_stax_zip/Open Stax/Humanities/U.S. History/Student Handbook.pdf"
                        }
                      ]
                    }]}]}]}

    Each object in the json tree correponds to a TopicNode, a ContentNode that
    contains a Files or an Exercise that contains Question.
    """
    RICECOOKER_JSON_TREE = 'ricecooker_json_tree.json'

    def pre_run(self, args, options):
        """
        This function is called before `run` to create the json tree file.
        """
        raise NotImplementedError('JsonTreeChef subclass must implement the `pre_run` method.')

    def get_json_tree_path(self, *args, **kwargs):
        """
        Return path to ricecooker json tree file. Override this method to use
        a custom filename, e.g., for channel with multiple languages.
        """
        json_tree_path = os.path.join(self.TREES_DATA_DIR, self.RICECOOKER_JSON_TREE)
        return json_tree_path

    def get_channel(self, **kwargs):
        # Load channel info from json_tree
        json_tree_path = self.get_json_tree_path(**kwargs)
        json_tree = read_tree_from_json(json_tree_path)
        channel = get_channel_node_from_json(json_tree)
        return channel

    def construct_channel(self, **kwargs):
        """
        Build the channel tree by adding TopicNodes and ContentNode children.
        """
        channel = self.get_channel(**kwargs)
        json_tree_path = self.get_json_tree_path(**kwargs)
        json_tree = read_tree_from_json(json_tree_path)
        build_tree_from_json(channel, json_tree['children'])
        raise_for_invalid_channel(channel)
        return channel




# SOUSCHEF LINECOOK
################################################################################

class LineCook(JsonTreeChef):
    """
    This sushi chef uses os.walk to import the content in `channeldir` folder
    `directory structure + CSV metadata files  -->  Kolibri channel`.
    Folders and CSV files can be creaed by hand or by a `souschef` script.
    """
    metadata_provider = None

    def __init__(self, *args, **kwargs):
        super(LineCook, self).__init__(*args, **kwargs)

        # We don't want to add argparse help if subclass has an __init__ method
        subclasses = self.__class__.__mro__[:-5]     # all subclasses after this
        if any(['__init__' in c.__dict__.keys() for c in subclasses]):
            add_parser_help = False    # assume subclass' __init__ will add help
        else:
            add_parser_help = True

        self.arg_parser = argparse.ArgumentParser(
            description="Upload the folder hierarchy to the content workshop.",
            add_help=add_parser_help,
            parents=[self.arg_parser]
        )
        self.arg_parser.add_argument('--channeldir', required=True,
            action=FolderExistsAction,
            help='The directory that corresponds to the root of the channel.')
        self.arg_parser.add_argument('--channelinfo',
            default=DEFAULT_CHANNEL_INFO_FILENAME,
            help='Filename for the channel metadata (assumed to be sibling of channeldir)')
        self.arg_parser.add_argument('--contentinfo',
            default=DEFAULT_CONTENT_INFO_FILENAME,
            help='Filename for content metadata (assumed to be sibling of channeldir)')
        self.arg_parser.add_argument('--exercisesinfo',
            default=DEFAULT_EXERCISES_INFO_FILENAME,
            help='Filename for execises metadata (assumed to be sibling of channeldir)')
        self.arg_parser.add_argument('--questionsinfo',
            default=DEFAULT_EXERCISE_QUESTIONS_INFO_FILENAME,
            help='Filename for execise questions metadata (assumed to be sibling of channeldir)')
        self.arg_parser.add_argument('--generate', action='store_true',
            help='Generate metadata files from directory stucture.')
        self.arg_parser.add_argument('--importstudioid',
            help='Generate CSV metadata from a specified studio_id (e.g. studio_id of main_tree for some channel)')


    def _init_metadata_provider(self, args, options):
        if args['contentinfo'].endswith('.csv'):
            metadata_provider = CsvMetadataProvider(args['channeldir'],
                                                    channelinfo=args['channelinfo'],
                                                    contentinfo=args['contentinfo'],
                                                    exercisesinfo=args['exercisesinfo'],
                                                    questionsinfo=args['questionsinfo'])
        else:
            raise ValueError('Uknown contentinfo file format ' + args['contentinfo'])
        self.metadata_provider = metadata_provider

    def pre_run(self, args, options):
        """
        This function is called before `run` in order to build the json tree.
        """
        if 'generate' in args and args['generate']:
            self.metadata_provider = CsvMetadataProvider(args['channeldir'],
                                                    channelinfo=args['channelinfo'],
                                                    contentinfo=args['contentinfo'],
                                                    exercisesinfo=args['exercisesinfo'],
                                                    questionsinfo=args['questionsinfo'],
                                                    validate_and_cache=False)
            self.metadata_provider.generate_templates(exercise_questions=True)
            self.metadata_provider.generate_contentinfo_from_channeldir(args, options)
            sys.exit(0)

        elif 'importstudioid' in args and args['importstudioid']:
            studio_id = args['importstudioid']
            config.LOGGER.info("Calling with importstudioid... " + studio_id)
            self.metadata_provider = CsvMetadataProvider(args['channeldir'],
                                                    channelinfo=args['channelinfo'],
                                                    contentinfo=args['contentinfo'],
                                                    exercisesinfo=args['exercisesinfo'],
                                                    questionsinfo=args['questionsinfo'],
                                                    validate_and_cache=False)
            self.metadata_provider.generate_templates(exercise_questions=True)
            self.metadata_provider.generate_exercises_from_importstudioid(args, options)
            sys.exit(0)

        if self.metadata_provider is None:
            self._init_metadata_provider(args, options)
        kwargs = {}   # combined dictionary of argparse args and extra options
        kwargs.update(args)
        kwargs.update(options)
        json_tree_path = self.get_json_tree_path(**kwargs)
        build_ricecooker_json_tree(args, options, self.metadata_provider, json_tree_path)
