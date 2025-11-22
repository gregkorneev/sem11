import csv
import os
import matplotlib.pyplot as plt

DATA_DIR = "data"
CSV_DIR = os.path.join(DATA_DIR, "csv")
PNG_DIR = os.path.join(DATA_DIR, "png")


def ensure_dirs():
    os.makedirs(CSV_DIR, exist_ok=True)
    os.makedirs(PNG_DIR, exist_ok=True)


def read_timings_cpp(filename):
    n_values = []
    t_std = []
    t_strassen = []

    path = os.path.join(CSV_DIR, filename)
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            n_values.append(int(row["n"]))
            t_std.append(float(row["standard_ms"]))
            t_strassen.append(float(row["strassen_ms"]))

    return n_values, t_std, t_strassen


def read_timings_numpy(filename):
    """Читаем результаты бенчмарка NumPy из data/csv."""
    path = os.path.join(CSV_DIR, filename)
    timings = {}
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            n = int(row["n"])
            t_np = float(row["numpy_ms"])
            timings[n] = t_np
    return timings


def main():
    ensure_dirs()

    cpp_filename = "timings.csv"
    numpy_filename = "timings_numpy.csv"

    # ---- C++ данные ----
    try:
        n_values, t_std, t_strassen = read_timings_cpp(cpp_filename)
    except FileNotFoundError:
        print(
            f"Не найден {os.path.join(CSV_DIR, cpp_filename)}. "
            "Сначала запусти C++ benchmark и benchmark_numpy.py."
        )
        return

    # ---- NumPy данные ----
    t_numpy = None
    try:
        numpy_timings = read_timings_numpy(numpy_filename)
        t_numpy = [numpy_timings.get(n, None) for n in n_values]
    except FileNotFoundError:
        print(
            f"Внимание: файл {os.path.join(CSV_DIR, numpy_filename)} "
            "не найден. График NumPy построен не будет."
        )

    # ---------- График 1: общий (линейный) ----------
    fig_all = plt.figure()
    plt.plot(n_values, t_std, marker="o",
             label="Стандартный алгоритм C++ (O(n^3))")
    plt.plot(n_values, t_strassen, marker="o",
             label="Алгоритм Штрассена C++ (O(n^{log2 7}))")
    if t_numpy is not None and any(v is not None for v in t_numpy):
        plt.plot(n_values, t_numpy, marker="o",
                 label="NumPy (np.dot / @)")

    plt.xlabel("Размер матрицы n (n x n)")
    plt.ylabel("Время, мс")
    plt.title("Сравнение времени работы алгоритмов умножения матриц")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    all_path = os.path.join(PNG_DIR, "timings_all.png")
    fig_all.savefig(all_path, dpi=200)
    print(f"Сохранён общий график (линейный): {all_path}")

    # ---------- График 1b: общий (лог-лог) ----------
    if all(v > 0 for v in t_std + t_strassen if v is not None) and \
       (t_numpy is None or all((v is None or v > 0) for v in t_numpy)):
        fig_all_log = plt.figure()
        plt.plot(n_values, t_std, marker="o",
                 label="Стандартный алгоритм C++ (O(n^3))")
        plt.plot(n_values, t_strassen, marker="o",
                 label="Алгоритм Штрассена C++ (O(n^{log2 7}))")
        if t_numpy is not None and any(v is not None for v in t_numpy):
            plt.plot(n_values, t_numpy, marker="o",
                     label="NumPy (np.dot / @)")

        plt.xscale("log")
        plt.yscale("log")

        plt.xlabel("Размер матрицы n (n x n), лог. шкала")
        plt.ylabel("Время, мс, лог. шкала")
        plt.title("Сравнение времени работы (лог-лог масштаб)")
        plt.grid(True, which="both")
        plt.legend()
        plt.tight_layout()

        all_log_path = os.path.join(PNG_DIR, "timings_all_loglog.png")
        fig_all_log.savefig(all_log_path, dpi=200)
        print(f"Сохранён общий график (лог-лог): {all_log_path}")
    else:
        print("Не удалось построить лог-лог график: есть нулевые значения.")

    # ---------- График 2: только стандартный ----------
    fig_std = plt.figure()
    plt.plot(n_values, t_std, marker="o",
             label="Стандартный алгоритм C++ (O(n^3))")
    plt.xlabel("Размер матрицы n (n x n)")
    plt.ylabel("Время, мс")
    plt.title("Время работы стандартного алгоритма C++")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    std_path = os.path.join(PNG_DIR, "timings_standard.png")
    fig_std.savefig(std_path, dpi=200)
    print(f"Сохранён график стандартного алгоритма: {std_path}")

    # ---------- График 3: только Штрассен ----------
    fig_str = plt.figure()
    plt.plot(n_values, t_strassen, marker="o",
             label="Алгоритм Штрассена C++ (O(n^{log2 7}))")
    plt.xlabel("Размер матрицы n (n x n)")
    plt.ylabel("Время, мс")
    plt.title("Время работы алгоритма Штрассена C++")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    str_path = os.path.join(PNG_DIR, "timings_strassen.png")
    fig_str.savefig(str_path, dpi=200)
    print(f"Сохранён график Штрассена: {str_path}")

    # ---------- График 4: только NumPy (если есть данные) ----------
    if t_numpy is not None and any(v is not None for v in t_numpy):
        fig_np = plt.figure()
        plt.plot(n_values, t_numpy, marker="o",
                 label="NumPy (np.dot / @)")
        plt.xlabel("Размер матрицы n (n x n)")
        plt.ylabel("Время, мс")
        plt.title("Время работы умножения матриц в NumPy")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        np_path = os.path.join(PNG_DIR, "timings_numpy.png")
        fig_np.savefig(np_path, dpi=200)
        print(f"Сохранён график NumPy: {np_path}")

    # Если хочешь показать окна:
    # plt.show()


if __name__ == "__main__":
    main()
