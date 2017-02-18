def a_1():
    import math
    for n in range(1, 201):
        sum = 0
        for k in range(0, 200-n):
            sum += math.sqrt(k)
        p = 10*n + sum
        print("n={}: {}".format(n,p))