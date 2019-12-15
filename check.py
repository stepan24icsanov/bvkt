import requests
import json
import instaloader
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

l = instaloader.Instaloader()
l.login('login', 'password')
profile = instaloader.Profile.from_username(l.context, 'username')
users_list = []
for user in profile.get_followees():
    users_list.append(user.userid)



query_hash = 'query_hash'

for user in users_list:
    try:
        variables = {"reel_ids": [str(user)],
                 "tag_names": [],
                 "location_ids": [],
                 "highlight_reel_ids": [],
                 "precomposed_overlay": "false",
                 "show_story_viewer_list": "true",
                 "story_viewer_fetch_count": 50,
                 "story_viewer_cursor": "",
                 "stories_video_dash_manifest": "false"}
        variables_json = json.dumps(variables)
        get_story_id = session.get(url='https://www.instagram.com/graphql/query/',
                               params={
                                   'query_hash': query_hash,
                                   'variables': variables_json
                               },
                               headers=parameters)
        r = get_story_id.json()
        list_story = r['data']['reels_media'][0]['items']
        latest_reel_media_id = r['data']['reels_media'][0]['latest_reel_media']
        for story in list_story:
            view_story = session.post(url='https://www.instagram.com/stories/reel/seen',
                                      data={'reelMediaId': list_story[0]['id'],
                                            'reelMediaOwnerId': user,
                                            'reelId': user,
                                            'reelMediaTakenAt': latest_reel_media_id,
                                            'vievSeenAt': latest_reel_media_id
                                            },
                                    headers=parameters)
            print(viev_story.json())
            sleep(1)
    except:
        continue




