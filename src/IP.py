from FileController import FileController
from ortools.linear_solver import pywraplp

# customers_coord is the coordinate of custumer. The deliver time between 2 person is the distance euclean between them
customers_coord = [(82.0, 76.0), (96.0, 44.0), (50.0, 5.0), (49.0, 8.0), (13.0, 7.0), (29.0, 89.0), (58.0, 30.0), (84.0, 39.0), (14.0, 24.0), (2.0, 39.0), (3.0, 82.0), (5.0, 10.0), (98.0, 52.0), (84.0, 25.0), (61.0, 59.0), (1.0, 65.0), (88.0, 51.0), (91.0, 2.0), (19.0, 32.0), (93.0, 3.0), (50.0, 93.0), (98.0, 14.0), (5.0, 42.0), (42.0, 9.0), (61.0, 62.0), (9.0, 97.0), (80.0, 55.0), (57.0, 69.0), (23.0, 15.0), (20.0, 70.0), (85.0, 60.0), (98.0, 5.0)]
# receiving_time is the time what customer receive item
receiving_time = [0.0, 19.0, 21.0, 6.0, 19.0, 7.0, 12.0, 16.0, 6.0, 16.0, 8.0, 14.0, 21.0, 16.0, 3.0, 22.0, 18.0, 19.0, 1.0, 24.0, 8.0, 12.0, 4.0, 8.0, 24.0, 24.0, 2.0, 20.0, 15.0, 2.0, 14.0, 9.0]

customers_coord = customers_coord[:9]
receiving_time = receiving_time[:15]
#num_postmas is the number of postman
num_postmans = 5

# num_postmans, customers_coord, receiving_time = FileController.Read_File_Data()
# print(num_postmans, customers_coord, receiving_time)

#num_customers is the number of customers
num_customers = len(customers_coord)
print(num_customers)
#transport_duration is fuction what calculate time between 2 person between their coordinate
def transport_duration(customer_x, customer_y):
    s_sq_difference = 0
    for customer_xi,customer_yi in zip(customer_x, customer_y):
        s_sq_difference += (customer_xi - customer_yi)**2    
    distance = s_sq_difference**0.5
    return int(distance)

def main():
    solver = pywraplp.Solver('VRP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    if not solver:
        return
    x = {}
    y = {}
    z = {}
    

    for k in range(num_postmans):
        for i in range(num_customers):
            for j in range(num_customers):
                # x[i, j, k] = 1 if k_th postman go through the path between i_th customer and j_th customer
                # x[i, j, k] = 0 vice versa    
                # 0 <= x[i, j, k] <= 1 with each any i, j, k
                x[i, j, k] = solver.IntVar(0, 1, f'x_{i}_{j}_{k}')

    for k in range(num_postmans):
        for i in range(num_customers):
            # y[i, k] = 1 if k_th postman visited i_th customer
            # y[i, k] =  vice versa
            y[i, k] = solver.IntVar(0, 1, f'y_{i}_{k}')

        for i in range(num_customers):
            #z[i, k] is the number of visits i_th customer of k_th postman 
            z[i, k] = solver.IntVar(0, num_customers, f'z_{i}_{k}')
    
    #res is the result
    res = solver.IntVar(0, solver.infinity(), 'res')

    for i in range(1, num_customers):
        solver.Add(
            solver.Sum(x[i, j, k] for j in range(num_customers) for k in range(num_postmans)) == 1
        )
    for k in range(num_postmans):
        #Each postman will leave the start point once time
        solver.Add(
             solver.Sum(x[0, i, k] for i in range(1, num_customers)) == 1
        )

        #Each postman will return the start point once time
        solver.Add(
            solver.Sum(x[i, 0, k] for i in range(1, num_customers)) == 1
        )

        #Each postman will return the start point once time
        for i in range(num_customers):
            #k_th postman will vist i_th customer once time
            solver.Add(
                solver.Sum(x[i, j, k] for j in range(num_customers)) == y[i, k]
            )

            solver.Add(
                solver.Sum(x[j, i, k] for j in range(num_customers)) == y[i, k]
            )

            solver.Add(
                x[i, i, k] == 0
            )
        # for i in range(num_customers):
        #     for j in range(1, num_customers):
        #         if i == j: continue
        #         solver.Add(
        #             z[i, k]  + x[i, j, k] <= z[j, k]
        #         )
        # solver.Add(z[0, k] == 0)
    
    for k in range(num_postmans):
        for i in range(1, num_customers):
            for j in range(1, num_customers):
                # solver.Add(
                #     z[i, k] + 1 - (num_customers - 1) * ( 1- x[i, j, k]) <= z[j, k]
                # )
                if i == j: continue
                solver.Add(
                    z[i, k] - z[j, k] + num_customers * x[i, j, k] <= num_customers - 1
                )
    
    for k in range(num_postmans):
        solver.Add(
            solver.Sum(x[i, j, k] * (transport_duration(customers_coord[i], customers_coord[j]) + receiving_time[j]) for i in range(num_customers) for j in range(num_customers)) <= res
        )
    solver.Minimize(res)
    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print("Total value = ", solver.Objective().Value())
        print(res.solution_value())
        for k in range(num_postmans):
            print("postman: ", k)
            for i in range(num_customers):
                for j in range(num_customers):
                    if x[i, j, k].solution_value() == 1:
                        print(i, j, "Time: ", transport_duration(customers_coord[i], customers_coord[j]) + receiving_time[j])
        print('Time = ', solver.WallTime(), ' milliseconds')
    else:
        print('The problem does not have an optimal solution.')



if __name__ == '__main__':
    main()

