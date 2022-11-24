import numpy as np

# p: vector de prices
# w: vector de weights
# c: max capacity
def knapsack_dynamic_programming(p, w, c):
    n = len(p)
    z = np.zeros((n, c+1))
    A = np.zeros((n, c+1))
    for j in range(n):
        for d in range(c+1):
            if(w[j] > d): 
                z[j,d] = z[j-1,d]
            else: 
                z[j,d] = max(z[j-1,d], p[j] + z[j-1,d-w[j]])
                
            if(z[j,d] != z[j-1,d]): A[j,d] = 1
    
    selected = np.zeros(n)
    for j in range(n-1,-1,-1):
        selected[j] = A[j,c]
        if(selected[j] == 1) : c -= w[j] 
        
    max_price = z[-1,-1]
    
    return max_price, selected

def knapsack_greedy(p, w, c):
    ratio_values = p/w
    idx_ordered = np.argsort(ratio_values)[::-1]
    idx_back = np.argsort(idx_ordered)
    p = p[idx_ordered]
    w = w[idx_ordered]
    
    j = 0
    max_price = 0
    selected = np.zeros(len(p))
    while(j < n and w[j] < c):
        selected[j] = 1
        max_price += p[j]
        c -= w[j]
        j += 1
    
    selected = selected[idx_back] 
    
    return max_price, selected

def knapsack_branchbound(p, w, c):
    ratio_values = p/w
    idx_ordered = np.argsort(ratio_values)[::-1]
    idx_back = np.argsort(idx_ordered)
    p = p[idx_ordered]
    w = w[idx_ordered]
    
    s, l, z_best, s_best = np.zeros(len(p)), 0, 0, np.zeros(len(p))
    z_best, s_best = knapsack_branchbound_rec(p, w, c, s, l, z_best, s_best)
    s_best = s_best[idx_back]
    
    return z_best, s_best

def update_best_and_bound(p, w, c, s, l):
    s[l:] = np.zeros(len(p) - l)
    z = np.dot(p[:l], s[:l])
    c -= np.dot(w[:l], s[:l])
    if(c < 0): z, bound = 0, 0
    else:
        j, n = l, len(p)
        while(j < n and w[j] < c):
            s[j] = 1
            z += p[j]
            c -= w[j]
            j += 1
        bound = z
        if(j < n): bound += p[j] * c/w[j] 
    return z, bound, s

def knapsack_branchbound_rec(p, w, c, s, l, z_best, s_best): 
    z, bound, s = update_best_and_bound(p, w, c, s, l)
    if(z > z_best):
        z_best = z
        s_best = s.copy()
             
    if(l < len(p)):
        if(z_best <= bound):
            s[l] = 1
            z_best0, s_best0 = knapsack_branchbound_rec(p, w, c, s, l+1, z_best, s_best)
            if(z_best0 > z_best): z_best, s_best = z_best0, s_best0.copy()
            s[l] = 0
            z_best1, s_best1 = knapsack_branchbound_rec(p, w, c, s, l+1, z_best, s_best)
            if(z_best1 > z_best): z_best, s_best = z_best1, s_best1.copy()
    
    return z_best, s_best
    

n = 6  # No. items
p = np.random.randint(5, 100, n) # Quetzales
w = np.random.randint(5, 50, n)  # Libras
c = 100 # Max libras

max_price1, selected1 = knapsack_greedy(p, w, c)
max_price2, selected2 = knapsack_dynamic_programming(p, w, c)
max_price3, selected3 = knapsack_branchbound(p, w, c)

print('=== Knapsack Problem ===')
print('Precios:', p)
print('Weights:', w)
print('Capacity:', c)

print('\n=== Greedy ===\nPrecio max:', max_price1, 
      '\nPeso sol.:', np.dot(w,selected1),'\nSeleccion:',selected1)
print('=== Dynamic Programming ===\nPrecio max:', max_price2, 
      '\nPeso sol.:', np.dot(w,selected2), '\nSeleccion:',selected2)
print('=== Branch & Bound ===\nPrecio max:', max_price3, 
      '\nPeso sol.:', np.dot(w,selected3),'\nSeleccion:',selected3)



    
    