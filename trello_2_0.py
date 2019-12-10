import requests
import sys

# Данные авторизации а API трелло
auth_params = {
    'key': '', #введите свой API ключ
    'token': '', #введите свой токен
}

# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.
base_url = 'https://api.trello.com/1/{}';
board_id = ''; #введите короткий id достки из адреса
board_id_long = ''; #введите длиныый id доски



def read():  # метод вывода списка колонок, кол-во задач в них и названия задач
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json();
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        print(column['name'] + ' ', end='')
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        if not task_data:
            print('(The sum of tasks = 0)')
            print('\t' + 'Нет задач!')
            continue
        else:
            print('(The sum of tasks = {sum})'.format(sum=len(task_data)));  # считаем кол-во задач в колонке
        for task in task_data:
            print('\t' + task['name']+' '+task['id']);

# метод создания задачи
def create(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    idColumn=search_column(column_name, column_data); #ищем id колонны где надо создать задачу
    response = requests.post(base_url.format('cards'), data={'name': name, 'idList': idColumn, **auth_params})
    success_result(response.status_code, response.text);

# метод создания колонки в нашей доске
def create_list(column_name):
    response = requests.post(base_url.format('lists'),
                             data={'name': column_name, 'idBoard': board_id_long, **auth_params});
    success_result(response.status_code, response.text)

#вспомогательный метод поиска id нужной нам колонки - вынесен, чтобы не дублировать код
def search_column(column_name, column_data):
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
    wrong_column = 0;
    for column in column_data:
        if column['name'] == column_name:
            wrong_column += 1;
            return column['id'];
            break
    if wrong_column == 0:
        print('Указанная вами колонка отсутствует в этой доске');
        return 0;

#вспомогательные метод проверки на дубликаты названий задач и получения корректного id задачи
def search_and_check_duplicate(column_data, name):
    task_id_lists = list();  # собираем список id задач с одинкавыми именами
    duplicate_info = dict();  # заносим информацию по задачам с одинаковыми именами
    # Среди всех колонок нужно найти задачу по имени и получить её id
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id_lists.append(task['id']);
                duplicate_info[task['id']] = task['name'], task['id'], column['name'];
    # после прохода по всем столбцам обрабатываем результаты поиска дубликатов
    if len(task_id_lists) == 0:
        print('Выбранная вами задача отсутствует в этой доске')
        return 0
    elif len(duplicate_info.keys()) == 1:
        return task_id_lists[0];
    else:
        print('Среди задач обнаружены дубли', '\n');
        for values in duplicate_info.values():
            values = list(values);
            print('Имя дубликата: {name}, id дубликата: {id}, колонка дубликата: {column}'.format(name=values[0],
                                                                                                  id=values[1],
                                                                                                  column=values[2]))
        task_id = input('Введите id задачи, которую нужно переместить \n')
        return task_id

#вспомогательным метод объеявления результата передача через апи задачи - вынесен, чтобы не дублировать код
def success_result(status, text):
    if status == 200:
        print('операция успешно выполнена')
    else:
        print('во время операции возникала ошибка - статус: ', status, '\n', text)

#метод перемещения задачи по колонкам
def move(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    idCard = search_and_check_duplicate(column_data, name);  # получаем id карты
    idColumn = search_column(column_name, column_data);  # получаем id колонки
    if idCard != 0 and idColumn != 0: #если есть id карты и колонки - делаем запрос на перемещение
        response = requests.put(base_url.format('cards') + '/' + idCard + '/idList',
                                data={'value': idColumn, **auth_params})
        success_result(response.status_code, response.text);
def initial_check():
    if auth_params['key'] =='' or auth_params['token'] == '' or board_id =='' or board_id_long == '':
        print('Перед началом работы в файле скрипта нужно ввести API ключ, токен, оба id досок')
        return False

if __name__ == "__main__":
    if initial_check() !=False:
        if len(sys.argv) <= 2:
            read()
        elif sys.argv[1] == 'create':
            create(sys.argv[2], sys.argv[3]);
        elif sys.argv[1] == 'move':
            move(sys.argv[2], sys.argv[3]);
        elif sys.argv[1] == 'create_column':
            create_list(sys.argv[2]);

#команды для проверки
#Перед началом тестирования заполните свои апи ключ и токен, а также короткий и длинный id для вашей программы
# python3 trello_2_0.py - вывести список задач
# python3 trello_2_0.py move 'изучи python4' 'Doing' - перенести задачу в другой список
# python3 trello_2_0.py create 'изучи python25' 'To Do' - создать задачу
# python3 trello_2_0.py create_column 'supercheck34' - создать новую колонку для задач
# https://test.pypi.org/project/trello-client-basics-api-nightgust-2/0.0.1/ - адрес пакета для pip
# для установки через pip: python3 -m pip install --index-url https://test.pypi.org/project/trello-client-basics-api-nightgust-2/0.0.4/
