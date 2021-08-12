from Python.Zoom_Migration.config import FROMACCOUNTID, FROM_API_KEY, TOACCOUNTID, TO_API_KEY
from Python.Zoom_Migration.role import match_roles
from Python.Zoom_Migration.group import match_groups
from Python.Zoom_Migration.account import match_account_settings
import requests
import logging
import jwt
import json
import pytz
from datetime import datetime, timedelta

import config
import account
import group
import role

#confiigure variables
API_KEY = config.API_KEY
API_SECRET = config.API_SECRET
API_ALG = config.API_ALG
JWT_EXPIRY = config.JWT_EXPIRY
BASE_URL = config.BASE_URL
TIMEZONE = config.TIMEZONE

"""
This configuration will save a log file into the same folder as the *.py file
"""
logging.basicConfig(filename='./logs/ZoomMigration.log',level=logging.DEBUG, format='%(levelname)s %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Function to create JWT Token

def jwt_token(accountID):
    if accountID == FROMACCOUNTID:
        API_KEY = FROM_API_KEY
    if accountID == TOACCOUNTID:
        API_KEY == TO_API_KEY
    exp_time = datetime.utcnow() + timedelta(seconds =JWT_EXPIRY)
    payload = {'iss' : API_KEY, 'exp' : exp_time}
    headers = {'alg' : 'HS256', 'typ' : 'JWT'}
    token = str(jwt.encode(headers = headers, payload = payload, key = API_SECRET, algorithm = 'HS256'), 'utf-8')
    return(token)

# REQUEST FUNCTIONS

"""
Get JWT token, assemble headers, assemble endpoint URL, Log URL and Headers, send get request.
If status is not 200 log warning otherwise log response content as info
return response content
"""
def send_get_request(endpoint, accountID):
    token = jwt_token(accountID)
    headers  = {"authorization" : "Bearer %s" % token, "content-type" : "application/json"}
    FINAL_URL = BASE_URL + endpoint
    logging.debug("'{0}', '{1}'".format(FINAL_URL, headers))
    r = requests.get(FINAL_URL, headers = headers)
    if r.status_code != 200:
        logging.warning("'{0}'".format(r.content))
    logging.info("'{0}'".format(r.content))
    return r.content

"""
Get JWT token, assemble headers, assemble endpoint URL, Log URL and Headers, send patch request with payload.
If status is not 200 log warning otherwise log response content as info
return response content
"""
def send_patch_request(endpoint, data, accountID):
    token = jwt_token(accountID)
    headers  = {'authorization' : 'Bearer %s' % token, 'content-type' : 'application/json'}
    FINAL_URL = BASE_URL + endpoint
    logging.debug("'{0}', '{1}', '{2}'".format(FINAL_URL, headers, data))
    r = requests.patch(FINAL_URL, headers = headers, data = data)
    if r.status_code != 200:
        logging.warning("'{0}'".format(r.content))
    logging.info("'{0}'".format(r.content))
    return r.content

"""
Get JWT token, assemble headers, assemble endpoint URL, Log URL and Headers, send post request with payload.
If status is not 200 log warning otherwise log response content as info
return response content
"""
def send_post_request(endpoint, data, AccountID):
    token = jwt_token(AccountID)
    headers  = {'authorization' : 'Bearer %s' % token, 'content-type' : 'application/json'}
    FINAL_URL = BASE_URL + endpoint
    logging.debug("'{0}', '{1}', '{2}'".format(FINAL_URL, headers, data))
    r = requests.post(FINAL_URL, headers = headers, data = data)
    if r.status_code != 200:
        logging.warning("'{0}'".format(r.content))
    logging.info("'{0}'".format(r.content))
    return r.content

""""
Run the matchine scripts for each portion as defined in the config file
"""
def app():
    if config.migrate_setting == True:
        match_account_settings()
    if config.migrate_groups == True:
        match_groups()
    if config.migrate_roles == True:
        match_roles()
       


"""
Run app function
"""
app()
