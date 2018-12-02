#!/usr/bin/python3

import os
import requests

TWITCH_AUTH = os.environ['TWITCH_AUTH']
TWITCH_CLIENT = os.environ['TWITCH_CLIENT']

class ValidNames:
    def __init__(self, filepath, file_write_path):
        self.filepath = filepath
        self.file_write_path = file_write_path

    # function to create an array with all valid names
    def create_valid_names(self, option='twitch'):
        if ("TWITCH_AUTH" not in os.environ or "TWITCH_CLIENT" not in os.environ):
            print ('Environment variables not set')
            return

        valid_names = []

        # read in the names
        with open(self.filepath, 'r') as fp:
            headers = {}
            alist = [line.rstrip() for line in fp]

            for username in alist:
                print (username)

                if option == 'twitch':
                    url = 'https://api.twitch.tv/kraken/users?login=%s'%(username)
                    headers = {
                        'Accept': 'application/vnd.twitchtv.v5+json',
                        'Client-ID': TWITCH_CLIENT,
                    }
                    r = requests.get(url, headers=headers)
                else:
                    # form_string = 'username=%s'(username)
                    url = 'https://fortnite-public-api.theapinetwork.com/prod09/users/id'
                    headers = {
                        'Authorization': TWITCH_AUTH,
                        'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
                        'X-Fortnite-API-Version': 'v1.1'
                    }
                    payload = {
                        'form': 'username=%s'%(username)
                    }
                    r = requests.post(url, headers=headers, data=payload)

                data = r.json()
                print (data)

                # check and do certain thing with data if it's 
                # a twitch request or an epic request
                if option == 'twitch':
                    if data['_total'] == 0:
                        valid_names.append(username)

        return valid_names

    def write_valid_usernames(self, usernames):
        with open(self.file_write_path, 'w') as fw:
            fw.writelines("%s\n" % l for l in usernames)
            print ('Done.')


filepath = './usernames.txt'
file_write_path = './valid_usernames.txt'

v = ValidNames(filepath, file_write_path)

valid_name_array = v.create_valid_names()
v.write_valid_usernames(valid_name_array)

print(valid_name_array)


