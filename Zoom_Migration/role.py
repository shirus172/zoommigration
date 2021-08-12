import app
import logging
import json
import config
from datetime import datetime, timedelta

#configure variables
fromAccount = config.FROMACCOUNTID
toAccount= config.TOACCOUNTID
DO_NOT_REPLICATE_ROLE=config.DO_NOT_REPLICATE_ROLE


"""
get a value from the response of list roles and add it to a list and return that list
"""
def get_role_value(fromAccount, key):
    logging.info("Get Roles")
    values = []
    url = '/roles/'
    response = app.send_get_request(url, fromAccount)
    encoded_data=json.loads(response)
    for item in encoded_data['roles']:
        value = item[key]
        if item not in DO_NOT_REPLICATE_ROLE:
            values.append(value)
    return(values)

"""
Get the settings of a particular role and return them
"""
def get_role_settings(fromAccount, roleID):
    logging.info("Get Role Settings")
    url = '/roles/%s' % roleID
    response = app.send_get_request(url, fromAccount)
    return(response)

"""
Update the settings of a specific role
"""
def update_role_settings(accountID, roleID, payload):
    logging.info("update role settings")
    url = '/roles/%s' % roleID
    payload = payload 
    response = app.send_patch_request(url, payload, accountID)
    return(response)

"""
Create a role
"""
def create_role(accountID, name):
    logging.info("Create Role")
    url = '/roles'
    payload = {"name" : "%s" % name} 
    response = app.send_post_request(url, payload, accountID)
    return(response)

def match_roles(fromAccount, toAccount):
    roles = get_role_value(fromAccount, "id")
    for role in roles:
        roleID = get_role_value(fromAccount, "id")
        roleName = get_role_value(fromAccount, "name")
        payload = get_role_settings(fromAccount, roleID)
        response = create_role(toAccount, roleName)
        encoded_data=json.loads(response)
        for item in encoded_data['properties']:
            toRoleID = item["id"]
        update_role_settings(toAccount, toRoleID, payload)




