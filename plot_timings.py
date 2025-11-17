import csv
import matplotlib.pyplot as plt

def read_timings(filename):
    n_values = []
    t_std = []
    t_strassen = []

    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            n = int(row["n"])
            n_values.append(n)
            t_std.append(float(row["standard_ms"]))
            t_strassen.append(float(row["strassen_ms"]))

    return n_values, t_std, t_strassen


def main():
    filename = "timings.csv"
    n_values, t_std, t_strassen = read_timings(filename)

    # график времени от размера n
    plt.figure()
    plt.plot(n_values, t_std, marker="o", label="Стандартный алгоритм (O(n^3))")
    plt.plot(n_values, t_strassen, marker="o", label="Алгоритм Штрассена (O(n^{log2 7}))")
    plt.xlabel("Размер матрицы n (n x n)")
    plt.ylabel("Время, мс")
    plt.title("Сравнение времени работы алгоритмов умножения матриц")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("timings_plot.png", dpi=200)
    plt.show()


if __name__ == "__main__":
    main()
