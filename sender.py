import requests
from random import randint
import time
import codecs
import os
import base64


def send_data(encoded_value):   
    data = '{"records":[{"key":"key1", "value":' + '"' + encoded_value + '"' + '}]}'
    # data = encoded_value
    # print(data)

    response = requests.post('http://my-bridge-route-kafka-analytics.apps.adkadam-ocp1.shiftstack.com/topics/my-topic', headers=headers, data=data)
    print(response.text)    

    

headers = {
    'content-type': 'application/vnd.kafka.json.v2+json',
}

path = "/home/adkadam/kafka-analytics/video/"
i = 0
for filename in os.listdir(path):
    if i == 0:
        if filename == "index.m3u8":
            with open(os.path.join(path, filename), 'rb') as f:
                playlist = f.read()
                playlist_encode = base64.b64encode(playlist)
                send_data(filename + str(playlist_encode, 'utf-8'))
                i += 1
    else:
        if filename.startswith("segment"):
            with open(os.path.join(path, filename), 'rb') as f:
                segment = f.read()
                segment_encode = base64.b64encode(segment)
                send_data(filename + str(segment_encode, 'utf-8'))
                i += 1




# response = requests.post('http://my-bridge-route-kafka-analytics.apps.adkadam-ocp1.shiftstack.com/topics/my-topic', headers=headers, data=data)


# print(response.text)

# video = open('webcam_output.mp4', 'rb')
# video_read = video.read()

# video_64_encode = base64.encodestring(video_read)

# print(video_64_encode)
# value = str(randint(0,100))



    




