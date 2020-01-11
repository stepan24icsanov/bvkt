import requests
import json
from time import sleep


def auth(login, password):
    url = 'https://www.instagram.com/accounts/login/ajax/'
    csrf_token = requests.get("https://instagram.com").cookies.get_dict()["csrftoken"]
    params = {'username': login,
              'password': password,
              'enc_password': None,
              'queryParams': {},
              'optIntoOneTap': 'false'}
    session = requests.Session()
    response = session.post(url, data=params)
    user_id = response.json()["userId"]
    cookies = response.cookies.get_dict()
    session_id = cookies["sessionid"]
    mid = cookies["mid"]
    parameters = {
        "cookie": f"mid={mid}; csrftoken={csrf_token}; ds_user_id={user_id}; sessionid={session_id};",
        "x-csrftoken": csrf_token}
    return session, parameters


def users_list(name_file):
    with open(name_file) as file:
        users_list = [l.strip() for l in file]
    return users_list


def view_story(session, query_hash, parameters, user):
    get_id = session.get(f'https://www.instagram.com/{user}/?__a=1')
    string_with_id = get_id.json()['logging_page_id']
    id_user = int(string_with_id[12:])
    variables = {"reel_ids": [str(id_user)],
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
    list_story = get_story_id.json()['data']['reels_media'][0]['items']
    latest_reel_media_id = get_story_id.json()['data']['reels_media'][0]['latest_reel_media']
    for story in list_story:
        view_story = session.post(url='https://www.instagram.com/stories/reel/seen',
                                  data={'reelMediaId': list_story[0]['id'],
                                        'reelMediaOwnerId': id_user,
                                        'reelId': id_user,
                                        'reelMediaTakenAt': latest_reel_media_id,
                                        'vievSeenAt': latest_reel_media_id
                                        },
                                  headers=parameters)
        sleep(7)
        


login = 'login'
password = 'password'
query_hash = 'query_hash'

if __name__ == '__main__':
    instagram_auth = auth(login, password)
    session = instagram_auth[0]
    parameters = instagram_auth[1]
    list_users = users_list('result.txt')
    for user in list_users:
        view_story(session, query_hash, parameters, user)


