import vk_api
import requests
import os
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType



token = os.environ.get('GROUP_TOKEN')
groupID =  169777737
access_token = os.environ.get('ACCESS_TOKEN')

vk = vk_api.VkApi(token=token)

vk._auth_token()
vk.get_api()
longpoll = VkBotLongPoll(vk, groupID)

while True:
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.from_chat:
                if '.ава' in event.object['message']['text'].lower():
                    try:
                        get_user = vk.method('users.get', {'user_id': event.object['message']['text'][5:], 'fields': 'photo_id'})
                        photo = get_user[0]['photo_id']
                        vk.method('messages.send', {'chat_id': event.chat_id, 'attachment': f'photo{photo}', 'random_id': 0})
                    except:
                        vk.method('messages.send',
                                  {'chat_id': event.chat_id, 'message': 'пользователь умер',
                                   'random_id': 0})

                elif '.видео' in event.object['message']['text'].lower():
                    try:
                        search_video = requests.get('https://api.vk.com/method/video.search',
                                                    params={'access_token':access_token,
                                                            'q': event.object['message']['text'][7:],
                                                            'adult': 1,
                                                            'v': '5.103'
                                                            })
                        video = search_video.json()['response']
                        owner_id = video['items'][0]['owner_id']
                        id_video = video['items'][0]['id']
                        vk.method('messages.send', {'chat_id': event.chat_id, 'attachment': f'video{owner_id}_{id_video}', 'random_id': 0})
                    except:
                        vk.method('messages.send', {'chat_id': event.chat_id, 'message':'видео не найдено' , 'random_id': 0})

        elif event.type == VkBotEventType.WALL_POST_NEW:
            print(event)





