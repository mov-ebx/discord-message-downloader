import json, datetime, markdown

def discord_md(text):
    return markdown.markdown(text.replace('#','&#35;').replace('<','&lt;').replace('>','&gt;').replace('>','&gt;')).replace('\n', '<br>')

def write(id):
    data = json.loads(open('data.json', 'r').read())
    html = f'<!DOCTYPE html>\n<html lang="en">\n<head>\n\t<meta charset="UTF-8">\n\t<meta http-equiv="X-UA-Compatible" content="IE=edge">\n\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n\t<title>Saved - {id}</title>\n\t'+'''<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300&family=Work+Sans:wght@400&display=swap" rel="stylesheet"><style>html, body {padding: 0;margin: 0;height: 100%;width: 100%;background-color: #313238;}body > div {width: max-content;margin-bottom:16px;}.message {margin-top: 17px;margin-left: 16px;}.post {left: 72px;}.content {padding-left: 16px;display: inline;position: absolute; margin: 0; width: max-content;}.text {margin: 0; padding: 0;}.text * {color: rgb(224, 225, 229); margin: 0;}.timestamp {color: rgb(152, 154, 162); margin-left: 2px;font-size: 0.75rem;}img {width: 40px;height: 40px;margin-top: 2px;clip-path:circle();display: inline;}h3 {display: inline;position: relative;}* { font-family: 'Open Sans', sans-serif; font-family: 'Work Sans', sans-serif; font-size: 1rem; font-weight: 500; line-height: 1.375rem; } strong, strong * {font-weight: bold;}</style>'''+'\n</head>\n<body>\n\t<div>'
    last_time, last_author = datetime.datetime.min, 0
    for msg in reversed(data):
        timestamp = datetime.datetime.fromisoformat(msg['timestamp'][:-6])
        if msg['author']['id'] == last_author and (timestamp-last_time).total_seconds() < 10*60:
            html += f'\n\t\t<h3 class="text post">\n\t\t\t{discord_md(msg["content"])}\n\t\t</h3>'
        else:
            html += f'\n\t\t<div class="message">\n\t\t\t<img src="https://cdn.discordapp.com/avatars/{msg["author"]["id"]}/{msg["author"]["avatar"]}.webp?size=80" aria-hidden="true" alt="">\n\t\t\t<div class="content">\n\t\t\t\t<h3>\n\t\t\t\t\t<span style="color:#F3F4F5;">\n\t\t\t\t\t\t{msg["author"]["display_name"] if msg["author"]["display_name"] != None else msg["author"]["username"]}\n\t\t\t\t\t</span>\n\t\t\t\t\t<span class="timestamp">\n\t\t\t\t\t\t{timestamp.strftime("%m/%d/%Y %I:%M %p")}\n\t\t\t\t\t</span>\n\t\t\t\t</h3>\n\t\t\t\t<br>\n\t\t\t\t<h3 class="text">\n\t\t\t\t\t{discord_md(msg["content"])}\n\t\t\t\t</h3>\n\t\t\t</div>\n\t\t</div>'
        last_time = datetime.datetime.fromisoformat(msg['timestamp'][:-6])
        last_author = msg['author']['id']
    html += '\n\t</div>\n</body>\n</html>'
    open(f'{id}.html', 'w').writelines(html)

if __name__ == '__main__':
    write('index')
