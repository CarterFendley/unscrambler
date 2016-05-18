import logging
logger = logging.getLogger('dashboard')
log_datefmt = "%H:%M:%S"
log_format = "%(asctime)s:%(msecs)03d %(levelname)-8s: %(name)-20s: %(message)s"

#!/usr/bin/env python3

import optparse
import sys

from database import DataBase

class Scrabbler:
    def __init__(self, options):
        self.database = None
        
        if options.first_run:
            self.database = DataBase(options.database_dir, new=True)
        else:
            self.database = DataBase(options.database_dir)
        
        if options.add_wordlist is not None:
            with open(options.add_wordlist, 'r') as file:
                
                for word in file:
                    word = word.replace("\n", "")
                    print(word)
                    if not self.database.hasWord(word):
                       self.database.addWord(word)
                    
            self.database.close()
            sys.exit(0)
            
            
            

if __name__ == '__main__':
    parser = optparse.OptionParser()
    
    parser.add_option('--add_wordlist', default=None, help='Adds a wordlist to the json database')
    
    parser.add_option('--analyze_new_formats', default=False, action='store_true', help='Analyze database for new format')
    
    parser.add_option('--database_dir', default=".", help="Location of the database.d")
    
    parser.add_option('--first_run', default=False, action='store_true', help='Creates new database. WARNING: may rewrite old database')
    
    '''
    parser.add_option('--ip', default='127.0.0.1', help="Address of NetworkTable server")
    
    parser.add_option('-v', '--verbose', default=False, action='store_true', help='Enable verbose logging')
    
    parser.add_option('-c', '--config', default="ExampleConfig.json", help='Config for graph layout')
    '''
    
    options, args = parser.parse_args()
    
    # Setup logging
    #logging.basicConfig(datefmt=log_datefmt, format=log_format, level=logging.DEBUG if options.verbose else logging.INFO)
    
    scrabbler = Scrabbler(options)