from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import time

def Get_Distance(p, q):
    s_sq_difference = 0
    for p_i,q_i in zip(p,q):
        s_sq_difference += (p_i - q_i)**2    
    distance = s_sq_difference**0.5
    return distance

def create_data_model(_k, _x, _t):
    k, x, t = _k, _x, _t
    distance_matrix = []
    for i in range(len(x)):
        row_i = []
        for j in range(len(x)):
            dst = Get_Distance(x[i],x[j]) + t[j]
            row_i.append(dst)
        distance_matrix.append(row_i)

    data = {}
    data['distance_matrix'] = distance_matrix
    data['num_vehicles'] = k
    data['depot'] = 0
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    max_route_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Cost of the route: {}\n'.format(route_distance)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum of the route cost: {}'.format(max_route_distance))

def Get_Optimal_Value(data, manager, routing, solution, intime):
    """Prints solution on console."""
    max_route_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)        
        route_distance = 0
        while not routing.IsEnd(index):            
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)        
        max_route_distance = max(route_distance, max_route_distance)
    print("Ortool Routing: ", max_route_distance, " in time: ", round(intime, 5), " [sec]")

def Solution(_k, _x, _t):
    """Entry point of the program."""
    # Instantiate the data problem.
    stime = time.time()
    data = create_data_model(_k, _x, _t)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    etime = time.time()
    # Print solution on console.
    if solution:
        # print_solution(data, manager, routing, solution)
        Get_Optimal_Value(data, manager, routing, solution, etime - stime)
    else:
        print('No solution found !')

