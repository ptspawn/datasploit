#!/usr/bin/env python

# Response Codes
# 200 - OK 	The request was successful.
# 202 - Accepted 	The request was successful and it is currently being processed.
# 400 - Bad Request 	There was an issue with the request that was provided.
# 401 - Unauthorized 	You have not provided valid credentials for this resource or provided them improperly.
# 403 - Forbidden 	The credentials you provided are valid but either you do not have access to this resource, or you have exceeded your allotted usage.
# 404 - Not Found 	No data could be found.
# 429 - Too Many Requests 	The request is denied because you have reached your request rate limit.
# 50X - Server Error 	Something is broken on FullContact's side. If you encounter this, please contact us at support@fullcontact.com for assistance.


import json
import sys

import requests
import vault
from termcolor import colored

ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def main(email):
    fullcontact_api = vault.get_key('fullcontact_api')
    if fullcontact_api is not None:
        obj = json.dumps({"email": email}, )
        req = requests.post("https://api.fullcontact.com/v3/person.enrich",
                            headers={"Authorization": "Bearer " + fullcontact_api}, data=obj)
        data = json.loads(req.content)
        return data
    else:
        return [False, "INVALID_API"]


def banner():
    print(colored(style.BOLD + '\n---> Checking Fullcontact..\n' + style.END, 'blue'))


def _select_handler(data):
    if type(data) == dict:
        _handle_dict(data)
    elif type(data) == list:    
        _handle_list(data)
    else:
        _handle_values(data)


def _handle_dict(data):
    for key in data.keys():
        value = data.get(key)
        if not value:
            continue
        print(key + ":")
        _select_handler(value)

    
def _handle_list(data):
    for elem in data:
        _select_handler(elem)
    

def _handle_values(elem):    
    print(" - " + elem + "\n")


def output(data, email=""):
    if type(data) == list and data[1] == "INVALID_API":
        print(colored(
            style.BOLD + '\n[-] Full-Contact API Key not configured. Skipping Fullcontact Search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END,
            'red'))
    else:
        status = data.get("status")
        if status is None or status in [200, 201, 202]:
            _select_handler(data)
            # TODO: print the output like the former implementation
            # 
            # 
            # if data.get("contactInfo", "") != "":
            #     print("Name: %s" % data.get("contactInfo", "").get('fullName', ''))
            # print("\nOrganizations:")
            # for x in data.get("organizations", ""):
            #     if x.get('isPrimary', ''):
            #         primarycheck = " - Primary"
            #     else:
            #         primarycheck = ""
            #     if x.get('endDate', '') == '':
            #         print("\t%s at %s - (From %s to Unknown Date)%s" % (
            #             x.get('title', ''), x.get('name', ''), x.get('startDate', ''), primarycheck))
            #     else:
            #         print("\t%s - (From %s to %s)%s" % (
            #             x.get('name', ''), x.get('startDate', ''), x.get('endDate', ''), primarycheck))
            # if data.get("contactInfo", "") != "":
            #     if data.get("contactInfo", "").get('websites', '') != "":
            #         print("\nWebsite(s):")
            #         for x in data.get("contactInfo", "").get('websites', ''):
            #             print("\t%s" % x.get('url', ''))
            #     if data.get("contactInfo", "").get('chats', '') != "":
            #         print('\nChat Accounts')
            #         for x in data.get("contactInfo", "").get('chats', ''):
            #             print("\t%s on %s" % (x.get('handle', ''), x.get('client', '')))
            # 
            # print("\nSocial Profiles:")
            # for x in data.get("socialProfiles", ""):
            #     print("\t%s:" % x.get('type', '').upper())
            #     for y in x.keys():
            #         if y != 'type' and y != 'typeName' and y != 'typeId':
            #             print('\t%s: %s' % (y, x.get(y, '')))
            #     print('')
            # 
            # print("Other Details:")
            # if data.get("demographics", "") != "":
            #     print("\tGender: %s" % data.get("demographics", "").get('gender', ''))
            #     print("\tCountry: %s" % data.get("demographics", "").get('country', ''))
            #     print("\tTentative City: %s" % data.get("demographics", "").get('locationGeneral', '').encode('utf-8'))
            # 
            # print("Photos:")
            # for x in data.get("photos", ""):
            #     print("\t%s: %s" % (x.get('typeName', ''), x.get('url', '')))

        else:
            print('Error Occured - Encountered Status Code: %s. Please check if Email_id exist or not?' % data.get(
                "message",
                ""))


if __name__ == "__main__":
    try:
        email = sys.argv[1]
        banner()
        result = main(email)
        output(result, email)
    except Exception as e:
        print(e)
        print("Please provide an email as argument")
