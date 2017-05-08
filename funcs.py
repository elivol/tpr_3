import numpy as np


def preference(matrix):

    row = matrix.shape[0]
    col = matrix.shape[1]
    M = row

    # Преобразование матрицы
    matrix = np.array([[M-el for el in row] for row in matrix])

    # Нахождение суммы оценок (сумма по строкам)
    sum_of_ev = np.array(matrix.sum(1))

    # Нахождение коэффициентов важности
    c_importance = np.array([el/sum_of_ev.sum() for el in sum_of_ev], dtype=float)

    return (matrix, sum_of_ev, c_importance)


def rank(matrix):

    row = matrix.shape[0]
    col = matrix.shape[1]

    # Нахождение суммы оценок (сумма по строкам)
    sum_of_ev = np.array(matrix.sum(1))

    # Нахождение коэффициентов важности
    c_importance = np.array([el/sum_of_ev.sum() for el in sum_of_ev], dtype=float)

    return (matrix, sum_of_ev, c_importance)


#a = np.array([[1, 2, 1, 1], [2, 1, 2, 2]], dtype=int)
#print(rank(a))