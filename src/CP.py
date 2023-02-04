from FileController import FileController
import numpy as np
from ortools.sat.python import cp_model

def get_data():
    num_postman, customers_coords, receiving_times = FileController.Read_File_Data('../data/A-n32-k5.txt')

    return num_postman, customers_coords, receiving_times

def euclid_distance(a, b):
    ax, ay = a
    bx, by = b
    return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5

def solve(num_postman, customers_coords, receiving_times):
    # num postman
    k = num_postman

    # num customer 0, 1, ..., n - 1
    n = len(customers_coords)

    # receiving times
    d = receiving_times

    # duplicate start node n -> n + k - 1 = 0
    # duplicate end node n + k -> n + 2 * k - 1 = 0
    # cost matrix 
    c = np.zeros((n + 2 * k, n + 2 * k), dtype=int)

    # round base
    fix_base = 10

    for i in range(n + 2 * k):
        for j in range(n + 2 * k):
            u = customers_coords[i] if i < n else customers_coords[0]
            v = customers_coords[j] if j < n else customers_coords[0]
            t = receiving_times[i] if i < n else 0

            c[i][j] = round((euclid_distance(u, v) + t) * fix_base)
              
    model = cp_model.CpModel()

    # variable

    # R_i next node of i
    R = [model.NewIntVar(1, n + 2 * k - 1, f'R[{i}]') for i in range(0, n + k)]
    
    # S_i start node of postman i
    S = [model.NewIntVar(n, n + k - 1, f'S[{i}]') for i in range(k)]
    
    # E_i end node of postman i
    E = [model.NewIntVar(n + k, n + 2 * k - 1, f'E[{i}]') for i in range(k)]

    # C_i_j cost i -> j
    C = []
    for i in range(n + 2 * k):
        C.append([model.NewIntVar(c[i][j], c[i][j], f'C[{i}][{j}]') for j in range(n + 2 * k)])
    
    # Q_i total time 0 -> i
    Q = [model.NewIntVar(0, 10 **5, f'Q[{i}]') for i in range(0, n + 2 * k)]

    # T minimal ouput
    T = model.NewIntVar(0, 10 ** 5, 'T')

    # constrains

    # R_i != i
    for i in range(1, n + k):
        model.Add(R[i] != i)
    
    # R_i < n (i = n...n+k-1)
    for i in range(n, n + k):
        model.Add(R[i] < n)

    # R_i < n | >= n + k (i = 1...n - 1)
    for i in range(1, n):
        t = model.NewBoolVar(f"TMP_RANGE_R_{i}")
        model.Add(R[i] < n).OnlyEnforceIf(t)
        model.Add(R[i] >= n + k).OnlyEnforceIf(t.Not())
    
    # R different
    model.AddAllDifferent(R[1:])
    
    # S different
    model.AddAllDifferent(S)
    
    # E different
    model.AddAllDifferent(E)

    # Q_{R_i} = Q_i + C_i_R_i
    for i in range(1, n + k):
        cr = model.NewIntVar(0, 10 ** 5, f'TMP_CR_{i}')
        qr = model.NewIntVar(0, 10 ** 5, f'TMP_Q_{i}')
        # cr = C_i_R_i
        model.AddElement(R[i], C[i], cr)
        # qr = Q_{R_i}
        model.AddElement(R[i], Q, qr)
        model.Add(qr == Q[i] + cr)

    # T = max(Q[n+k -> n+2 * k - 1])
    model.AddMaxEquality(T, Q[n + k:])

    # solver problem
    model.Minimize(T)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds =  60
    status = solver.Solve(model)

    if(status == cp_model.OPTIMAL or status == cp_model.FEASIBLE):
        print(f"Optimal value: {solver.ObjectiveValue() / fix_base}")
        # for i in range(n + k):
        #     print(f"{i} --> {solver.Value(R[i])}")
        
        # for i in range(n + 2 * k):
        #     print(f"F{i}: {solver.Value(Q[i])}")
    else:
        print("No solution")
        
def main():
    num_postman, customers_coords, receiving_times = get_data()
    solve(num_postman, customers_coords, receiving_times)

if __name__ == '__main__':
    main()
