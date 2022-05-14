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
    while True:
        try:
            sleep(5)
            response = api.media_upload(file_upload)
        except Exception as e:
            print('Failed',e)
            continue
        break
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
