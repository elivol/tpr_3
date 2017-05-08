from tkinter import ttk, messagebox
from tkinter.filedialog import *
from funcs import *
import pickle as pckl

root = Tk()
root.title('ТПР')

class MainWindow():

    def __init__(self):
        # Виджет шапка
        fra = Frame(root, bg='#dcf7dc')
        header = Label(fra, text='Выберите параметры матрицы и метод решения', bg='#dcf7dc')
        header.grid(row=0, column=0, columnspan=4, rowspan=2)
        fra.grid(row=0, column=0, columnspan=4, rowspan=2)

        # Выпадающие листы с размерностью матрицы
        entry = [i for i in range(1, 10, 1)]
        param_l = Label(root, text='Количество параметров h')
        param = ttk.Combobox(root, values=entry, height=8, width=10, state='readonly')
        param.set(entry[0])

        expert_l = Label(root, text='Количество экспертов E')
        expert = ttk.Combobox(root, values=entry, height=8, width=10, state='readonly')
        expert.set(entry[0])

        # Выбор метода
        meth_l = Label(root, text='Выберите метод')

        methods = ['Метод предпочтения', 'Метод ранга']
        m_lst = ttk.Combobox(root, values=methods, height=2, state='readonly')
        m_lst.set(methods[0])

        # Кнопка
        do_btn = Button(root, text='Далее', bg='#dcf7dc')

        # Расположение виджетов в окне и их отображение
        param_l.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        expert_l.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        param.grid(row=2, column=2, columnspan=2, padx=5, pady=5)
        expert.grid(row=3, column=2, columnspan=2, padx=5, pady=5)
        meth_l.grid(row=4, column=0, columnspan=1, padx=5, pady=5)
        m_lst.grid(row=4, column=2, columnspan=1, padx=5, pady=5)
        do_btn.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        def full_matrix(event):
            InputMatrix(int(expert.get()), int(param.get()), m_lst.current())

        # Связывание виджета, события и функции
        do_btn.bind('<Button-1>', full_matrix)


class InputMatrix():

    method = 0  # Метод (по-умолчанию 0 - предпочтения)
    col = 1
    row = 1
    matrix_entry = []
    flag = False

    def __init__(self, row, col, method):

        # Установка свойств класса
        self.col = col
        self.row = row
        self.method = method

        # Создание дочернего окна
        win = Toplevel(root, relief='raised')
        win.title('Ввод матрицы')

        # Лейблы для столбцов и строк
        params_l = [Label(win, text='h[' + str(i + 1) + ']') for i in range(self.col)]
        experts_l = [Label(win, text='E[' + str(i + 1) + ']') for i in range(self.row)]

        # Поля ввода для столбцов и строк матрицы
        self.matrix_entry = [[Entry(win, width=8) for i in range(self.col)] for j in range(self.row)]

        # Отображение лейблов критериев и вариантов
        for i in range(self.col):
            params_l[i].grid(row=2, column=i + 1)
        for i in range(self.row):
            experts_l[i].grid(row=3 + i, column=0)

        # Отображение полей ввода матрицы
        for i in range(self.row):
            for j in range(self.col):
                self.matrix_entry[i][j].grid(row=3 + i, column=1 + j, padx=3, pady=3)

        # Ввод дополнительных полей для метода ранга
        if self.method == 1:
            # Создание леблов для баллов
            Label(win, text='Введите границы балльной системы', bg='#dcf7dc').grid(row=4+self.row, column=0, columnspan=self.col+1)
            Label(win, text='От:').grid(row=5+self.row, column=0)
            Entry(win, width=8).grid(row=5+self.row, column=1)
            Label(win, text='До:').grid(row=6 + self.row, column=0)
            Entry(win, width=8).grid(row=6 + self.row, column=1)


        # Кнопка и ее отображение в окне win
        do_btn = Button(win, text='Далее', bg='#dcf7dc')
        do_btn.grid(row=7+self.row, column=(1+self.col)//2, pady=5)

        # Кнопки сохранения и загрузки конфигурации
        save_config_btn = Button(win, text='Сохранить конфигурацию', bg='#dcf7dc')
        load_config_btn = Button(win, text='Загрузить конфигурацию', bg='#dcf7dc')
        save_config_btn.grid(row=3 + self.row + 6, column=self.col // 2, pady=5)
        load_config_btn.grid(row=3 + self.row + 6, column=self.col // 2 + 2, pady=5)

win = MainWindow()
root.mainloop()