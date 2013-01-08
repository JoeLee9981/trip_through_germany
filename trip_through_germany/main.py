'''
Created on Oct 28, 2012

@author: Joseph Lee
'''
from shortest_path import *
from data_manager import Data_Manager
from city import City
from connection import Connection
import math

def main():

    data = Data_Manager()
    path = []
    paths = prim(path)
    blCost = 0
    blTime = 0
    blDist = 0
    
    shortest = calc_shortest(paths)
    print_results(shortest)
    blCost, blTime, blDist = alt_stats(shortest, 21)
    print()
    print("""        The results show that most efficient route on both time and cost is Petrol. Time by train is based directly
        off the website. Time by car is based directly off an average speed of 135kmh. Cost by car is based either on
        daily or weekly values, and cost by train is figured per trip or per weekly pass. The reason petrol was more
        efficient is that not all routes are available via train, and the cost for 5 tickets is significant compared to
        a car rental.
        Fewer people traveling will change the results. Also costs by car were figured off prices in the assignment description
        actual prices may reflect higher due to inflation. Altogether however for 5 people, renting a petrol car by the week will
        be by far the most efficient price. Although actual time spent traveling by train will be faster since you wont always
        be able to travel the full 135kmh.""")
    print()
    print("------------------BOTTOM LINE COSTS------------------")
    print(str.format("Traveling Cost: ${0:.6}, Time Traveled: {1:.4} hours, Distance Traveled: {2:.6} km ({3:.6} miles)", blCost, blTime / 60, blDist, blDist * .621371))
    xtra_cost(12.00, "on a taxi to drive under the river")
    blCost += 12
    xtra_cost(1169.80, "purchasing iPad's at 180 Euros ($233.96) each")
    blCost += 1169.8
    xtra_cost(24, "on a taxi to visit the Hauptbahnof 10km away")
    blDist += 10
    blCost += 24
    print(str.format("    Extra Time: {0} {1}", 24, "hours to visit the spa in Baden Baden"))
    blTime += 24 * 60
    print(str.format("******BOTTOM LINE COST: ${0:.6}, BOTTOM LINE TIME: {1:.4} hours, BOTTOM LINE DISTANCE: {2:.6} km ({3:.6} miles)", blCost, blTime / 60, blDist, blDist * .621371))
    
    input("press any key to end")

def xtra_cost(val, exp):
    print(str.format("    Extra Cost: ${0} {1}", float(val), exp))
    
def calc_shortest(paths):
    shortest = float('inf')
    shortIndex = 0
    
    for i in range(len(paths)):
        totalDist = 0
        
        for connect in paths[i]:
            totalDist += connect[2]
            
            
        if totalDist < shortest:
            shortest = totalDist
            shortIndex = i
            
    return paths[shortIndex]
        

def print_results(a):
    totalDist = 0;
    totalCost = 0;
    totalTime = 0;
    i = 0;
    data = Data_Manager()
    
    print("---------Trip Through Germany - Shortest Path---------")
    print()
    print("---------Tracing path based on either Petrol, Diesel or Train per city on the path-------")
    print("Starting City:", data.city_by_key(a[0][0]))
    
    for conn in a:
        i += 1
        start = conn[0]
        end = conn[1]
        city = data.city_by_key(start)
        connect = data.find_connect(start, end)

        if connect == None:
            dist = conn[2]
            dies = diesel(dist)
            pet = petrol(dist)
            time = get_time(dist)
            connect = Connection(conn[0], conn[1], 0, dies, pet, 0, time, dist)
            
        dist, type, cost, time = connect.opt_weight()
        
        totalDist += dist
        totalCost += cost
        totalTime += time
        print("Stop:", i, "--", city, conn[1])
        print(str.format("Distance Traveled: {0:.4} km, by {1}, Travel Cost: ${2:.5}, Time Traveled: {3:.4} minutes", float(dist), type, float(cost), float(time)))
    print("-----------------------------------------------------------")
    print()
    print("    Result Totals for Alternating Methods: ----")
    print(str.format("       Cost: ${0:.6}, Time: {1:.4} hours, Distance: {2:.6} km ({3:.6} miles)", totalCost, totalTime / 60, totalDist, totalDist * .621371))
    print()
 
def alt_stats(path, numOfDays):
    xtraExpense = 0
    weeks = math.ceil(float(numOfDays / 7)) 
    totalDist = 0
    totalPetCost = 600 * weeks
    totalDiesCost = 700 * weeks
    totalTrainCost = 2415 * weeks
    totalTrainTime = 0
    totalCarTime = 0
    i = 0
    
    data = Data_Manager()
    
    for conn in path:
        start = conn[0]
        end = conn[1]
        connect = data.find_connect(start, end)
        
        if connect == None:
            dist = conn[2]
            dies = diesel(dist)
            pet = petrol(dist)
            time = get_time(dist)
            connect = Connection(conn[0], conn[1], 0, dies, pet, 0, time, dist)
        
        totalDist += connect.distance
        totalPetCost += connect.costByPetrol
        totalDiesCost += connect.costByDiesel
        if connect.costByTrain == 0:
            totalTrainCost += connect.costByPetrol + 115
            totalTrainTime += connect.timeByCar
        totalTrainTime += connect.timeByTrain
        totalCarTime += connect.timeByCar
    if(totalPetCost + totalCarTime < totalTrainCost + totalCarTime):
        if(totalPetCost < totalDiesCost):
            return totalPetCost, totalCarTime, totalDist
        else:
            return totalDiesCost, totalCarTime, totalDist   
    elif(totalDiesCost + totalCarTime < totalTrainCost + totalCarTime):
        return totalDiesCost, totalCarTime, totalDist
    else:
        return totalTrainCost, totalTrainTime, totalDist
    print("---Alternate atistics comparing different travel methods---")
    print("    *Costs are based on weekly rates using only car or train,")
    print("    *When calculating Train, uses price for petrol when train is not availaable")
    print()
    print("    By Train: ----")
    print(str.format("       Cost: ${0:.6}, Time: {1:.4} hours, Distance: {2:.6} km ({3:.6} miles)", totalTrainCost, totalTrainTime / 60, totalDist, totalDist * .621371))
    print()
    print("    By Petrol Car: ----")
    print(str.format("       Cost: ${0:.6}, Time: {1:.4} hours, Distance: {2:.6} km ({3:.6} miles)", totalPetCost, totalCarTime / 60, totalDist, totalDist * .621371))
    print()
    print("    By Diesel Car: ----")
    print(str.format("       Cost: ${0:.6}, Time: {1:.4} hours, Distance: {2:.6} km ({3:.6} miles)", totalDiesCost, totalCarTime / 60, totalDist, totalDist * .621371))
    
def by_train():
    pass

def by_car():
    pass

def diesel(x):
    return x * 1.49 / 13

def petrol(x):
    return x * 1.61 / 22

def get_time(x):
    return x / 2.25
    

if __name__ == '__main__':
    main()