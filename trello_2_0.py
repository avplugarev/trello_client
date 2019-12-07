import requests
import sys

#Данные авторизации а API трелло
auth_params = {
    'key': 'd7b864e1040c8e3b473769742f42a6ff',
    'token': '82a4b855a0ca518754561bd83c6267ddf01028d7786e08f760be944e5ab5639b',
}

# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.
base_url = 'https://api.trello.com/1/{}'
board_id = 'iVPLKIAa';

def read (): #метод вывода списка колонок, кол-во задач в них и названия задач
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json();
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        print(column['name']+' ', end='')
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        if not task_data:
            print('(The sum of tasks = 0)')
            print('\t' + 'Нет задач!')
            continue
        else:
            print('(The sum of tasks = {sum})'.format(sum=len(task_data))); #считаем кол-во задач в колонке
        for task in task_data:
            print('\t' + task['name']);

def create (name, column_name): #метод создания задачи
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
    for column in column_data:
        if column['name'] == column_name:
            # Создадим задачу с именем name в найденной колонке
            response = requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            if response.status_code == 200:
                print('задача успешно создана')
            else:
                print('во время создания возникала ошибка - статус: ', response.status_code)
            break
def create_list (column_name): #метод создания колонки в нашей доске
    response = requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard':'5dd8256605ab1e8bcff7fd4d', **auth_params});
    if response.status_code == 200:
        print('колонка успешно создана')
    else:
        print('во время создания колонки возникала ошибка - статус: ', response.status_code)

def send_move_data (task_id, column_name, column_data):
    # Теперь, когда у нас есть id задачи и она мы знаем, что у нее нет дублей
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
    for column in column_data:
        if column['name'] == column_name:
            # И выполним запрос к API для перемещения задачи в нужную колонку
            response = requests.put(base_url.format('cards') + '/' + task_id + '/idList',
                                    data={'value': column['id'], **auth_params})
            if response.status_code == 200:
                print('задача успешно перемещена')
            else:
                print('во время перемещения возникала ошибка - статус: ', response.status_code)
            break

def move(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Среди всех колонок нужно найти задачу по имени и получить её id
    task_id_lists = list(); #собираем список id задач с одинкавыми именами
    duplicate_info = dict(); #заносим информацию по задачам с одинаковыми именами
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id_lists.append(task['id']);
                duplicate_info[task['id']] = task['name'], task['id'], column['name'];
    #после прохода по всем столбцам обрабатываем результаты поиска дубликатов
    if len(task_id_lists) == 0:
        print('Выбранная вами задача отсутствует в этой доске')
    elif len(duplicate_info.keys()) == 1:
        send_move_data(task_id_lists[0], column_name, column_data);
    else:
        print('Среди задач обнаружены дубли','\n');
        for values in duplicate_info.values():
            values=list(values);
            print('Имя дубликата: {name}, id дубликата: {id}, колонка дубликата: {column}'.format(name=values[0],
                                                                                                  id=values[1],
                                                                                               column=values[2]))
        task_id = input('Введите id задачи, которую нужно переместить \n')
        send_move_data(task_id, column_name, column_data);

if __name__ == "__main__":
    #create_list('check');
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3]);
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3]);
    elif sys.argv[1] == 'create_column':
        create_list(sys.argv[2]);


#python3 trello_2_0.py - вывести список задач
#python3 trello_2_0.py move 'изучи python' 'Doing' - перенести задачу в другой список
#python3 trello_2_0.py create 'изучи python' 'To Do' - создать задачу
#python3 trello_2_0.py create_column 'supercheck' - создать новую колонку для задач
#https://test.pypi.org/project/trello-client-basics-api-nightgust-2/0.0.1/ - адрес пакета для pip
#для установки через pip: python3 -m pip install --index-url https://test.pypi.org/project/trello-client-basics-api-nightgust-2/0.0.1/