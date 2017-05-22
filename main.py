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
        entry = [i for i in range(2, 21, 1)]
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
            InputMatrix(int(param.get()), int(expert.get()), m_lst.current())

        # Связывание виджета, события и функции
        do_btn.bind('<Button-1>', full_matrix)


class InputMatrix():

    method = 0  # Метод (по-умолчанию 0 - предпочтения)
    col = 1
    row = 1
    matrix_entry = []
    point_entry = []
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
        params_l = [Label(win, text='h[' + str(i + 1) + ']') for i in range(self.row)]
        experts_l = [Label(win, text='E[' + str(i + 1) + ']') for i in range(self.col)]

        # Поля ввода для столбцов и строк матрицы
        self.matrix_entry = [[Entry(win, width=8) for i in range(self.col)] for j in range(self.row)]

        # Отображение лейблов критериев и вариантов
        for i in range(self.col):
            experts_l[i].grid(row=2, column=i + 1)
        for i in range(self.row):
            params_l[i].grid(row=3 + i, column=0)

        # Отображение полей ввода матрицы
        for i in range(self.row):
            for j in range(self.col):
                self.matrix_entry[i][j].grid(row=3 + i, column=1 + j, padx=3, pady=3)

        # Ввод дополнительных полей для метода ранга
        if self.method == 1:
            # Создание леблов для баллов
            Label(win, text='Введите границы балльной системы', bg='#dcf7dc').grid(row=4+self.row, column=0, columnspan=self.col+1)
            Label(win, text='От:').grid(row=5+self.row, column=0)
            self.point_entry.append(Entry(win, width=8))
            self.point_entry[-1].grid(row=5+self.row, column=1)
            Label(win, text='До:').grid(row=6 + self.row, column=0)
            self.point_entry.append(Entry(win, width=8))
            self.point_entry[-1].grid(row=6 + self.row, column=1)


        # Кнопка и ее отображение в окне win
        do_btn = Button(win, text='Далее', bg='#dcf7dc')
        do_btn.grid(row=7+self.row, column=(1+self.col)//2, pady=5)

        # Кнопки сохранения и загрузки конфигурации
        save_config_btn = Button(win, text='Сохранить конфигурацию', bg='#dcf7dc')
        load_config_btn = Button(win, text='Загрузить конфигурацию', bg='#dcf7dc')
        save_config_btn.grid(row=8 + self.row, column=self.col // 2, pady=5)
        load_config_btn.grid(row=8 + self.row, column=self.col // 2 + 2, pady=5)

        # Обработчик событий кнопки "Сохранить конфигурацию"
        def save_config(event):
            sa = asksaveasfilename(defaultextension='pr', filetypes=[('PR files', '.pr'), ('All files', '.*')])
            if sa:
                file = open(sa, 'wb')
                matrix_for_write = [[el.get() for el in row] for row in self.matrix_entry]
                from_wr = []
                to_wr = 0
                if self.method == 1:
                    from_wr = self.point_entry[0].get()
                    to_wr = self.point_entry[1].get()
                content = [matrix_for_write, from_wr, to_wr]
                pckl.dump(content, file)
                file.close()

        # Обработчик событий кнопки "Загрузить конфигурацию"
        def load_config(event):
            op = askopenfilename(defaultextension='pr', filetypes=[('PR files', '.pr'), ('All files', '.*')])
            if op:
                file = open(op, 'rb')
                content = pckl.load(file)
                file.close()

                # Проверить совместимость конфигурации и матрицы
                if len(content[0]) != self.row or len(content[0][0]) != self.col:
                    messagebox.showwarning("Ошибка", "Конфигурация не согласована с размерностью матрицы!")
                    return
                for i in range(self.row):
                    for j in range(self.col):
                        self.matrix_entry[i][j].insert(END, content[0][i][j])

                if self.method == 1:
                    self.point_entry[0].insert(END, content[1])
                    self.point_entry[1].insert(END, content[-1])


        def show_solution(event):
            matrix = np.zeros((self.row, self.col), dtype=float)
            from_point = 0
            to_point = 0

            for i in range(self.row):
                for j in range(self.col):
                    if self.matrix_entry[i][j].get():
                        try:
                            matrix[i, j] = float(self.matrix_entry[i][j].get())
                        except ValueError:
                            self.flag = True
                            messagebox.showwarning("Ошибка", "Данные введены неверно!")
                            return
                        else:
                            if not 1 <= matrix[i, j] <= self.row:
                                messagebox.showwarning("Ошибка", "Оценки(а) меньше 1 или больше количества критериев!")
                                return
                    else:
                        self.flag = True
                        messagebox.showwarning("Ошибка", "Данные введены неверно!")
                        return

            # Если метод ранга
            if self.method == 1:
                if self.point_entry[0] and self.point_entry[1]:
                    try:
                        from_point = float(self.point_entry[0].get())
                        to_point = float(self.point_entry[1].get())
                    except ValueError:
                        messagebox.showwarning("Ошибка", "Балльная шкала введена неверно!")
                        return
                else:
                    messagebox.showwarning("Ошибка", "Балльная шкала введена неверно!")
                    return

                for i in range(self.row):
                    for j in range(self.col):
                        if not from_point <= matrix[i, j] <= to_point:
                            messagebox.showwarning("Ошибка", "Данные не соответствуют балльной шкале!")
                            return

            # Вызов нужного окна для решения задачи
            SolutionPreference(matrix) if self.method == 0 else SolutionRank(matrix)

        # Связывание виджета, события и функции
        do_btn.bind('<Button-1>', show_solution)
        save_config_btn.bind('<Button-1>', save_config)
        load_config_btn.bind('<Button-1>', load_config)


class SolutionPreference():
    matrix = None

    def __init__(self, matrix):

        # Установка свойств
        self.matrix = matrix

        # Решение задачи
        solution = preference(self.matrix)
        row_matrix = self.matrix.shape[0]
        col_matrix = self.matrix.shape[1]

        # Создание дочернего окна
        win = Toplevel(root, relief='raised')
        win.title('Вывод решения')

        # Виджет шапка
        fra = Frame(win, width=200, height=20, bg='#dcf7dc')
        header = Label(fra, text='Решение по методу предпочтений', bg='#dcf7dc', justify='center')
        header.grid()
        fra.grid(row=0, column=0, columnspan=row_matrix, padx=3)

        # ШАГ 1
        Label(win, text='Шаг 1', bg='#dcf7dc').grid(row=1, column=0, pady=3)
        Label(win, text='Преобразуем матрицу оценок по формуле '
                        '(где M-количество параметров h)').grid(row=2,
                                                                column=0,
                                                                columnspan=col_matrix)

        Label(win, text='M-a[ij]', fg='red').grid(row=3, column=0, columnspan=col_matrix)

        # Вывод матрицы
        for i in range(row_matrix):
            for j in range(col_matrix):
                Label(win, text=str(solution[0][i, j]), fg='blue').grid(row=4+i, column=j, pady=3)

        ttk.Separator(win, orient='vertical').grid(row=1, column=col_matrix+1, rowspan=row_matrix+5, sticky='ns')

        # ШАГ 2
        Label(win, text='Шаг 2', bg='#dcf7dc').grid(row=1, column=col_matrix+2)
        Label(win, text='Найдем матрицу-столбец суммы оценок по строке').grid(row=2,
                                                                              column=col_matrix+2)

        # Вывод столбца сумм
        for i in range(row_matrix):
            Label(win, text=str(solution[1][i]), fg='blue').grid(row=4+i, column=col_matrix+2)

        Label(win, text='Сумма всех оценок: ').grid(row=4 + row_matrix, column=col_matrix + 2)
        Label(win, text=str(solution[1].sum()), fg='blue').grid(row=5 + row_matrix, column=col_matrix + 2)

        ttk.Separator(win, orient='vertical').grid(row=1, column=col_matrix+5, rowspan=row_matrix+5, sticky='ns')

        # ШАГ 3
        Label(win, text='Шаг 3', bg='#dcf7dc').grid(row=1, column=col_matrix+6)
        Label(win, text='Найдем коэффициенты важности как отношение оценки параметра к сумме всех оценок').grid(row=2,
                                                                              column=col_matrix + 7)
        # Вывод коэффициентов важности
        for i in range(row_matrix):
            Label(win, text='h[%d] = %.4f' % (i+1, solution[2][i]), fg='blue').grid(row=4+i, column=col_matrix + 7)

        crit_solution = '%.4f' % solution[2].min()
        Label(win, text='Наиболее важным критерием является критерий со значением '+crit_solution).grid(
            row=4+row_matrix, column=col_matrix+7)

        # Сохоанение результата
        save_solution_btn = Button(win, text='Сохранить результаты решения', bg='#dcf7dc')
        save_solution_btn.grid(row=6+row_matrix, column=0, pady=5)

        # Обработчик нажатия кнопки
        def save_solution(event):
            sa = asksaveasfilename(defaultextension='txt', filetypes=[('Text files', '.txt'), ('All files', '.*')])
            if sa:
                content = 'Метод предпочтений\nИсходные данные:\n1)Оценки экспертов:\n'

                for i in range(row_matrix):
                    for j in range(col_matrix):
                        content += str(self.matrix[i, j]) + ' '
                    content += '\n'

                content += '\n1)Преобразованные оценки:\n'
                for i in range(row_matrix):
                    for j in range(col_matrix):
                        content += str(solution[0][i, j]) + ' '
                    content += '\n'

                content += '\n' + '2)Сумма оценок:\n'
                for i in range(row_matrix):
                    content += str(solution[1][i]) + '\n'

                content += '\n3)Коэффициенты важности:\n'
                for i in range(row_matrix):
                    content += str(solution[2][i]) + '\n'
                file = open(sa, 'w')
                file.write(content)
                file.close()

        # Связывание обработчика и кнопки
        save_solution_btn.bind('<Button-1>', save_solution)

class SolutionRank():
    matrix = None

    def __init__(self, matrix):

        # Определение свойств
        self.matrix = matrix

        # Решение задачи
        solution = rank(self.matrix)
        row_matrix = self.matrix.shape[0]
        col_matrix = self.matrix.shape[1]

        # Создание дочернего окна
        win = Toplevel(root, relief='raised')
        win.title('Вывод решения')

        # Виджет шапка
        fra = Frame(win, width=200, height=20, bg='#dcf7dc')
        header = Label(fra, text='Решение по методу ранга', bg='#dcf7dc', justify='center')
        header.grid()
        fra.grid(row=0, column=0, columnspan=row_matrix, padx=3)

        # ШАГ 1
        Label(win, text='Шаг 1', bg='#dcf7dc').grid(row=1, column=0)
        Label(win, text='Найдем матрицу-столбец суммы оценок по строке').grid(row=2,
                                                                              column=0)

        # Вывод столбца сумм
        for i in range(row_matrix):
            Label(win, text=str(solution[1][i]), fg='blue').grid(row=4 + i, column=0)

        Label(win, text='Сумма всех оценок: ').grid(row=4 + row_matrix, column=0)
        Label(win, text=str(solution[1].sum()), fg='blue').grid(row=5 + row_matrix, column=0)

        ttk.Separator(win, orient='vertical').grid(row=1, column=col_matrix, rowspan=row_matrix + 5, sticky='ns')

        # ШАГ 2
        Label(win, text='Шаг 2', bg='#dcf7dc').grid(row=1, column=col_matrix + 1)
        Label(win, text='Найдем коэффициенты важности как '
                        'отношение оценки параметра к сумме всех оценок').grid(row=2,
                                                                               column=col_matrix + 2)
        # Вывод коэффициентов важности
        for i in range(row_matrix):
            Label(win, text='h[%d] = %.4f' % (i+1, solution[2][i]), fg='blue').grid(row=4 + i, column=col_matrix + 2)

        crit_solution = '%.4f' % solution[2].max()
        Label(win, text='Наиболее важным критерием является критерий со значением ' + crit_solution).grid(
            row=4 + row_matrix, column=col_matrix + 2)

        # Сохоанение результата
        save_solution_btn = Button(win, text='Сохранить результаты решения', bg='#dcf7dc')
        save_solution_btn.grid(row=6 + row_matrix, column=0, pady=5)

        # Обработчик нажатия кнопки
        def save_solution(event):
            sa = asksaveasfilename(defaultextension='txt', filetypes=[('Text files', '.txt'), ('All files', '.*')])
            if sa:
                content = 'Метод ранга\nИсходные данные:\nОценки экспертов:\n'

                for i in range(row_matrix):
                    for j in range(col_matrix):
                        content += str(self.matrix[i, j]) + ' '
                    content += '\n'

                content += '\nРешение:\n'

                content += '1)Сумма оценок:\n'
                for i in range(row_matrix):
                    content += str(solution[1][i]) + '\n'

                content += '\n2)Коэффициенты важности:\n'
                for i in range(row_matrix):
                    content += str(solution[2][i]) + '\n'
                file = open(sa, 'w')
                file.write(content)
                file.close()

        # Связывание обработчика и кнопки
        save_solution_btn.bind('<Button-1>', save_solution)


win = MainWindow()
root.mainloop()