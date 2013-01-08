'''
Created on Nov 28, 2012

@author: Joseph Lee
'''

class Connection(object):
    '''
    classdocs
    '''


    def __init__(self, city0, city1, costByTrain, costByDiesel,
                 costByPetrol, timeByTrain, timeByCar, distance):
        '''
        Constructor
        '''
        self.city0 = city0
        self.city1 = city1
        self.costByTrain = costByTrain
        self.costByDiesel = costByDiesel
        self.costByPetrol = costByPetrol
        self.timeByTrain = timeByTrain
        self.timeByCar = timeByCar
        self.distance = distance
        
    def opt_weight(self):
        train = self.train_weight()
        petrol = self.pet_weight()
        diesel = self.dies_weight()
        if petrol < diesel:
            if train < petrol and train > 0:
                return self.distance, "Train", self.costByTrain, self.timeByTrain
            else:
                return self.distance, "Petrol", 230 + self.costByPetrol, self.timeByCar
        else:
            if train < diesel and train > 0:
                return self.distance, "Train", self.costByTrain, self.timeByTrain
            else:
                return self.distance, "Diesel", 230 + self.costByDiesel, self.timeByCar
    
    def get_weight(self):
        return self.distance
    
    def train_weight(self):
        return (self.costByTrain + 2 * self.timeByTrain) / 2
        #return self.timeByTrain
    
    def pet_weight(self):
        #cost of rental is based off a per day basis looked up online, to optimize path on a per day basis instead of weekly
        return ( 230 + self.costByPetrol + 2 * self.timeByCar) / 2
        #return self.timeByCar
    
    def dies_weight(self):
        #cost of rental is based off a per day basis looked up online, to optimize path on a per day basis instead of weekly
        return (230 + self.costByDiesel + 2 * self.timeByCar) / 2
        #return self.timeByCar
    
    def __str__(self):
        return str.format("City0: {0} City1: {1}", self.city0, self.city1)
    
    def __lt__(self, connection):
        #return self.opt_weight() < connection.opt_weight()
        return self.distance < connection.distance
    
    def __gt__(self, connection):
        #return self.opt_weight() > connection.opt_weight()
        return self.distance > connection.distance
    
    def __eq__(self, connection):
        if connection == None:
            return False
        if not connection is Connection:
            return False
        #return self.opt_weight() == connection.opt_weight()
        return self.distance == connection.distance
    
    def __hash__(self):
        return int(self.city0 * 7 + self.city1 * 13 + self.opt_weight() * 39 + 
                   self.costByTrain * 43 + self.costByPetrol * 23 + 
                   self.costByDiesel * 11 + self.distance * 113)
    
    