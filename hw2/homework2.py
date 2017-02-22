import math
def a_1():
    for n in range(1, 201):
        sum = 0
        for k in range(1, 200-n):
            sum += math.sqrt(k)
        p = -(10*n + sum)
        print("n={},{}: {}".format(n, 200-n,p))
#a_1()

def sw(n, max=200):
    return -(n*10+(200-n)*math.sqrt(200-n))

#print(2000.0/1851.87)

def a_1_iteratively_adding():
    sum = 0.0
    n_r_1 = 0
    n_r_2 = 0
    for n in range(0, 200):
        r_1 = -1*10.0
        r_2 = -math.sqrt(n_r_2 + 1)
        if r_1 > r_2:
            n_r_1 += 1
            sum += r_1
        elif r_1 < r_2:
            n_r_2 += 1
            sum += r_2
        else:
            n_r_1 += 1
            sum += r_1
            # we just take r_1
            print("I'm divergent! n_r_1={}, n_r_2={}: sum={}", n_r_1, n_r_2, sum)
    print("n_r_1={}, n_r_2={}: sum={}", n_r_1, n_r_2, sum)

#a_1_iteratively_adding()


def recursive_p_function(n_r_1, n_r_2, n, r_1, r_2, sum):
    if n_r_1 + n_r_2 == n:
        print("r1:{}, r2:{}, sum:{}".format(n_r_1, n_r_2, sum))
        return
    utility_r1 = r_1(n_r_1)
    utility_r2 = r_2(n_r_2)
    if utility_r1 < utility_r2:
        recursive_p_function(n_r_1, n_r_2+1, n, r_1, r_2, sum+utility_r2)
    elif utility_r1 > utility_r2:
        recursive_p_function(n_r_1+1, n_r_2, n, r_1, r_2, sum+utility_r1)
    else:
        print("Diverging")
        recursive_p_function(n_r_1, n_r_2+1, n, r_1, r_2, sum+utility_r2)
        recursive_p_function(n_r_1+1, n_r_2, n, r_1, r_2, sum+utility_r1)


r_1 = lambda x: -10
r_2 = lambda x: -math.sqrt(x+1)

recursive_p_function(0, 0, 200, r_1, r_2, 0.0)