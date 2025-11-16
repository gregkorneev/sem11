#ifndef STRASSEN_H
#define STRASSEN_H

#include "matrix_utils.h"

// Рекурсивная реализация алгоритма Штрассена (без вывода промежуточных матриц)
Matrix strassenRec(const Matrix &A, const Matrix &B);

// Реализация Штрассена для верхнего уровня:
// считает те же шаги, но печатает M1..M7 и блоки C11..C22
Matrix strassenWithPrint(const Matrix &A, const Matrix &B);

#endif // STRASSEN_H
