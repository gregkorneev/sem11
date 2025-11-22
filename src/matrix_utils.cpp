#include "matrix_utils.h"
#include <iostream>
#include <iomanip>

Matrix createMatrix(int n) {
    return Matrix(n, std::vector<double>(n, 0.0));
}

void inputMatrix(Matrix &m, const std::string &name) {
    int n = (int)m.size();
    std::cout << "Введите элементы матрицы " << name
              << " (" << n << " x " << n << "):" << std::endl;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            std::cin >> m[i][j];
        }
    }
}

void printMatrix(const Matrix &m, const std::string &name) {
    int n = (int)m.size();
    std::cout << name << ":" << std::endl;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            std::cout << std::setw(8) << m[i][j] << " ";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

Matrix addMatrix(const Matrix &A, const Matrix &B) {
    int n = (int)A.size();
    Matrix C = createMatrix(n);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            C[i][j] = A[i][j] + B[i][j];
        }
    }
    return C;
}

Matrix subMatrix(const Matrix &A, const Matrix &B) {
    int n = (int)A.size();
    Matrix C = createMatrix(n);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            C[i][j] = A[i][j] - B[i][j];
        }
    }
    return C;
}

void splitMatrix(const Matrix &A,
                 Matrix &A11, Matrix &A12,
                 Matrix &A21, Matrix &A22) {
    int n = (int)A.size();
    int k = n / 2;

    A11 = createMatrix(k);
    A12 = createMatrix(k);
    A21 = createMatrix(k);
    A22 = createMatrix(k);

    for (int i = 0; i < k; ++i) {
        for (int j = 0; j < k; ++j) {
            A11[i][j] = A[i][j];
            A12[i][j] = A[i][j + k];
            A21[i][j] = A[i + k][j];
            A22[i][j] = A[i + k][j + k];
        }
    }
}

Matrix joinMatrix(const Matrix &C11, const Matrix &C12,
                  const Matrix &C21, const Matrix &C22) {
    int k = (int)C11.size();
    int n = 2 * k;
    Matrix C = createMatrix(n);

    for (int i = 0; i < k; ++i) {
        for (int j = 0; j < k; ++j) {
            C[i][j]         = C11[i][j];
            C[i][j + k]     = C12[i][j];
            C[i + k][j]     = C21[i][j];
            C[i + k][j + k] = C22[i][j];
        }
    }

    return C;
}

Matrix multiplyStandard(const Matrix &A, const Matrix &B) {
    int n = (int)A.size();
    Matrix C = createMatrix(n);

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            double sum = 0.0;
            for (int k = 0; k < n; ++k) {
                sum += A[i][k] * B[k][j];
            }
            C[i][j] = sum;
        }
    }

    return C;
}

bool isPowerOfTwo(int n) {
    if (n <= 0) {
        return false;
    }
    return (n & (n - 1)) == 0;
}
