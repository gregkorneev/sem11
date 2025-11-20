import numpy as np
import time


def print_matrix(m, name):
    print(f"{name}:")
    for row in m:
        for x in row:
            print(f"{x:8.2f}", end=" ")
        print()
    print()


def main():
    n = int(input("Введите размер квадратных матриц n x n: "))

    # Для иллюстрации можно вводить матрицы руками (закомментировано).
    # Сейчас используем случайные матрицы, чтобы проще оценивать время.
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)

    print_matrix(A, "A (NumPy)")
    print_matrix(B, "B (NumPy)")

    start = time.perf_counter()
    C = np.dot(A, B)     # или: C = A @ B, или np.matmul(A, B)
    end = time.perf_counter()

    print_matrix(C, "C = A * B (NumPy)")
    print(f"Время умножения (NumPy): {end - start:.6f} с")


if __name__ == "__main__":
    main()
