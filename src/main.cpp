
#include <iostream>

#include "matrix_utils.h"
#include "strassen.h"

int main() {
    std::cout << "Размер квадратных матриц n x n (n - степень двойки, например 2, 4, 8): ";
    int n;
    std::cin >> n;

    if (!isPowerOfTwo(n)) {
        std::cout << "Ошибка: для алгоритма Штрассена n должно быть степенью двойки." << std::endl;
        std::cout << "Вы можете выбрать другое n или дополнять матрицы нулями." << std::endl;
        return 1;
    }

    Matrix A = createMatrix(n);
    Matrix B = createMatrix(n);

    inputMatrix(A, "A");
    inputMatrix(B, "B");

    // 1. Стандартное умножение
    Matrix C_standard = multiplyStandard(A, B);
    printMatrix(C_standard, "C (стандартное умножение)");

    // 2. Алгоритм Штрассена
    std::cout << "=== Алгоритм Штрассена ===" << std::endl;
    Matrix C_strassen = strassenWithPrint(A, B);
    printMatrix(C_strassen, "C (алгоритм Штрассена)");

    // Простая проверка совпадения результатов
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
