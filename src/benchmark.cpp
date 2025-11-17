#include <iostream>
#include <fstream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <chrono>

#include "matrix_utils.h"
#include "strassen.h"

// Заполнение матрицы случайными числами
void fillRandom(Matrix &m) {
    int n = (int)m.size();
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            // простые небольшие значения, чтобы числа не росли слишком сильно
            m[i][j] = std::rand() % 10;
        }
    }
}

// Замер времени выполнения переданной функции умножения
template <typename Func>
double measureTime(Func f, const Matrix &A, const Matrix &B) {
    auto start = std::chrono::high_resolution_clock::now();
    Matrix C = f(A, B);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double, std::milli> ms = end - start;
    return ms.count(); // миллисекунды
}

int main() {
    std::srand((unsigned int)std::time(nullptr));

    // Размеры матриц, для которых будем мерить время (степени двойки)
    std::vector<int> sizes = {2, 4, 8, 16, 32};

    std::ofstream fout("timings.csv");
    if (!fout.is_open()) {
        std::cout << "Не удалось открыть файл timings.csv для записи." << std::endl;
        return 1;
    }

    // Заголовок CSV
    fout << "n,standard_ms,strassen_ms\n";

    std::cout << "Запуск бенчмарка..." << std::endl;

    for (int n : sizes) {
        std::cout << "Размер n = " << n << std::endl;

        Matrix A = createMatrix(n);
        Matrix B = createMatrix(n);

        fillRandom(A);
        fillRandom(B);

        // Замер стандартного умножения
        double t_std = measureTime(multiplyStandard, A, B);

        // Замер Штрассена
        double t_strassen = measureTime(strassenRec, A, B);

        // Запись в CSV
        fout << n << "," << t_std << "," << t_strassen << "\n";

        std::cout << "  standard:  " << t_std << " ms\n";
        std::cout << "  strassen:  " << t_strassen << " ms\n";
    }

    fout.close();
    std::cout << "Готово. Данные записаны в timings.csv" << std::endl;

    return 0;
}
