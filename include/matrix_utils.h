#ifndef MATRIX_UTILS_H
#define MATRIX_UTILS_H

#include <vector>
#include <string>

typedef std::vector<std::vector<double> > Matrix;

// Создание квадратной матрицы n x n, заполненной нулями
Matrix createMatrix(int n);

// Ввод матрицы с клавиатуры
void inputMatrix(Matrix &m, const std::string &name);

// Вывод матрицы на экран
void printMatrix(const Matrix &m, const std::string &name);

// Сложение и вычитание матриц одинакового размера
Matrix addMatrix(const Matrix &A, const Matrix &B);
Matrix subMatrix(const Matrix &A, const Matrix &B);

// Разбиение квадратной матрицы A на 4 блока одинакового размера
void splitMatrix(const Matrix &A,
                 Matrix &A11, Matrix &A12,
                 Matrix &A21, Matrix &A22);

// Сборка 4 блоков в одну квадратную матрицу
Matrix joinMatrix(const Matrix &C11, const Matrix &C12,
                  const Matrix &C21, const Matrix &C22);

// Стандартное умножение матриц O(n^3)
Matrix multiplyStandard(const Matrix &A, const Matrix &B);

// Проверка: является ли n степенью двойки
bool isPowerOfTwo(int n);

#endif // MATRIX_UTILS_H
