import requests, json

TOKEN = open('src/token.txt', 'r').read()

user_to_channel = lambda user_id: requests.post('https://discord.com/api/v9/users/@me/channels', json={'recipients':[user_id]}, headers={'authorization':TOKEN}).json()['id']

def save_data(id):
    total = []
    data = requests.get(f'https://discord.com/api/v9/channels/{id}/messages?limit=50', headers={'authorization':TOKEN}).json()
    while True:
        total.append(data)
        if len(data) < 50:
            break
        else:
            last = data[49]['id']
        data = requests.get(f'https://discord.com/api/v9/channels/{id}/messages?before={last}&limit=50', headers={'authorization':TOKEN}).json()
    open('data.json', 'w').write(json.dumps([x for y in total for x in y]))

download_type = int(input('\u001b[34mPlease select which type of channel you want to download?\u001b[0m\n\n1. User DMs\n2. Text channel\n\n> '))

if download_type == 1:
    save_data(user_to_channel(int(input('\n\u001b[34mEnter their user ID:\u001b[0m '))))
elif download_type == 2:
    save_data(int(input('\n\u001b[34mEnter the channel ID:\u001b[0m ')))
