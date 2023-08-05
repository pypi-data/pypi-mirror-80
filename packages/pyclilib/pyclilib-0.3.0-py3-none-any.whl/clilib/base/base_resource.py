import argparse
from abc import ABC

class BaseResource(ABC):    
    def __init__(self):
        self._parser = None
        self._name = ""
        self._verbs = []


    @property
    def parser(self):
        return self._parser
    

    @property
    def name(self):
        return self._name
    

    @property
    def verbs(self):
        return self._verbs
    
    
    @parser.setter
    def parser(self, val):
        assert(isinstance(val, argparse.ArgumentParser))
        
        self._parser = val

    
    @name.setter
    def name(self, val):
        assert(isinstance(val, str))

        self._name = val


    @verbs.setter
    def verbs(self, val):
        assert(isinstance(val, list))

        self._verbs = val
    

    @parser.deleter
    def parser(self):
        del self._parser


    @name.deleter
    def name(self):
        del self._name


    @verbs.deleter
    def verbs(self):
        del self._verbs