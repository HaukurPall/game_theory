from hw5 import VCG
import matplotlib.pyplot as plt
import time

def plot_line_graph(x, y, y_name, x_name):
    """
    Helper function
    """
    plt.plot(x, y)
    plt.ylabel(y_name)
    plt.xlabel(x_name)
    #plt.xscale('log')
    plt.savefig(x_name + y_name + '.png')
    plt.clf()

def main():
    N = [10, 12, 14, 16, 18, 20]
    N_times = []
    G = [10, 20, 30, 40, 50, 60]
    G_times = []
    for n in N:
        auction = VCG.VCG(N=n, G=10)
        auction.reset()
        start= time.clock()
        auction.naive_allocation()
        end= time.clock()
        N_times.append((end-start))
    plot_line_graph(N, N_times, 'run-time(seconds)', 'N')
    for g in G:
        auction = VCG.VCG(N=10, G=g)
        auction.reset()
        start= time.clock()
        auction.naive_allocation()
        end= time.clock()
        G_times.append((end-start))
    plot_line_graph(G, G_times, 'run-time(seconds)', 'G')


if __name__ == "__main__":
    main()
