from datetime import date
from tinydb import TinyDB, Query


'''Создание БД списка операций'''
db = TinyDB('wallet.json')
'''Создание БД баланса'''
table = db.table('balance')
qop = Query()

def main():
    balance = 0
    choice = 10
    print('\n')
    print("1.Добавить операцию")
    print("2.Просмотреть все операции")
    print("3.Поиск по дате")
    print("4.Поиск по категории")
    print("5.Поиск по сумме")
    print("6.Изменить операцию")
    print("7.Удалить операцию")
    print("8.Очистка списка операций")
    print("9.Текущий баланс")
    print("0.Выход")
    print('\n')

    while choice != 0:
        '''Создание вариантов выбора для главного меню'''
        choice = int(input())

        if choice == 1:
            '''Добавление записи'''
            print('***** Добавление записи *****')

            print("Укажите категорию операции:\n"
                    "Расход или Доход")
            category = input()

            amount = int(input("Укажите сумму операции: "))

            i_year = int(input('Укажите год операции: '))
            i_month = int(input('Укажите месяц операции: '))
            i_day = int(input('Укажите число операции: '))

            '''Запись даты и преобразование в строку для сериализации в JSON.'''
            date_operation = date(year = i_year, month = i_month, day = i_day)
            str_dateop = date_operation.strftime('%d.%m.%Y')
            description = input("Описание операции: ")
            '''Расчет баланса после ввода категории'''
            if category == 'Расход':
                balance = balance - amount
            elif category == 'Доход':
                balance = balance + amount
            else:
                print('Неверная категория')

            id = int(input("Укажите уникальный номер операции для обозначения его в списке: "))

            '''Добавление записи в БД'''
            db.insert({'Номер_операции': id,
                       'Категория': category,
                       'Сумма':   amount,
                       'Дата': str_dateop,
                       'Описание': description})
            print("Запись добавлена")

            '''Обновление баланса после добавление операции'''
            table.update({'Баланс': balance})


        elif choice == 2:
            '''Вывод всех записей'''
            print('***** Вывод всех записей *****')

            wallet = db.search(qop.Сумма > 0)
            for line in wallet:
                print(line)
                print('\n')

        elif choice == 3:
            '''Поиск по дате'''
            print('***** Поиск по дате *****')

            f_year = int(input('Укажите год операции: '))
            f_month = int(input('Укажите месяц операции: '))
            f_day = int(input('Укажите число операции: '))

            '''Для поиска по интервалам даты я мог бы сделать кодировщик JSONEncoder из библиотеки json, чтобы он поддерживал не только примитивные типы данных, но и объекты date'''

            operation_d = date(year = f_year, month = f_month, day = f_day)
            str_datese = operation_d.strftime('%d.%m.%Y')
            operation_f = db.search(qop.Дата == str_datese)
            for line in operation_f:
                print('\n')
                print(line)


        elif choice == 4:
            '''Поиск по категории'''
            print('***** Поиск по категории *****')

            find_category = input('Укажите категорию для поиска: ')
            operation_c = db.search(qop.Категория == find_category)
            for line in operation_c:
                print('\n')
                print(line)

        elif choice == 5:
            '''Поиск по сумме'''
            print('***** Поиск по сумме *****')

            find_amount = int(input("Укажите сумму для поиска: "))
            operation_a = db.search(qop.Сумма == find_amount)
            for line in operation_a:
                print('\n')
                print(line)


        elif choice == 6:
            '''Изменение записи'''
            print('***** Изменение записи *****')

            id = int(input('Укажите номер операции для её изменения: '))
            upd_category = input('Укажите категорию для изменения: ')
            '''Поиск по id и взятие программой суммы и категории для перерасчета баланса после изменения записи об операции'''
            find_list = db.search(qop.Номер_операции == id)
            find_dict = find_list[0]
            result_amount = find_dict['Сумма']

            find_listcat = db.search(qop.Номер_операции == id)
            find_dictcat = find_listcat[0]
            result_cat = find_dictcat['Категория']

            upd_amount = int(input("Укажите сумму для изменения: "))
            '''Расчет баланса после изменения записи об операции, отталкиваясь от исходной категории операции'''
            if upd_category == 'Расход':
                balance = balance - upd_amount
            elif upd_category == 'Доход':
                balance = balance + upd_amount


            f_year = int(input('Укажите год операции для изменения: '))
            f_month = int(input('Укажите месяц операции для изменения: '))
            f_day = int(input('Укажите число операции для изменения: '))
            operation_d = date(year=f_year, month=f_month, day=f_day)
            str_datese = operation_d.strftime('%d.%m.%Y')

            upd_desc = input("Описание операции: ")

            db.update({'Категория': upd_category, 'Сумма': upd_amount, 'Дата': str_datese, 'Описание': upd_desc}, qop.Номер_операции == id)
            '''Перерасчет баланса после изменения записи об операции, отталкиваясь от измененной категории операции'''
            if result_cat == 'Расход':
                balance = balance + result_amount
            elif result_cat == 'Доход':
                balance = balance - result_amount

            table.update({'Баланс': balance})
            print('Запись обновлена')

        elif choice == 7:
            '''Удаление записи'''
            print('***** Удаление записи *****')
            id = int(input("Укажите номер операции для её удаления: "))
            print(db.search(qop.Номер_операции == id))
            confirmation = input("Вы хотите удалить эту операцию(Да/Нет)?: ")
            if confirmation == 'Да':
                find_list = db.search(qop.Номер_операции == id)
                find_dict = find_list[0]
                result_amount = find_dict['Сумма']

                find_listcat = db.search(qop.Номер_операции == id)
                find_dictcat = find_listcat[0]
                result_cat = find_dictcat['Категория']
                '''Перерасчет баланса после удаления записи об операции, отталкиваясь от указанной категории операции'''
                if result_cat == 'Расход':
                    balance = balance + result_amount
                elif result_cat == 'Доход':
                    balance = balance - result_amount
                table.update({'Баланс': balance})

                db.remove(qop.Номер_операции == id)
            else:
                pass

        elif choice == 8:
            '''Очистка списка'''
            print('***** Очистка списка *****')
            confirmation = input("Вы уверены, что хотите очистить кошелек(Да/Нет)?: ")
            '''Подтверждение очистки'''
            if confirmation == 'Да':
                db.truncate()
                table.truncate()
                table.insert({'Баланс': balance})
                print("Список операций очищен")
            else:
                pass

        elif choice == 9:
            '''Текущий баланс'''

            current_balance = table.search(qop.Баланс == balance)
            print('Текущий баланс: ', current_balance)

        else:
            '''Выход'''
            print("Выход")

if __name__ == "__main__":
    main()