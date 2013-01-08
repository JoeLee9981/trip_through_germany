PYTHON: Trip Through Germany: (run main.py to start)

  This alogorithm plots a trip through 22 cities in Germany, finding the most efficient route based upon
  cost, time and distance. You can start from any one of four German cities that contain an international
  airport, then finds the optimal route for each of the 4 starting cities. Once the 4 routes are determined
  it will choose the most efficient of the routes and run comparisons based on cost to find the best way to
  travel
  
  Travel choices include:
  1. Rental Car (petrol)
  2. Rental Car (diesel)
  3. Travel by Metro
  4. Travel by taxi (only used in certain scenarios)
  
  To choose the best route the algorithm will first use Prim's to create a Minimum Spanning Tree (MST) and then splits
  the MST into separate routes. It will then use Djikstra's shortest path algorithm to connect each route to allow
  for the most efficient back tracking. Once that is done all routes are connected together into one, and then return
  to a city with an airport.

  Analytics of the route will be displayed in a breakdown view in the console.
