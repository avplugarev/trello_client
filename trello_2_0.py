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

def read ():
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json();
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        tasks_list=list();
        print(column['name']+' ', end='')
        # Получим данные всех задач в колонке и перечислим все названия
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        if not task_data:
            print('(The sum of tasks = 0)')
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            task = '\t' + task['name'];
            tasks_list.append(task)
        #print('(',len(tasks_list),')')
        print('(The sum of tasks = {sum})'.format(sum=len(tasks_list)));
        for task in tasks_list:
            print(task);

def create (name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
    for column in column_data:
        if column['name'] == column_name:
            # Создадим задачу с именем _name_ в найденной колонке
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break
def create_list (column_name):
    requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard':'5dd8256605ab1e8bcff7fd4d', **auth_params});

def move(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Среди всех колонок нужно найти задачу по имени и получить её id
    task_id = None
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                break
        if task_id:
            break

            # Теперь, когда у нас есть id задачи, которую мы хотим переместить
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
    for column in column_data:
        if column['name'] == column_name:
            # И выполним запрос к API для перемещения задачи в нужную колонку
            requests.put(base_url.format('cards') + '/' + task_id + '/idList',
                         data={'value': column['id'], **auth_params})
            break



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