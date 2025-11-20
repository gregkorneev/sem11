#include <iostream>
#include <cstdlib>
#include <ctime>

#include "matrix_utils.h"
#include "strassen.h"

// Заполнение матрицы случайными числами 0..9
void fillRandom(Matrix &m) {
    int n = (int)m.size();
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            m[i][j] = std::rand() % 10;
        }
    }
}

int main() {
    std::cout << "Размер квадратных матриц n x n (n - степень двойки, например 2, 4, 8): ";
    int n;
    std::cin >> n;

    if (!isPowerOfTwo(n)) {
        std::cout << "Ошибка: для алгоритма Штрассена n должно быть степенью двойки."
                  << std::endl;
        std::cout << "Выберите другое n или дополняйте матрицы нулями." << std::endl;
        return 1;
    }

    // Инициализируем генератор случайных чисел
    std::srand((unsigned int)std::time(nullptr));

    Matrix A = createMatrix(n);
    Matrix B = createMatrix(n);

    // Генерируем случайные матрицы A и B
    fillRandom(A);
    fillRandom(B);

    printMatrix(A, "A (случайная матрица)");
    printMatrix(B, "B (случайная матрица)");

    // 1. Стандартное умножение
    Matrix C_standard = multiplyStandard(A, B);
    printMatrix(C_standard, "C (стандартное умножение)");

    // 2. Алгоритм Штрассена (с выводом M1..M7 и блоков C11..C22)
    std::cout << "=== Алгоритм Штрассена ===" << std::endl;
    Matrix C_strassen = strassenWithPrint(A, B);
    printMatrix(C_strassen, "C (алгоритм Штрассена)");

    // 3. Проверка совпадения результатов
    bool equal = true;
    for (int i = 0; i < n && equal; ++i) {
        for (int j = 0; j < n; ++j) {
            if (C_standard[i][j] != C_strassen[i][j]) {
                equal = false;
                break;
            }
        }
    }

    if (equal) {
        std::cout << "Результаты совпадают." << std::endl;
    } else {
        std::cout << "ВНИМАНИЕ: результаты НЕ совпадают." << std::endl;
    }

    return 0;
}
