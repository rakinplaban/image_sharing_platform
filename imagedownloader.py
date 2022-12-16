import requests

r = requests.get("https://i.pinimg.com/736x/d9/ed/94/d9ed9494c8675919343c36f942cb1ec5.jpg")

with open('sunset.jpg','wb') as f:
    f.write(r.content)