#include "strassen.h"
#include <iostream>

// Рекурсивная функция Штрассена (без печати)
Matrix strassenRec(const Matrix &A, const Matrix &B) {
    int n = (int)A.size();

    // Базовый случай: матрица 1x1
    if (n == 1) {
        return multiplyStandard(A, B);
    }

    int k = n / 2;

    Matrix A11, A12, A21, A22;
    Matrix B11, B12, B21, B22;

    splitMatrix(A, A11, A12, A21, A22);
    splitMatrix(B, B11, B12, B21, B22);

    Matrix M1 = strassenRec(addMatrix(A11, A22), addMatrix(B11, B22));
    Matrix M2 = strassenRec(addMatrix(A21, A22), B11);
    Matrix M3 = strassenRec(A11, subMatrix(B12, B22));
    Matrix M4 = strassenRec(A22, subMatrix(B21, B11));
    Matrix M5 = strassenRec(addMatrix(A11, A12), B22);
    Matrix M6 = strassenRec(subMatrix(A21, A11), addMatrix(B11, B12));
    Matrix M7 = strassenRec(subMatrix(A12, A22), addMatrix(B21, B22));

    Matrix C11 = addMatrix(subMatrix(addMatrix(M1, M4), M5), M7);
    Matrix C12 = addMatrix(M3, M5);
    Matrix C21 = addMatrix(M2, M4);
    Matrix C22 = addMatrix(subMatrix(addMatrix(M1, M3), M2), M6);

    Matrix C = joinMatrix(C11, C12, C21, C22);
    return C;
}

// Верхний уровень: вывод M1..M7 и C11..C22
Matrix strassenWithPrint(const Matrix &A, const Matrix &B) {
    int n = (int)A.size();

    if (n < 2) {
        std::cout << "Размер матриц слишком мал для разбиения на блоки (n < 2)."
                  << std::endl;
        return multiplyStandard(A, B);
    }

    int k = n / 2;

    Matrix A11, A12, A21, A22;
    Matrix B11, B12, B21, B22;

    splitMatrix(A, A11, A12, A21, A22);
    splitMatrix(B, B11, B12, B21, B22);

    Matrix M1 = strassenRec(addMatrix(A11, A22), addMatrix(B11, B22));
    Matrix M2 = strassenRec(addMatrix(A21, A22), B11);
    Matrix M3 = strassenRec(A11, subMatrix(B12, B22));
    Matrix M4 = strassenRec(A22, subMatrix(B21, B11));
    Matrix M5 = strassenRec(addMatrix(A11, A12), B22);
    Matrix M6 = strassenRec(subMatrix(A21, A11), addMatrix(B11, B12));
    Matrix M7 = strassenRec(subMatrix(A12, A22), addMatrix(B21, B22));

    printMatrix(M1, "M1");
    printMatrix(M2, "M2");
    printMatrix(M3, "M3");
    printMatrix(M4, "M4");
    printMatrix(M5, "M5");
    printMatrix(M6, "M6");
    printMatrix(M7, "M7");

    Matrix C11 = addMatrix(subMatrix(addMatrix(M1, M4), M5), M7);
    Matrix C12 = addMatrix(M3, M5);
    Matrix C21 = addMatrix(M2, M4);
    Matrix C22 = addMatrix(subMatrix(addMatrix(M1, M3), M2), M6);

    printMatrix(C11, "C11");
    printMatrix(C12, "C12");
    printMatrix(C21, "C21");
    printMatrix(C22, "C22");

    Matrix C = joinMatrix(C11, C12, C21, C22);
    return C;
}
