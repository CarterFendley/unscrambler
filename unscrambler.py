import logging
import optparse
import sys

#!/usr/bin/env python3
from database import DataBase


logger = logging.getLogger('dashboard')
log_datefmt = "%H:%M:%S"
log_format = "%(asctime)s:%(msecs)03d %(levelname)-8s: %(name)-20s: %(message)s"

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

class Unscrambler:
    def __init__(self, options):
        self.database = None
        
        if options.first_run:
            self.database = DataBase(options.database_dir, new=True)
        else:
            self.database = DataBase(options.database_dir)
        
        if options.add_wordlist is not None:
            with open(options.add_wordlist, 'r') as file:
                
                count = 0
                for word in file:
                    word = word.lower()
                    word = word.replace("\n", "")
                    
                    #Checks if word is legal
                    valid = True
                    for char in word:
                        if char not in ALPHABET:
                            valid = False
                            print("\"%s\" contains invalid characters" % word)
                            break
                        
                    if not valid:
                        continue 

                    if not self.database.hasWord(word):
                       self.database.addWord(word)
                       count += 1
                       
                print("Added %s valid words to database" % count)
                    
            self.database.close()
            sys.exit(0)
            
        if options.add_pattern is not None:
            #print(options.add_pattern)
            self.database.addPattern(options.add_pattern)
        
        self.database.close()
            
            
            

if __name__ == '__main__':
    parser = optparse.OptionParser()
    
    parser.add_option('--add_wordlist', default=None, help='Adds a wordlist to the json database')
    
    parser.add_option('--add_pattern', default=None, help='adds pattern to database')
    
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
    
    unscrambler = Unscrambler(options)