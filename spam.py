import requests


token = ''
params = {'access_token': token, 'random_id': 0, 'peer_id'; 431149734, 'message': 'huy'}
request = requests.get('https://api.vk.com/method/messages.send',params=params)
