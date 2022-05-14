import requests
import json
from time import sleep
import tweepy
#from our keys module (keys.py), import the keys dictionary
from keys import keys
from PIL import Image
from os import listdir
from os.path import isfile, join

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']
Bearer = keys['Bearer']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

headers = {
    'Authorization': Bearer,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
}

params = (
##    ('tweet.fields', 'created_at'),
    ('expansions', 'author_id'),
    ('user.fields', 'created_at'),
    ('tweet.fields', 'referenced_tweets')
)

def set_size(file):
    x = 100
    im1 = Image.open(file,mode='r')
    while x > 0:
        im1.save('temp_file.jpg', "JPEG", quality=x)
        with open('temp_file.jpg','rb') as f:
            data = f.read()
        size = len(data)
        if size <= 5000192:
            print('Compression:',x)
            x = 0
        else:
            x -= 1

def upload_file():
    print('uploading')
    file_upload = 'temp_file.jpg'
    response = api.media_upload(file_upload)
    media_id = response.media_id
    medias = []
    medias.append(media_id)
    print('upload done.')
    return medias

mypath ='./share/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
custom_message0 = 'Old picures '
for num,file in enumerate(onlyfiles):
    custom_message1 = str(num+1)+'/'+str(len(onlyfiles))
    #print(custom_message1)
    if num == 0:
        set_size(('./share/' + file))
        medias = upload_file()
        tweet = api.update_status(status = custom_message0 + custom_message1,
                                  media_ids=medias)
    else:
        set_size(('./share/' + file))
        medias = upload_file()
        tweet = api.update_status(status = custom_message1,
                                  media_ids=medias,
                                  in_reply_to_status_id=tweet.id,
                                  auto_populate_reply_metadata=True)
