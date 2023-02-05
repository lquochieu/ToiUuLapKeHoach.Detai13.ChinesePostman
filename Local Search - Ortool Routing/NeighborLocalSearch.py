from FileController import FileController
import random
import copy
import OrtoolRouting
import time
import math
#NeighborAlgorithm

# x = []
# t = []

# n = 0
# k = 0
# numOfRounds = 3000

# k, x, t = FileController.Read_File_Data('Data1.txt')

# n = len(x) - 1

# cost_per_postman = [0.0] * k
# postman_position = [0] * k
# customer_state = [False] * (n+1)
# num_of_customer_free = n
# customer_state[0] = True

# postman_path = []
# postman_path_new = []

numOfRounds = 5000

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
        minimum = math.inf
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
        
def NeighborAlgorithm_2opt(greedy_path):
    global postman_path_new, numOfRounds
    curMin = Get_Optimal_Value(greedy_path)    
    tmp = 0
    nround = numOfRounds
    while nround > 0:
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
        
        nround -= 1

    return curMin

def NeighborAlgorithm_oropt(greedy_path):
    global postman_path_new, numOfRounds
    curMin = Get_Optimal_Value(greedy_path)    
    tmp = 0
    nround = numOfRounds
    while nround > 0:
        postman_path_new = copy.deepcopy(greedy_path)

        postman = random.randint(0, k-1)
        if len(postman_path_new[postman]) < 3:
            continue
        firstPos = random.randint(1, len(postman_path_new[postman]) - 2)
        secondPos = random.randint(1, len(postman_path_new[postman]) - 2)

        if secondPos == firstPos:
            continue

        if secondPos < firstPos:
            tmpp = firstPos
            firstPos = secondPos
            secondPos = tmpp

        tmp = postman_path_new[postman][firstPos]
        for ind in range(secondPos - firstPos):
            postman_path_new[postman][firstPos + ind] = postman_path_new[postman][firstPos + 1 + ind]
        postman_path_new[postman][secondPos] = tmp

        newMin = Get_Optimal_Value(postman_path_new)

        if newMin < curMin:
            curMin = newMin
            greedy_path = copy.deepcopy(postman_path_new)
        
        nround -= 1

    return curMin

def NeighborAlgorithm_CrossExchange(greedy_path):
    global postman_path_new, numOfRounds
    curMin = Get_Optimal_Value(greedy_path)    
    nround = numOfRounds
    while nround > 0:
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
        
        nround -= 1

    return curMin

def SimulatedAnnealing(greedy_path):
    T = 500.0
    alpha = 0.999
    epsilon = 0.001
    while T > epsilon:       

        postman_path_new = copy.deepcopy(greedy_path)

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

        delta_E = Get_Optimal_Value(greedy_path) - Get_Optimal_Value(postman_path_new)

        if delta_E > 0 or math.exp(delta_E / T) > random.uniform(0.0,1.0):    
            greedy_path = copy.deepcopy(postman_path_new)                  
        
        T = T * alpha

    return Get_Optimal_Value(greedy_path)


def TabuSearch(greedy_path):
    global postman_path_new   
    tabu_list = []
    tabu_list.append(greedy_path)
    best = Get_Optimal_Value(greedy_path)
    for nround in range(100):

        #Tabu
        local_best = math.inf
        has_other_solution = False
        next_tabu = []
        for ite in range(500):
            #M Neighbor Solution
            postman_path_new.clear()
            postman_path_new = copy.deepcopy(greedy_path)

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

    return best


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

    print("File: A-n{}-k{}".format(n+1,k))
    print('Num of customer:', n)
    print('Num of postman:', k)

    stime = time.time()
    InitFisrtSolution(num_of_customer_free)
    etime = time.time()
    greedy_path = copy.deepcopy(postman_path) 
        
    print(">>")
    print("Greedy Algorithm: ", Get_Optimal_Value(greedy_path), " in time: ",round(etime - stime, 5), " [sec]") 

    print(">>")
    stime = time.time()
    opt = math.inf
    for check in range(10):
        val = NeighborAlgorithm_2opt(greedy_path)
        if opt > val:
            opt = val
    etime = time.time()
    print("Neighbor 2_opt: ", opt, " in time: ", round(etime - stime, 5), " [sec]")

    print(">>")
    stime = time.time()
    opt = math.inf
    for check in range(10):
        val = NeighborAlgorithm_oropt(greedy_path)
        if opt > val:
            opt = val
    etime = time.time()
    print("Neighbor or_opt: ", opt, " in time: ", round(etime - stime, 5), " [sec]")
    # NeighborAlgorithm_oropt(greedy_path)

    print(">>")
    stime = time.time()
    opt = math.inf
    for check in range(10):
        val = NeighborAlgorithm_CrossExchange(greedy_path)
        if opt > val:
            opt = val
    etime = time.time()
    print("Neighbor Cross Exchange: ", opt, " in time: ", round(etime - stime, 5), " [sec]")
    # NeighborAlgorithm_CrossExchange(greedy_path)

    print(">>")
    stime = time.time()
    opt = math.inf
    for check in range(10):
        val = SimulatedAnnealing(greedy_path)
        if opt > val:
            opt = val
    etime = time.time()
    print("Simulated Annealing: ", opt, " in time: ", round(etime - stime, 5), " [sec]")
    # SimulatedAnnealing(greedy_path)

    print(">>")
    stime = time.time()
    opt = math.inf
    for check in range(10):
        val = TabuSearch(greedy_path)
        if opt > val:
            opt = val
    etime = time.time()
    print("Tabu Search: ", opt, " in time: ", round(etime - stime, 5), " [sec]")
    # TabuSearch(greedy_path)

    # print(">>")
    # OrtoolRouting.Solution(k, x, t)

    e_time = time.time()
    print("Run in: ", round(e_time - s_time, 5), " [sec]")
    print('-----------------------------------------------------------')









