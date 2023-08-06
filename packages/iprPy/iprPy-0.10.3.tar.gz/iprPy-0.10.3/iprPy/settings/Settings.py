# Standard Python libraries
from copy import deepcopy
from pathlib import Path
import json

import potentials

# iprPy imports
from ..tools import screen_input

class Settings(potentials.Settings):
    """
    Class for handling saved settings.
    """
    
    @property
    def runner_log_directory(self):
        """pathlib.Path : Path to the directory where runner logs are saved to."""

        # Check runner_log_directory value
        if 'iprPy_runner_log_directory' in self.__content:
            return Path(self.__content['iprPy_runner_log_directory'])
        else:
            return Path(self.directory, 'runner-logs')

    @property
    def databases(self):
        """dict: The pre-defined database settings organized by name"""
        if 'iprPy_database' not in self.__content:
            self.__content['iprPy_database'] = {}
        return deepcopy(self.__content['iprPy_database'])

    @property
    def list_databases(self):
        """list: The names of the pre-defined database names"""
        return list(self.databases.keys())

    @property
    def run_directories(self):
        """dict: The pre-defined run_directory paths organized by name"""
        if 'iprPy_run_directory' not in self.__content:
            self.__content['iprPy_run_directory'] = {}
        return deepcopy(self.__content['iprPy_run_directory'])

    @property
    def list_run_directories(self):
        """list: The names of the pre-defined database names"""
        return list(self.run_directories.keys())
    
    def set_runner_log_directory(self, path=None):
        """
        Sets the runner log directory to a different location.

        Parameters
        ----------
        path : str or Path
            The path to the new runner log directory where log files generated
            by runners are saved to.  If not given, will be asked for in a
            prompt.
        """
        # Check if a different directory has already been set
        if 'iprPy_runner_log_directory' in self.__content:
            print(f'Runner log directory already set to {self.runner_log_directory}')
            option = screen_input('Overwrite? (yes or no):')
            if option.lower() in ['yes', 'y']:
                pass
            elif option.lower() in ['no', 'n']: 
                return None
            else: 
                raise ValueError('Invalid choice')
        
        # Ask for path if not given
        if path is None:
            path = screen_input("Enter the path for the new runner log directory:")
        self.__content['iprPy_runner_log_directory'] = Path(path).resolve().as_posix()

        # Save changes
        self.save()
        
    def unset_runner_log_directory(self):
        """
        Resets the saved runner log directory information back to the default
        <Settings.directory>/runner-logs/ location.
        """
        
        # Check if library_directory has been set
        if 'iprPy_runner_log_directory' not in self.__content:
            print(f'Runner log directory not set: still using {self.runner_log_directory}')
        
        else:
            print(f'Remove runner log directory {self.runner_log_directory} and reset to {Path(self.directory, "runner-logs")}?')
            test = screen_input('Delete settings? (must type yes):').lower()
            if test == 'yes':
                del self.__content['iprPy_runner_log_directory']

            # Save changes
            self.save()

    def set_database(self, name=None, style=None, host=None, **kwargs):
        """
        Allows for database information to be defined in the settings file. Screen
        prompts will be given to allow any necessary database parameters to be
        entered.

        Parameters
        ----------
        name : str, optional
            The name to assign to the database. If not given, the user will be
            prompted to enter one.
        style : str, optional
            The database style associated with the database. If not given, the
            user will be prompted to enter one.
        host : str, optional
            The database host (directory path or url) where the database is
            located. If not given, the user will be prompted to enter one.
        **kwargs : any, optional
            Any other database style-specific parameter settings required to
            properly access the database.
        """
        # Ask for name if not given
        if name is None:
            name = screen_input('Enter a name for the database:')

        # Load database if it exists
        if name in self.list_databases:
            
           # Ask if existing database should be overwritten
            print(f'Database {name} already defined.')
            option = screen_input('Overwrite? (yes or no):')
            if option.lower() in ['yes', 'y']:
                pass
            elif option.lower() in ['no', 'n']: 
                return None
            else: 
                raise ValueError('Invalid choice')
                 
        # Create database entry
        self.__content['iprPy_database'][name] = entry = {} 
            
        # Ask for style if not given
        if style is None: 
            style = screen_input("Enter the database's style:")
        entry['style'] = style

        #Ask for host if not given
        if host is None:
            host = screen_input("Enter the database's host:")
        entry['host'] = str(host)

        # Ask for additional kwargs if not given
        if len(kwargs) == 0:
            print('Enter any other database parameters as key, value')
            print('Exit by leaving key blank')
            while True:
                key = screen_input('key:')
                if key == '': 
                    break
                kwargs[key] = screen_input('value:')
        for key, value in kwargs.items():
            entry[key] = value

        # Save changes
        self.save()
    
    def unset_database(self, name=None):
        """
        Deletes the settings for a pre-defined database from the settings file.

        Parameters
        ----------
        name : str
            The name assigned to a pre-defined database.
        """
        database_names = self.list_databases
                  
        # Ask for name if not given
        if name is None:
            
            if len(database_names) > 0:
                print('Select a database:')
                for i, database in enumerate(database_names):
                    print(i+1, database)
                choice = screen_input(':')
                try:
                    choice = int(choice)
                except:
                    name = choice
                else:
                    name = database_names[choice-1]
            else:
                print('No databases currently set')
                return None

        # Verify listed name exists 
        try:
            i = database_names.index(name)
        except:
            raise ValueError(f'Database {name} not found')

        print(f'Database {name} found')
        test = screen_input('Delete settings? (must type yes):').lower()
        if test == 'yes':
            del(self.__content['iprPy_database'][name])
            self.save()
                  
    def set_run_directory(self, name=None, path=None):
        """
        Allows for run_directory information to be defined in the settings file.

        Parameters
        ----------
        name : str, optional
            The name to assign to the run_directory.  If not given, the user will
            be prompted to enter one.
        path : str, optional
            The directory path for the run_directory.  If not given, the user will
            be prompted to enter one.
        """
                  
        # Ask for name if not given
        if name is None:
            name = screen_input('Enter a name for the run_directory:')

        # Load run_directory if it exists
        if name in self.list_run_directories:
            
            # Ask if existing run_directory should be overwritten     
            print(f'run_directory {name} already defined.')
            option = screen_input('Overwrite? (yes or no):')
            if option.lower() in ['yes', 'y']:
                pass
            elif option.lower() in ['no', 'n']: 
                return None
            else: 
                raise ValueError('Invalid choice')
        
        # Ask for path if not given
        if path is None:
            path = screen_input("Enter the run_directory's path:")
        self.__content['iprPy_run_directory'][name] = Path(path).resolve().as_posix()

        self.save()

    def unset_run_directory(self, name=None):
        """
        Deletes the settings for a pre-defined run_directory from the settings
        file.

        Parameters
        ----------
        name : str
            The name assigned to a pre-defined run_directory.
        """
        run_directory_names = self.list_run_directories

        # Ask for name if not given
        if name is None:
            if len(run_directory_names) > 0:
                print('Select a run_directory:')
                for i, run_directory in enumerate(run_directory_names):
                    print(i+1, run_directory)
                choice = screen_input(':')
                try:
                    choice = int(choice)
                except:
                    name = choice
                else:
                    name = run_directory_names[choice-1]
            else:
                print('No run_directories currently set')
                return None

        # Verify listed name exists 
        try:
            i = run_directory_names.index(name)
        except:
            raise ValueError(f'Run directory {name} not found')

        print(f'Run directory {name} found')
        test = screen_input('Delete settings? (must type yes):').lower()
        if test == 'yes':
            del(self.__content['iprPy_run_directory'][name])                  
            self.save()