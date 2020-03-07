import requests
import time
import json

TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
URL = 'https://api.vk.com/method/'
VERSION_API = '5.103'

# (eshmargunov) и id (171691064)
main_user = '171691064'


# Клас для обработки ошибки при обращении к vk api
class VkApiError(Exception):
    def __init__(self, text):
        self.txt = text


# Список сообществ пользователя
def get_groups(user):
    method = 'groups.get'
    url = f'{URL}{method}'
    params = {
        'access_token': TOKEN,
        'user_id': user,
        'v': VERSION_API,
        'count': 1000
    }
    response = requests.get(url, params=params)
    group_list = (response.json()['response'])
    group_list_in = group_list['items']
    return group_list_in


# Список пользователей в группе, с фильтрацией по друзьям, параметр 'filter': 'friends'
def entry_user(user_id):
    method = 'groups.getMembers'
    url = f'{URL}{method}'
    group_list = get_groups(user_id)
    ex_group_list = []
    for group_id in group_list:
        params = {
            'access_token': TOKEN,
            'group_id': group_id,
            'filter': 'friends',
            'v': VERSION_API
        }
        response = requests.get(url, params=params)
        # print(response.json())
        count = response.json()['response']['count']
        print('.')
        time.sleep(0.5)
        if count == 0:
            ex_group_list.append(group_id)
    return ex_group_list


# Информация о группах в которой состоит пользователь и создание списка по заданному шаблону
def group_info(user_id):
    method = 'groups.getById'
    url = f'{URL}{method}'
    group_list = entry_user(user_id)
    # to_json_dict = {}
    to_json_list = []
    for group_id in group_list:
        params = {
            'access_token': TOKEN,
            'group_id': group_id,
            'v': VERSION_API,
            'fields': 'members_count'
        }
        try:
            response = requests.get(url, params=params)
            if 'error' in response.json().keys():
                time.sleep(0.5)
                error = response.json()['error']['error_msg']
                raise VkApiError(f'Ошибка! {error}')
            for dict_group in response.json()['response']:
                name = dict_group['name']
                gid = dict_group['id']
                members_count = dict_group['members_count']
                to_json_1 = {"name": name, "gid": gid, "members_count": members_count}
                to_json_list.append(to_json_1)
        except VkApiError as msg:
            print(msg)
    return to_json_list


def wr_json_file(user_id):
    name_file = f'without friends_id{user_id}.json'
    with open(name_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(group_info(user_id), indent=4, ensure_ascii=False))
    print(f"Файл со словарём групп пользователя, где нет его друзей создан! Имя файла '{name_file}'")


if __name__ == '__main__':
    wr_json_file(main_user)
