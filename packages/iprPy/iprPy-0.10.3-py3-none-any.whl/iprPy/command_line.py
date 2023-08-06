#!/usr/bin/env python
# coding: utf-8

# Standard Python libraries
import argparse

# https://github.com/usnistgov/iprPy
from . import (load_database, load_run_directory, load_calculation,
               check_modules, Settings)

def command_line():
    args = command_line_parser()
    command_line_actions(args)

def command_line_actions(args):
    """
    Calls iprPy actions based on the parsed arguments
    """
    # Actions for subcommand build_refs
    if args.action == 'build_refs':
        database = load_database(args.database)
        database.build_refs()
    
    # Actions for subcommand check_records
    elif args.action == 'check_records':
        database = load_database(args.database)
        database.check_records(record_style=args.record_style)
    
    # Actions for subcommand check_modules
    elif args.action == 'check_modules':
        check_modules()
    
    # Actions for subcommand clean_records
    elif args.action == 'clean_records':
        database = load_database(args.database)
        run_directory = load_run_directory(args.run_directory)
        database.clean_records(run_directory=run_directory, record_style=args.record_style)
    
    # Actions for subcommand copy_records
    elif args.action == 'copy_records':
        database1 = load_database(args.database1)
        database2 = load_database(args.database2)
        database1.copy_records(database2, record_style=args.record_style)
    
    # Actions for subcommand destroy_records
    elif args.action == 'destroy_records':
        database = load_database(args.database)
        database.destroy_records(args.record_style)
    
    # Actions for subcommand prepare
    elif args.action == 'prepare':
        database = load_database(args.database)
        run_directory = load_run_directory(args.run_directory)
        calculation = load_calculation(args.calculation)
        database.prepare(run_directory, calculation, input_script=args.input_script)
    
    # Actions for subcommand runner
    elif args.action == 'runner':
        database = load_database(args.database)
        run_directory = load_run_directory(args.run_directory)
        database.runner(run_directory)
    
    # Actions for subcommand set_database
    elif args.action == 'set_database':
        Settings().set_database(args.name)
    
    # Actions for subcommand unset_database
    elif args.action == 'unset_database':
        Settings().unset_database(args.name)
    
    # Actions for list_databases
    elif args.action == 'list_databases':
        for name in Settings().list_databases:
            print(name)

    # Actions for subcommand set_run_directory
    elif args.action == 'set_run_directory':
        Settings().set_run_directory(args.name)
    
    # Actions for subcommand unset_run_directory
    elif args.action == 'unset_run_directory':
        Settings().unset_run_directory(args.name)
    
    # Actions for list_run_directories
    elif args.action == 'list_run_directories':
        for name in Settings().list_run_directories:
            print(name)

    # Actions for directory
    elif args.action == 'directory':
        print(Settings().directory)

    # Actions for set_directory
    elif args.action == 'set_directory':
        Settings().set_directory(args.path)

    # Actions for unset_directory
    elif args.action == 'unset_directory':
        Settings().unset_directory()

    # Actions for library_directory
    elif args.action == 'library_directory':
        print(Settings().library_directory)

    # Actions for set_library_directory
    elif args.action == 'set_library_directory':
        Settings().set_library_directory(args.path)

    # Actions for unset_library_directory
    elif args.action == 'unset_library_directory':
        Settings().unset_library_directory()

    # Actions for runner_log_directory
    elif args.action == 'runner_log_directory':
        print(Settings().runner_log_directory)

    # Actions for set_runner_log_directory
    elif args.action == 'set_runner_log_directory':
        Settings().set_runner_log_directory(args.path)

    # Actions for unset_runner_log_directory
    elif args.action == 'unset_runner_log_directory':
        Settings().unset_runner_log_directory()

    else:
        raise ValueError('Unknown action argument')
    
def command_line_parser():
    """
    Defines the command line parsing logic for the iprPy command line executable.
    """
    parser = argparse.ArgumentParser(description='iprPy high-throughput commands')
    subparsers = parser.add_subparsers(title='actions', dest='action')
    
    # Define subparser for build_refs
    subparser = subparsers.add_parser('build_refs', 
                        help='add library reference records to a database')
    subparser.add_argument('database', nargs='?', default=None, 
                        help='database name')
    
    # Define subparser for check_records
    subparser = subparsers.add_parser('check_records', 
                        help='checks status of a run_directory or database')
    subparser.add_argument('database', nargs='?', default=None,
                        help='database name')
    subparser.add_argument('record_style', nargs='?', default=None,
                        help='optional record style to limit by')
    
    # Define subparser for check_modules
    subparser = subparsers.add_parser('check_modules',
                        help='prints load status of all modules in iprPy')
    
    # Define subparser for clean_records
    subparser = subparsers.add_parser('clean_records',
                        help='resets prepared calculations for running again')
    subparser.add_argument('database', nargs='?', default=None,
                        help='database name')
    subparser.add_argument('run_directory', nargs='?', default=None,
                        help='run_directory name')
    subparser.add_argument('record_style', nargs='?', default=None,
                        help='optional record style')
    
    # Define subparser for copy_records
    subparser = subparsers.add_parser('copy_records',
                        help='copy records of a given style from one database to another')
    subparser.add_argument('database1', nargs='?', default=None,
                        help='database name to copy from')
    subparser.add_argument('database2', nargs='?', default=None,
                        help='database name to copy to')
    subparser.add_argument('record_style', nargs='?', default=None,
                        help='optional record style')
    
    # Define subparser for destroy_records
    subparser = subparsers.add_parser('destroy_records',
                        help='delete all records of a given style from a database')
    subparser.add_argument('database', nargs='?', default=None,
                        help='database name')
    subparser.add_argument('record_style', nargs='?', default=None,
                        help='record style')
    
    # Define subparser for prepare
    subparser = subparsers.add_parser('prepare',
                        help='prepare calculations')
    subparser.add_argument('database',
                        help='database name')
    subparser.add_argument('run_directory',
                        help='run_directory name')
    subparser.add_argument('calculation',
                        help='calculation name')
    subparser.add_argument('input_script',
                        help='input parameter script')
    
    # Define subparser for runner
    subparser = subparsers.add_parser('runner',
                        help='start runner working on prepared calculations')
    subparser.add_argument('database', nargs='?', default=None,
                        help='database name')
    subparser.add_argument('run_directory', nargs='?', default=None,
                        help='run_directory name')
    
    # Define subparser for list_databases
    subparser = subparsers.add_parser('list_databases',
                        help='prints the names of all set databases')

    # Define subparser for set_database
    subparser = subparsers.add_parser('set_database',
                        help='define database access information')
    subparser.add_argument('name', nargs='?', default=None,
                        help='name to assign to the database')
    
    # Define subparser for unset_database
    subparser = subparsers.add_parser('unset_database',
                        help='forget settings for a defined database')
    subparser.add_argument('name', nargs='?', default=None,
                        help='name assigned to the database')
    
    # Define subparser for list_run_directories
    subparser = subparsers.add_parser('list_run_directories',
                        help='prints the names of all set run_directory paths')

    # Define subparser for set_run_directory
    subparser = subparsers.add_parser('set_run_directory',
                        help='define run_directory path')
    subparser.add_argument('name', nargs='?', default=None,
                        help='name to assign to the run_directory')
    
    # Define subparser for unset_run_directory
    subparser = subparsers.add_parser('unset_run_directory',
                        help='forget settings for a defined run_directory')
    subparser.add_argument('name', nargs='?', default=None,
                        help='name assigned to the run_directory')
    
    # Define subparser for directory
    subparser = subparsers.add_parser('directory',
                        help='prints the path where iprPy settings are saved')

    # Define subparser for set_directory
    subparser = subparsers.add_parser('set_directory',
                        help='define directory path where iprPy settings are saved')
    subparser.add_argument('path', nargs='?', default=None,
                        help='path for the directory')
    
    # Define subparser for unset_directory
    subparser = subparsers.add_parser('unset_directory',
                        help="revert to using iprPy's default settings directory path <home>/.iprPy/")

    # Define subparser for library_directory
    subparser = subparsers.add_parser('library_directory',
                        help='prints the path where the iprPy library is located')

    # Define subparser for set_library_directory
    subparser = subparsers.add_parser('set_library_directory',
                        help='define the path where the iprPy library is located')
    subparser.add_argument('path', nargs='?', default=None,
                        help='path for the directory')
    
    # Define subparser for unset_library_directory
    subparser = subparsers.add_parser('unset_library_directory',
                        help="revert to using default location of <directory>/library/")

    # Define subparser for runner_log_directory
    subparser = subparsers.add_parser('runner_log_directory',
                        help='prints the path where runner scripts will save their log files to')

    # Define subparser for set_library_directory
    subparser = subparsers.add_parser('set_library_directory',
                        help='define the path where runner scripts will save their log files to')
    subparser.add_argument('path', nargs='?', default=None,
                        help='path for the directory')
    
    # Define subparser for unset_library_directory
    subparser = subparsers.add_parser('unset_library_directory',
                        help="revert to using default location of <directory>/runner-logs/")

    # Parse command line arguments
    return parser.parse_args()

if __name__ == '__main__':
    command_line()