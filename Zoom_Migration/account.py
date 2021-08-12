import app
import logging
import json
import config
from datetime import datetime, timedelta


#configure variables
fromAccount = config.FROMACCOUNTID
toAccount= config.TOACCOUNTID

"""
Get the account settings for a specific account and return them
"""
def get_account_settings(accountID):
    logging.info("Get Account Settings")
    url = '/settings'
    #print(url)
    response = app.send_get_request(url, accountID)
    data = response
    encoded_data = json.loads(data)
    #print(encoded_data)
    return(encoded_data)

"""
Change the account settings of a specified account to the settings defined in the payload
"""
def update_account_settings(accountID, payload):
    logging.info("Update Account Settings: %s" % accountID)
    url = '/settings'
    data = payload
    response = app.send_patch_request(url, json.dumps(data), accountID)
    print(response)
    return(response)

"""
get the locked settings from a specified account and return that data
"""
def get_locked_settings(accountID):
    logging.info("Get Locked Settings")
    url = "/lock_settings"
    response = app.send_get_request(url, accountID)
    data = response
    encoded_data = json.loads(data)
    #print(encoded_data)
    return(encoded_data)

def update_locked_settings(accountID, payload):
    logging.info("Update Locked Settings: %s" % accountID)
    url = '/settings'
    data = payload
    response = app.send_patch_request(url, json.dumps(data), accountID)
    print(response)
    return(response)

def match_account_settings(fromAccount, toAccount):
    payload = get_account_settings(fromAccount)
    lockedPayload = get_locked_settings(fromAccount)
    update_account_settings(toAccount, payload)
    update_locked_settings(toAccount, lockedPayload)
    logging.info("Match Account Settings: from: %s, to: %s" % fromAccount, toAccount)
