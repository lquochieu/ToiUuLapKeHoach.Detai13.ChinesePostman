from FileController import FileController
import random
import copy
import OrtoolRouting
import time
#NeighborAlgorithm

x = []
t = []

n = 0
k = 0
numOfRounds = 3000

k, x, t = FileController.Read_File_Data('Data1.txt')

n = len(x) - 1

cost_per_postman = [0.0] * k
postman_position = [0] * k
customer_state = [False] * (n+1)
num_of_customer_free = n
customer_state[0] = True

postman_path = []
postman_path_new = []

def Get_Distance(p, q):
    s_sq_difference = 0
    for p_i,q_i in zip(p,q):
        s_sq_difference += (p_i - q_i)**2    
    distance = s_sq_difference**0.5
    return distance

def Get_Minimum_Postman():
    opt = cost_per_postman[0]
    index = 0
    for i in range(k):
        if cost_per_postman[i] < opt:
            opt = cost_per_postman[i]
            index = i
    return index

def Get_Optimal_Value(solution):
    global cost_per_postman
    opt = 0.0
    for i in range(k):
        cost_per_postman[i] = 0.0
        for j in range(len(solution[i])):
            if j < len(solution[i]) - 1:
                cost_per_postman[i] += Get_Distance(x[solution[i][j]], x[solution[i][j+1]]) + t[solution[i][j+1]]
        if opt < cost_per_postman[i]:
            opt = cost_per_postman[i]
    return round(opt,2)

def Get_Solution():
    global postman_path
    for i in range(k):
        print('Path of Postman ',i+1,' : ', postman_path[i])

def InitFisrtSolution(num):
    global postman_position, cost_per_postman, postman_path, customer_state
    while(num > 0):
        index_postman = Get_Minimum_Postman()
        minimum = 999999
        cost = cost_per_postman[index_postman]
        index = 0
        for i in range(n+1):
            if customer_state[i] == False:
                cost = cost_per_postman[index_postman] + Get_Distance(x[postman_position[index_postman]], x[i]) + t[i]
                if minimum > cost:
                    minimum = cost
                    index = i
        cost_per_postman[index_postman] = minimum
        postman_position[index_postman] = index
        postman_path[index_postman].append(index)      
        customer_state[index] = True
        num -= 1

    for i in range(k):
        cost_per_postman[i] += Get_Distance(x[postman_position[index_postman]], x[0])
        postman_path[i].append(0)
        
def NeighborAlgorithm_SwitchNode(greedy_path):
    global postman_path_new
    stimeGreed = time.time()
    curMin = Get_Optimal_Value(greedy_path)    
    tmp = 0
    for round in range(numOfRounds):
        postman_path_new = copy.deepcopy(greedy_path)

        postman = random.randint(0, k-1)
        if len(postman_path_new[postman]) < 3:
            continue
        firstPos = random.randint(1, len(postman_path_new[postman]) - 2)
        secondPos = random.randint(1, len(postman_path_new[postman]) - 2)

        tmp = postman_path_new[postman][firstPos]
        postman_path_new[postman][firstPos] = postman_path_new[postman][secondPos]
        postman_path_new[postman][secondPos] = tmp

        newMin = Get_Optimal_Value(postman_path_new)

        if newMin < curMin:
            curMin = newMin
            greedy_path = copy.deepcopy(postman_path_new)

    etimeNeighbor = time.time()
    print('Neighbor Switch Node: ', curMin, " in time: ", etimeNeighbor - stimeGreed, " [sec]")

def NeighborAlgorithm_SwitchArc(greedy_path):
    global postman_path_new
    stimeGreed = time.time()
    curMin = Get_Optimal_Value(greedy_path)    
    for round in range(numOfRounds):
        postman_path_new.clear()
        postman_path_new = copy.deepcopy(greedy_path)

        #Move
        postman = random.randint(0, k-1)
        if len(postman_path_new[postman]) < 3:
            continue
        firstPos = random.randint(1, len(postman_path_new[postman]) - 2)
        postman_2 = random.randint(0, k-1)
        if len(postman_path_new[postman_2]) < 3:
            continue
        secondPos = random.randint(1, len(postman_path_new[postman_2]) - 2)

        tmp = postman_path_new[postman][firstPos]
        postman_path_new[postman][firstPos] = postman_path_new[postman_2][secondPos]
        postman_path_new[postman_2][secondPos] = tmp

        newMin = Get_Optimal_Value(postman_path_new)

        if newMin < curMin:
            curMin = newMin
            greedy_path = copy.deepcopy(postman_path_new)

    etimeNeighbor = time.time()
    print('Neighbor Switch Arc: ', curMin, " in time: ", etimeNeighbor - stimeGreed, " [sec]")

def TabuSearch(greedy_path):
    global postman_path_new
    stimeGreed = time.time()    
    tabu_list = []
    tabu_list.append(greedy_path)
    best = Get_Optimal_Value(greedy_path)
    for round in range(200):

        #Tabu
        local_best = 999999
        has_other_solution = False
        next_tabu = []
        for m in range(100):
            #M Neighbor Solution
            postman_path_new.clear()
            postman_path_new = copy.deepcopy(greedy_path)

            postman = random.randint(0, k-1)
            if len(postman_path_new[postman]) < 3:
                continue
            firstPos = random.randint(1, len(postman_path_new[postman]) - 2)
            secondPos = random.randint(1, len(postman_path_new[postman]) - 2)

            tmp = postman_path_new[postman][firstPos]
            postman_path_new[postman][firstPos] = postman_path_new[postman][secondPos]
            postman_path_new[postman][secondPos] = tmp
            
            newMin = Get_Optimal_Value(postman_path_new)

            if postman_path_new in tabu_list:
                continue
            else:
                has_other_solution = True
                if local_best > newMin:
                    local_best = newMin
                    next_tabu = copy.deepcopy(postman_path_new)
        
        if has_other_solution:
            best = local_best
            tabu_list.append(next_tabu)
            greedy_path = copy.deepcopy(next_tabu)
        else:
            break
            #End Tabu

    etimeNeighbor = time.time()
    print('Tabu Search: ', best, " in time: ", etimeNeighbor - stimeGreed, " [sec]")

for i in range(27):
        s_time = time.time()

        path = 'Data' + str(i+1) + '.txt'
        k, x, t = FileController.Read_File_Data(path)

        n = len(x) - 1

        cost_per_postman = [0.0] * k
        postman_position = [0] * k
        customer_state = [False] * (n+1)
        num_of_customer_free = n
        customer_state[0] = True

        postman_path = []
        postman_path_new = []
        greedy_path = []

        for j in range(k):
            postman_path.append([0])

        print('File:',i+1)
        print('Num of customer:', n)
        print('Num of postman:', k)

        stime = time.time()
        InitFisrtSolution(num_of_customer_free)
        etime = time.time()
        greedy_path = copy.deepcopy(postman_path)    
        print("Greedy Algorithm: ", Get_Optimal_Value(greedy_path), " in time: ",etime - stime, " [sec]")   

        NeighborAlgorithm_SwitchNode(greedy_path)

        NeighborAlgorithm_SwitchArc(greedy_path)

        TabuSearch(greedy_path)

        OrtoolRouting.Solution(k, x, t)

        e_time = time.time()
        print("Run in: ", e_time - s_time, " [sec]")
        print('-----------------------------------------------------------')









