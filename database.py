import json
import os

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

class DataBase:
    
    def __init__(self, directory, new=False):
        self.directory = directory
        self.databases = {}
        self.databases_changed_mask = {}
        
        
        if(not new):
            for letter in ALPHABET:
                try:
                    with open("%s/database.d/%s.json" %(self.directory, letter)) as database:
                        self.databases[lettter] = json.load(database)
                        self.databases_changed_mask[letter] = False
                except:
                    print('Error while loading databases. Exiting process...')
                sys.exit(1)
        else:
            for letter in ALPHABET:
                self.databases[letter] = {}
                self.databases_changed_mask[letter] = False
            os.makedirs("%s/database.d" %(self.directory))
                
    # TODO: Run this word through all existing formats
    def addWord(self, word):
        word = word.lower()
        if word not in self.databases[word[0]]:
            self.databases[word[0]][word] = {}
            self.databases_changed_mask[word[0]] = True
    
    def hasWord(self, word):
        word = word.lower()
        try:
            if word in self.databases[word[0]]:
                return True
        except KeyError:
            print('invalid key: %s' % word[0])
        return False
        
    def addReference(self, word, reference):
        pass
        
    def close(self):
        for letter, changed in self.databases_changed_mask.items():
            if changed:
                with open("%s/database.d/%s.json" %(self.directory, letter), "w") as database:
                    json.dump(self.databases[letter], database, indent=4, sort_keys=True)
        