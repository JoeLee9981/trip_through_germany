'''
Created on Nov 28, 2012

@author: Joseph Lee
'''

class City(object):
    '''
    classdocs
    '''


    def __init__(self, key, name, start, xTime, xCost):
        '''
        Constructor
        '''
        self._key = key
        self._name = name
        self._start = start
        self._xTime = xTime
        self._xCost = xCost
        
    def __str__(self):
        return str.format("{0}", self._name)
    