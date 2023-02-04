from FileController import FileController
from ortools.linear_solver import pywraplp

def get_data():
    filenames = []
    for i in range(32, 40):
        if i == 35: continue
        filenames.append(f'../data/A-n{i}-k5.txt')

    num_postmans, customers_coords, receiving_times = FileController.Read_Multi_File_Data(filenames)
    
    num_customers = [5, 7, 9, 10]
    n = len(num_customers)
    m = len(num_postmans)

    num_postmans[0:n] = [2]*n
    num_postmans[n:] = [3]*(m - n)   

    for i in range(m):
        customers_coords[i] = customers_coords[i][:num_customers[i % n]]
        receiving_times[i] = receiving_times[i][:num_customers[i % n]]

    return num_postmans, customers_coords, receiving_times

#transport_duration is fuction what calculate time between 2 person between their coordinate
def transport_duration(customer_x, customer_y):
    s_sq_difference = 0
    for customer_xi,customer_yi in zip(customer_x, customer_y):
        s_sq_difference += (customer_xi - customer_yi)**2    
    distance = s_sq_difference**0.5
    return distance

def solve(num_postman, customers_coord, receiving_time):
    #num_customers is the number of customers
    num_customers = len(customers_coord)
    solver = pywraplp.Solver('VRP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    if not solver:
        return
    x = {}
    y = {}
    z = {}
    
    print("-----------------------------------------------------------")
    print(f"Start solving: {num_customers} customer, {num_postman} postman")
    for k in range(num_postman):
        for i in range(num_customers):
            for j in range(num_customers):
                # x[i, j, k] = 1 if k_th postman go through the path between i_th customer and j_th customer
                # x[i, j, k] = 0 vice versa    
                # 0 <= x[i, j, k] <= 1 with each any i, j, k
                x[i, j, k] = solver.IntVar(0, 1, f'x_{i}_{j}_{k}')

    for k in range(num_postman):
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
            solver.Sum(x[i, j, k] for j in range(num_customers) for k in range(num_postman)) == 1
        )
    for k in range(num_postman):
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
    
    for k in range(num_postman):
        for i in range(1, num_customers):
            for j in range(1, num_customers):
                # solver.Add(
                #     z[i, k] + 1 - (num_customers - 1) * ( 1- x[i, j, k]) <= z[j, k]
                # )
                if i == j: continue
                solver.Add(
                    z[i, k] - z[j, k] + num_customers * x[i, j, k] <= num_customers - 1
                )
    
    for k in range(num_postman):
        solver.Add(
            solver.Sum(x[i, j, k] * (transport_duration(customers_coord[i], customers_coord[j]) + receiving_time[j]) for i in range(num_customers) for j in range(num_customers)) <= res
        )
    solver.Minimize(res)
    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print("Total value = ", solver.Objective().Value())
        print(res.solution_value())
        for k in range(num_postman):
            print("postman: ", k)
            for i in range(num_customers):
                for j in range(num_customers):
                    if x[i, j, k].solution_value() == 1:
                        print(i, j, "Time: ", transport_duration(customers_coord[i], customers_coord[j]) + receiving_time[j])
        print('Time = ', solver.WallTime(), ' milliseconds')
    else:
        print('The problem does not have an optimal solution.')
    print("-----------------------------------------------------------")
def main():

    # customers_coord is the coordinate of custumer. The deliver time between 2 person is the distance euclean between them
    customers_coords = []
    # receiving_time is the time what customer receive item
    receiving_times = []

    num_postmans, customers_coords, receiving_times = get_data()

    for i in range(len(num_postmans)):
        solve(num_postmans[i], customers_coords[i], receiving_times[i])
    
if __name__ == '__main__':
    main()

