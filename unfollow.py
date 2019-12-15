import instaloader
import requests
import time
from time import sleep


l = instaloader.Instaloader()
l.login('login', 'password')
profile = instaloader.Profile.from_username(l.context, 'username')



list_my_following = []
for following in profile.get_followees():
    list_my_following.append(following.userid)

set_my_following = set(list_my_following)



list_my_followers = []
for follower in profile.get_followers():
    list_my_followers.append(follower.userid)


set_my_followers = set(list_my_followers)
unfollow_set = set_my_following.difference(set_my_followers)
unfollow_list = list(unfollow_set)


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





i = 0
for user in unfollow_list:
    i = i + 1
    try:
        unfollow = session.post(f"https://www.instagram.com/web/friendships/{user}/unfollow/", headers=parameters)
        print(f'отписка от {user} выполнена. отписок выполнено: {i}')
        sleep(45)
    except:
        continue











