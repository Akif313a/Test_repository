import numpy as np
import matplotlib.pyplot as plt

class TravelingSalesman:
    def __init__(self, num_cities, min_coord, max_coord):
        self.num_cities = num_cities
        self.min_coord = min_coord
        self.max_coord = max_coord
        self.X = np.array([7, 19, 40, 40, 60, 77, 79, 85, 95, 100])
        self.Y = np.array([20, 33, 30, 54, 47, 55, 81, 80, 94, 100])
        self.S = np.arange(num_cities)
        np.random.shuffle(self.S)

    def calculate_distance(self, order):
        total_distance = 0
        for i in range(len(order) - 1):
            total_distance += np.sqrt((self.X[order[i+1]] - self.X[order[i]])**2 + (self.Y[order[i+1]] - self.Y[order[i]])**2)
        total_distance += np.sqrt((self.X[order[0]] - self.X[order[-1]])**2 + (self.Y[order[0]] - self.Y[order[-1]])**2)
        return total_distance

    def swap_cities(self, order):
        new_order = order.copy()
        idx1, idx2 = np.random.choice(len(order)-1, 2, replace=False)
        new_order[idx1:idx2+1] = np.flipud(new_order[idx1:idx2+1])
        return new_order

    def cool_down(self, t_max, k):
        return 0.1 * t_max / k

    def acceptance_probability(self, e_cur, e_next, t):
        return np.exp((e_cur - e_next) / t)

    def minimize_path(self, t_max, t_min, k_max):
        t = t_max
        e_cur = self.calculate_distance(self.S)
        k = 1
        while t > t_min and k < k_max:
            S_new = self.swap_cities(self.S)
            e_new = self.calculate_distance(S_new)
            if e_new <= e_cur or np.random.rand() <= self.acceptance_probability(e_cur, e_new, t):
                self.S = S_new
                e_cur = e_new
            t = self.cool_down(t_max, k)
            k += 1
        return e_cur, k, self.S

    def plot_path(self, order):
        plt.plot(self.X[order], self.Y[order], '-*')
        plt.title(f"Total Distance: {self.calculate_distance(order):.6f}")
        plt.show()

if __name__ == "__main__":
    num_cities = 20
    min_coord, max_coord = 0, 10
    t_max = 1000
    t_min = 0.001
    k_max = 1000000

    datasets = [10,] 
    runs = 5  

    all_results = []

    for dataset in datasets:
        for _ in range(runs):
            salesman = TravelingSalesman(dataset, min_coord, max_coord)
            print(f"Initial Order: {salesman.S}\nInitial Distance: {salesman.calculate_distance(salesman.S):.6f}")

            for i in range(3):
                total_distance, iterations, optimal_order = salesman.minimize_path(t_max, t_min, k_max)
                print(f"Iteration {i+1} - Total Distance: {total_distance:.6f}, Iterations: {iterations}, Optimal order: {optimal_order}")
                all_results.append((dataset, total_distance, iterations, optimal_order))
                salesman.plot_path(optimal_order)