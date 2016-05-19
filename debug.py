#!/usr/bin/env python3

import optparse
import sys

from database import WordPattern

class SearchDebug:
    def __init__(self, options):
        self.pattern = WordPattern(options.pattern)
        self.word = options.word
        
        if self.pattern.conformsToFormat(self.word):
            print('Word conforms')
        else:
            print('Word does not confirm')

if __name__ == '__main__':
    parser = optparse.OptionParser()
    
    parser.add_option('--word', default=None)
    parser.add_option('--pattern', default=None)
    
    options, args = parser.parse_args()
    
    # Setup logging
    #logging.basicConfig(datefmt=log_datefmt, format=log_format, level=logging.DEBUG if options.verbose else logging.INFO)
    
    debug = SearchDebug(options)