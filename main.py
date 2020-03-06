import requests
import time
import json

TOKEN = ''
URL = 'https://api.vk.com/method/'
VERSION_API = '5.103'

# (eshmargunov) и id (171691064)
main_user = ''


# Список друзей пользователя
def get_friends(user_id):
    method = 'friends.get'
    url = f'{URL}{method}'
    params = {
        'access_token': TOKEN,
        'user_id': user_id,
        'v': VERSION_API
    }
    response = requests.get(url, params=params)
    count = response.json()['response']['count']
    user_list = (response.json()['response'])
    user_list_in = user_list['items']
    return user_list_in


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
    # print(response.json())
    count = response.json()['response']['count']
    group_list = (response.json()['response'])
    group_list_in = group_list['items']
    return group_list_in


# Список пользователей в группе
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


def group_info(user_id):
    method = 'groups.getById'
    url = f'{URL}{method}'
    group_list = entry_user(user_id)
    to_json = {}
    for group_id in group_list:
        params = {
            'access_token': TOKEN,
            'group_id': group_id,
            'v': VERSION_API,
            'fields': 'members_count'
        }
        response = requests.get(url, params=params)
        for dict_group in response.json()['response']:
            name = dict_group['name']
            gid = dict_group['id']
            members_count = dict_group['members_count']
            to_json_1 = {"name": name, "gid": gid, "members_count": members_count}
            to_json.update(to_json_1)
    print(to_json)



def wr_json_file(user_id):
    name_file = f'without friends_id{user_id}.json'
    with open(name_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(group_info(user_id), sort_keys=True, indent=4, ensure_ascii=False))
    print(f'Файл со словарём групп пользователя, где нет его друзей создан! Имя файла {name_file}')


if __name__ == '__main__':
    # group_info(main_user)
    wr_json_file(main_user)
    # print(entry_user(main_user))
# print(get_friends(user_id))
