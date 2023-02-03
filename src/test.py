from ortools.linear_solver import pywraplp
import math
# customers_coord is the coordinate of custumer. The deliver time between 2 person is the distance euclean between them
customers_coord = [(82.0, 76.0), (96.0, 44.0), (50.0, 5.0), (49.0, 8.0), (13.0, 7.0), (29.0, 89.0), (58.0, 30.0), (84.0, 39.0), (14.0, 24.0), (2.0, 39.0), (3.0, 82.0), (5.0, 10.0), (98.0, 52.0), (84.0, 25.0), (61.0, 59.0), (1.0, 65.0), (88.0, 51.0), (91.0, 2.0), (19.0, 32.0), (93.0, 3.0), (50.0, 93.0), (98.0, 14.0), (5.0, 42.0), (42.0, 9.0), (61.0, 62.0), (9.0, 97.0), (80.0, 55.0), (57.0, 69.0), (23.0, 15.0), (20.0, 70.0), (85.0, 60.0), (98.0, 5.0)]
# receiving_time is the time what customer receive item
receiving_time = [0.0, 19.0, 21.0, 6.0, 19.0, 7.0, 12.0, 16.0, 6.0, 16.0, 8.0, 14.0, 21.0, 16.0, 3.0, 22.0, 18.0, 19.0, 1.0, 24.0, 8.0, 12.0, 4.0, 8.0, 24.0, 24.0, 2.0, 20.0, 15.0, 2.0, 14.0, 9.0]
#num_postmas is the number of postman
num_postmans = 5
customers_coord = customers_coord[:9]
receiving_time = receiving_time[:9]
num_customers = len(customers_coord)

# Calculate the delivery time between each customer
delivery_time = [[math.sqrt((customers_coord[i][0] - customers_coord[j][0]) ** 2 + (customers_coord[i][1] - customers_coord[j][1]) ** 2) for j in range(num_customers)] for i in range(num_customers)]

# Define the solver
solver = pywraplp.Solver('VRP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

# Create variables for the routes for each postman and each customer
x = {}
for i in range(num_customers):
    for j in range(num_customers):
        for k in range(num_postmans):
            x[i, j, k] = solver.IntVar(0, 1, "x[%i,%i,%i]" % (i, j, k))

# Constraints
# 1. Each customer is visited only once
for i in range(1, num_customers):
    solver.Add(solver.Sum(x[i, j, k] for j in range(num_customers) for k in range(num_postmans)) == 1)

# 2. Each customer is delivered by only one postman
for i in range(1, num_customers):
    for k in range(num_postmans):
        solver.Add(solver.Sum(x[j, i, k] for j in range(num_customers)) == 1)

# 3. A customer can only be delivered by one postman after it is received
for i in range(1, num_customers):
    for j in range(1, num_customers):
        if i != j:
            for k in range(num_postmans):
                solver.Add(x[i, j, k] <= x[0, i, k])

# 4. A postman cannot visit a customer twice before returning to the depot
for i in range(1, num_customers):
    for j in range(1, num_customers):
        for k in range(num_postmans):
            solver.Add(x[i, j, k] <= x[j, 0, k])

# Objective function: Minimize the total delivery time
objective = solver.Sum(x[i, j, k] * delivery_time[i][j] for i in range(num_customers) for j in range(num_customers) for k in range(num_postmans))
solver.Minimize(objective)

# Solve the problem
status = solver.Solve()

# Output the results
if status == pywraplp.Solver.OPTIMAL:
    print("Total value = ", solver.Objective().Value())
    print('Time = ', solver.WallTime(), ' milliseconds')
else:
    print("The problem does not have an optimal solution.")
