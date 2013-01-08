'''
Created on Oct 28, 2012

@author: Joseph Lee
'''
import sqlite3
from city import City
from connection import Connection
import decimal

class Data_Manager(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._cities = self._create_dict()
        
    def _create_dict(self):
        dict = {}        
        conn = sqlite3.connect("GermanyGraph.db")
        cursor = conn.cursor()
        query = "Select Key, Name From Cities"
        cursor.execute(query)
        data = cursor.fetchall()
        
        for x in data:
            dict[x[0]] = x[1]
        return dict

        
    def display_data(self):
        conn = sqlite3.connect("GermanyGraph.db")
        cursor = conn.cursor()
        print("----------CITY TABLE----------")
        self._display_cities(cursor)
        print()
        print("-------CONNECTION TABLE-------")
        self._display_connections(cursor)

    
    def _display_connections(self, cursor):
        query = "Select * From Connections"
        cursor.execute(query)
        data = cursor.fetchall()
        print("%7s %7s %15s %15s %15s %15s %15s %15s" % ("City 0", "City 1", "Cost By Train", "Cost By Diesel",
                                                               "Cost By Petrol", "Time By Train", "Time By Car", "Distance" ))
        for x in data:
            print("%7d %7s %15.2f %15.2f %15.2f %15.2f %15.2f %15.2f" % (x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]))
            
    def _display_cities(self, cursor):
        query = "Select * From Cities"
        cursor.execute(query)
        data = cursor.fetchall()
        print("%-5s %-15s %-10s %10s %12s" % ("Key", "City", "Start", "Extra Cost", "Extra Time" ))
        for x in data:
            print("%-5d %-15s %-10d %10.2f %12d" % (x[1], x[2], x[3], x[0], x[4]))

    def get_cities(self):
        conn = sqlite3.connect("GermanyGraph.db")
        cursor = conn.cursor()
        query = "Select Key From Cities"
        cursor.execute(query)
        data = cursor.fetchall()
        cities = []
        for x in data:
            cities.append(x[0])
        return cities
    
    def city_by_key(self, key):
        conn = sqlite3.connect("GermanyGraph.db")
        cursor = conn.cursor()
        query = "Select * From Cities Where Key == ?"
        cursor.execute(query, [(key)])
        data = cursor.fetchall()
        return City(data[0][1], data[0][2], data[0][3], data[0][4], data[0][0])
    
    def find_connect(self, city0, city1):
        conn = sqlite3.connect("GermanyGraph.db")
        cursor = conn.cursor()
        query = """
            Select * From Connections 
            Where (City0 == ? and City1 == ?)
            or (City1 == ? and city0 == ?)
            """
        cursor.execute(query, (city0, city1, city0, city1))
        data = cursor.fetchall()
        if len(data) > 0:
            return Connection(data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6], data[0][7], data[0][8])
        else:
            return None
            
    def get_start(self):
        conn = sqlite3.connect("GermanyGraph.db")
        cursor = conn.cursor()
        query = "Select Key From Cities Where Start == '1'"
        cursor.execute(query)
        data = cursor.fetchall()
        a = []
        for x in data:
            a.append(x[0])
        return a
            
    def get_conn(self, city):
        conn = sqlite3.connect("GermanyGraph.db")
        cursor = conn.cursor()
        query = "Select * From Connections Where City0 == ? or City1 == ?"
        cursor.execute(query, (city, city))
        data = cursor.fetchall()
        data = self._convert_conn(data)
        return data
        
    def _convert_conn(self, connections):
        a = []
        for x in connections:
            connect = Connection(x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8])
            weight = connect.get_weight()
            #print(x)
            #print(weight, connect.city0, connect.city1)
            #print("-------------------------------------------")
            a.append((weight, connect.city0, connect.city1))
            a.append((weight, connect.city1, connect.city0))
        return a      
    
    def get_dist(self):
        conn = sqlite3.connect("GermanyGraph.db")
        cursor = conn.cursor()
        query = "Select Key, Distance From Connections"
        cursor.execute(query)
        data = cursor.fetchall()
        a = []
        for x in data:
            a.append((x[0], x[1]))
        self.load_data(a)
                
    def load_data(self, a):
        conn = sqlite3.connect("GermanyGraph.db")
        for i in range(32, len(a)):
            
            cDies = self.diesel(a[i][1])
            sq1 = """
            UPDATE Connections
            SET CostByDiesel = ?
            WHERE Key = ?
            """
            conn.execute(sq1, (cDies, i+1))
            
            cPet = self.petrol(a[i][1])
            sq1 = """
            UPDATE Connections
            SET CostByPetrol = ?
            WHERE Key = ?
            """
            conn.execute(sq1, (cPet, i+1))
            
            t = self.time(a[i][1])
            sq1 = """
            UPDATE Connections
            SET TimeByCar = ?
            WHERE Key = ?
            """
            conn.execute(sq1, (t, i+1))
        conn.commit()
        
    def diesel(self, x):
        return x * 1.49 / 13

    def petrol(self, x):
        return x * 1.61 / 22

    def time(self, x):
        return x / 2.25