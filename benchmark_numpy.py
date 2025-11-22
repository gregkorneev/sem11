# benchmark_numpy.py
import csv
import time
import os
import shutil
import numpy as np

DATA_DIR = "data"
CSV_DIR = os.path.join(DATA_DIR, "csv")
PNG_DIR = os.path.join(DATA_DIR, "png")


def ensure_dirs():
    """Создаём папки data/, data/csv/, data/png/ при необходимости."""
    os.makedirs(CSV_DIR, exist_ok=True)
    os.makedirs(PNG_DIR, exist_ok=True)


def ensure_cpp_csv() -> str:
    """
    Гарантируем, что timings.csv от C++ лежит в data/csv/.
    Если файл лежит в корне проекта — переносим его туда.
    Возвращаем путь к файлу.
    """
    data_path = os.path.join(CSV_DIR, "timings.csv")
    root_path = "timings.csv"

    if os.path.exists(data_path):
        return data_path

    if os.path.exists(root_path):
        ensure_dirs()
        shutil.move(root_path, data_path)
        print(f"Перенёс {root_path} -> {data_path}")
        return data_path

    raise FileNotFoundError(
        "Не найден timings.csv. "
        "Сначала запусти C++ benchmark (./benchmark)."
    )


def read_n_values_from_cpp() -> list[int]:
    """Читаем размеры n из C++-бенчмарка (уже внутри data/csv)."""
    path = ensure_cpp_csv()
    n_values: list[int] = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            n_values.append(int(row["n"]))
    return n_values


def measure_numpy(n: int, repeats: int = 3) -> float:
    """
    Замеряем время умножения двух случайных матриц n x n с помощью NumPy.
    Возвращаем среднее время (мс) по нескольким запускам.
    """
    times = []
    for _ in range(repeats):
        A = np.random.rand(n, n)
        B = np.random.rand(n, n)

        start = time.perf_counter()
        _ = A @ B           # или np.dot(A, B)
        end = time.perf_counter()

        times.append((end - start) * 1000.0)

    return sum(times) / len(times)


def main():
    ensure_dirs()

    try:
        n_values = read_n_values_from_cpp()
    except FileNotFoundError as e:
        print(e)
        return

    out_filename = os.path.join(CSV_DIR, "timings_numpy.csv")
    with open(out_filename, "w", newline="") as f:
        fieldnames = ["n", "numpy_ms"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for n in n_values:
            print(f"Замер NumPy для n = {n} ...")
            t_np = measure_numpy(n)
            writer.writerow({"n": n, "numpy_ms": t_np})
            print(f"  numpy: {t_np:.3f} ms")

    print(f"Готово. Данные NumPy записаны в {out_filename}")


if __name__ == "__main__":
    main()
