import json
import os
import sys
from email._header_value_parser import InvalidParameter


ALPHABET = "abcdefghijklmnopqrstuvwxyz"
NUMBERS = "123456790"

class DataBase:
    VERSION_NUMBER = 0.1
    def __init__(self, directory, new=False):
        self.directory = directory
        
        self.databases = {}
        self.databases_changed_mask = {}
        
        self.info = {}
        self.patterns = {}
        
        if(not new):
            #Load all letter databases
            for letter in ALPHABET:
                with open("%s/database.d/%s.json" %(self.directory, letter)) as database:
                    self.databases[letter] = json.load(database)
                    self.databases_changed_mask[letter] = False
                
            #Load the info file   
            with open("%s/database.d/info.json" % self.directory) as info:
                self.info = json.load(info)
            
            #Load all patterns from info file   
            for pattern in self.info["known_patterns"]:
                file_friendly_pattern = pattern.replace("*", ".")
                with open("%s/database.d/patterns/%s.json" %(self.directory, file_friendly_pattern)) as f:
                        self.patterns[pattern] = json.load(f)
        else:
            for letter in ALPHABET:
                self.databases[letter] = {}
                self.databases_changed_mask[letter] = False
            self.info["known_patterns"] = []
            os.makedirs("%s/database.d/patterns" %(self.directory))
            
    def addWord(self, word):
        word = word.lower()
        if word not in self.databases[word[0]]:
            self.databases[word[0]][word] = {}
            self.databases[word[0]][word]["conforms_to"] = []
            self.databases_changed_mask[word[0]] = True
            
            self._analyzeForWord(word)
    
    def hasWord(self, word):
        word = word.lower()
        try:
            if word in self.databases[word[0]]:
                return True
        except KeyError:
            print('invalid key: %s' % word[0])
        return False
    
    def getConformities(self, word):
        return self.databases[word[0]][word]["conforms_to"]
    
    def getPatterns(self):
        return self.info["known_pattern"]
    
    def addPattern(self, pattern):
        '''
        :params
        @pattern the format. Use _ any unique letter and * for any letter you can add letters
                Example: "*A*" finds all that have an A letter
                Example: "*_*" finds all that have a unique letter
                Example: "*__*" finds all that have any two adjacent unique letters
                Example: "*_*_*" finds all that have any two unique letters
                Example: "*_" finds all that end with a unique letter
                Example: "_*" finds all that start with a unique letter
                
                TODO:
                Example: "A3A" finds words that contain Two "a" letters seperated by 3 letters 
            '''
        pattern = pattern.lower()
        
        for char in pattern:
            if char not in ALPHABET:
                if char is not "_":
                    if char is not "*":
                        raise InvalidParameter
        
        print("Tests passed for: \"%s\"" % pattern)
        
        if "_" in pattern:
            print("Starting dynamic analysis for \"%s\"" % pattern)
            for letter in ALPHABET:
                compare_pattern = pattern
                compare_pattern = compare_pattern.replace("_", letter)
                
                self.patterns[compare_pattern] = []
                
                self.info["known_patterns"].append(compare_pattern)
                self._analyzeForPattern(compare_pattern)
        else:
            self.patterns[pattern] = []
            
            self.info["known_patterns"].append(pattern)
            self._analyzeForPattern(pattern)
    
    def _analyzeForWord(self, word):
        print("Analyzing \"%s\" for all existing pattern" % word, end="")
        for pattern in self.patterns:
            
            p = WordPattern(pattern)
            
            if p.conformsToFormat(word):
                self._addConformity(word, patter)
        
        print(": Conforms to %s" % self.getConformities(word))
        
    
    def _analyzeForPattern(self, pattern):
        p = WordPattern(pattern)
        count = 0
        
        print("Analyzing database for pattern \"%s\"" % pattern, end="")
        
        for letter in self.databases:
            for word in self.databases[letter]:
                if p.conformsToFormat(word):
                    count += 1
                    self._addConformity(word, pattern)
        
        print(": Found %s words that conform!" % count)
    
    def _addConformity(self, word, pattern):
        self.databases[word[0]][word]["conforms_to"].append(pattern)
        self.patterns[pattern].append(word)
        
    def close(self):
        for letter in self.databases:
            with open("%s/database.d/%s.json" %(self.directory, letter), "w") as f:
                json.dump(self.databases[letter], f, indent=4, sort_keys=True)
        
        for pattern in self.info["known_patterns"]:
            file_friendly_pattern = pattern.replace("*", ".")
            with open("%s/database.d/patterns/%s.json" %(self.directory, file_friendly_pattern), "w") as f:
                    json.dump(self.patterns[pattern], f, indent=4, sort_keys=True)
        
        with open("%s/database.d/info.json" % self.directory, "w") as f:
            json.dump(self.info, f, indent=4, sort_keys=True)
        

class WordPattern:

    ANY_LETTER = "*"
    
    '''
    :params
    @pattern the format. Use _ any unique letter and * for any letter you can add letters
            Example: "*A*" finds all that have an A letter
            Example: "*AA*" finds all that have two adjacent A letters
            Example: "*A*A*" finds all that have two A letters
            Example: "*A" finds all that end with an A letter
            Example: "A*" finds all that start with an A letter
            
            TODO:
            Example: "A3A" finds words that contain Two "a" letters seperated by 3 letters 
    '''
    def __init__(self, pattern):
        self.pattern = pattern.lower()
    
    def conformsToFormat(self, word):
        if self._conformsToWildCardFormat(word, self.pattern):
            return True
        return False
                
    
    def _conformsToWildCardFormat(self, word, pattern):
        if self.pattern is "*":
            return True
        
        #Splits the pattern into substrings at wildcards;
        sub_strings = []
        current_string = ""
        for i, char in enumerate(pattern):
            if char is self.ANY_LETTER:
                #Determines if in first position (important for positioning)
                if current_string is not "":
                    sub_strings.append(current_string)
                    current_string = ""
                else:
                    sub_strings.append("*")
                
                #Adds wildcard if in last postition
                if i == len(pattern)-1:
                    sub_strings.append("*")
            else:
                current_string += char   
                  
                #Adds text if in last position
                if i == len(pattern)-1:
                    sub_strings.append(current_string)
        
        #If the pattern doesn't contain wildcards     
        if sub_strings is []:
            if word is pattern:
                return True
            return False
            
            if word is not pattern:
                return False
            return True
        
         #Makes sure word is long enough for the pattern to be fufilled
        minLength = 0
        for sub_string in sub_strings:
            if sub_string is not "*":
                minLength += len(sub_string)
        
        if len(word) < minLength:
            return False
        
        #If first is not moveable get rid of wildcard and adjust word
        if sub_strings[0] is not "*":
            if word[:len(sub_strings[0])] is not sub_strings[0]:
                return False
            else:
                if len(sub_strings) == 1: #If that was the only element
                    return True
            word = word[len(sub_strings[0]):]
        del sub_strings[0] #First no longer needed
        
        #If last is not moveable check it and get rid of wildcard and adjust word
        last_index = len(sub_strings)-1
        if sub_strings[last_index] is not "*":
            if word[(-1*len(sub_strings[last_index])):] is not sub_strings[last_index]:
                return False
            else:
                if last_index == 0: # if that was the only param
                    return True
            word = word[:(-1*len(sub_strings[last_index]))]
        del sub_strings[last_index]
        
        if self._wildCardSearch(sub_strings, word):
            return True
        return False
    
    def _wildCardSearch(self, ordered_substrings, string,):
        '''
        :param @ordered_substrings an list containing the substrings patterns to match "*T*N*TH*" would be ["t", "n", "th"]
        :param @string the string to check against
        '''
        #print(ordered_substrings)
        #print(string)
        ordered_elements = len(ordered_substrings)
        
        #Gets the total length of the string and the substrings
        total_string_length = len(string)
        total_substring_length = 0
        for sub_string in ordered_substrings:
                total_substring_length += len(sub_string)
        
        for i in range(0, total_string_length):
            length_of_first = len(ordered_substrings[0])
            if(total_string_length-i < total_substring_length):
                break
            
            higher_bound = (-1*(total_string_length-(length_of_first+i)))
            if higher_bound == 0:
                higher_bound = None
            if string[i:higher_bound] == ordered_substrings[0]:
                if ordered_elements == 1:
                    return True
                if self._wildCardSearch(ordered_substrings[1:], string[i+length_of_first:]):
                    return True
        return False    
                
                
                
                
    
                
           
                
        