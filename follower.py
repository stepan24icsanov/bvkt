import requests
import time
from time import sleep



login = 'login'
password = 'password'
url = 'https://www.instagram.com/accounts/login/ajax/'
csrf_token = requests.get("https://instagram.com").cookies.get_dict()["csrftoken"]

headers = {'x-csrftoken': csrf_token}
params = {'username': login,
          'password': password,
          'enc_password': None,
          'queryParams': {},
          'optIntoOneTap': 'false'}

session = requests.Session()
response = session.post(url, data=params, headers=headers)

user_id = response.json()["userId"]
cookies = response.cookies.get_dict()
session_id = cookies["sessionid"]
mid = cookies["mid"]

parameters = {
	"cookie": f"mid={mid}; csrftoken={csrf_token}; ds_user_id={user_id}; sessionid={session_id};",
    "x-csrftoken": csrf_token}


with open('F:/result.txt', 'r') as file:
    users = [l.strip() for l in file]

for user in users:
    try:
        response = requests.get(f'https://www.instagram.com/{user}/?__a=1')
        string_with_id = response.json()['logging_page_id']
        id_user = int(string_with_id[12:23])
        follow = session.post(f"https://www.instagram.com/web/friendships/{id_user}/follow/", headers=parameters)
        sleep(10)
        string_with_id_post = response.json()['graphql']['user']['edge_owner_to_timeline_media']['edges'][0]['node']['id']
        id_post = int(string_with_id_post)
        like = session.post(f'https://www.instagram.com/web/likes/{id_post}/like/', headers=headers)
        sleep(60)
        print(f'подписка выполнена на {user}')
    except:
        continue



