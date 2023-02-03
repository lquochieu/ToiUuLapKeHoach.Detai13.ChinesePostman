from FileController import FileController
#GreedyAlgorithm

x = []
t = []

n = 0
k = 0

k, x, t = FileController.Read_File_Data()
print(x)
n = len(x) - 1

cost_per_postman = [0.0] * k
postman_position = [0] * k
customer_state = [False] * (n+1)
num_of_customer_free = n
customer_state[0] = True

postman_path = []

for i in range(k):
    postman_path.append([0])

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

def OptimalValue():
    opt = cost_per_postman[0]
    for i in range(k):
        if cost_per_postman[i] > opt:
            opt = cost_per_postman[i]
    return round(opt,2)


def GreedyAlgorithm(num):
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
        print('Path of postman ', i, ' : ', postman_path[i])
    
    print("Optimal Value: ", OptimalValue())


GreedyAlgorithm(num_of_customer_free)



