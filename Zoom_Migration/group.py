from Python.Zoom_Migration.config import DO_NOT_REPLICATE
import app
import logging
import json
import config
from datetime import datetime, timedelta

#configure variables
fromAccount = config.FROMACCOUNTID
toAccount= config.TOACCOUNTID
DO_NOT_REPLICATE=config.DO_NOT_REPLICATE

"""
function to create a group on a specified account with a specified group name
"""
def create_group(accountID, groupName):
    logging.info("Create Group")
    url = '/groups'
    print(url)
    payload = {'name' : '%s' % groupName}
    response = app.send_post_request(url, json.dumps(payload), accountID)
    print(response)
    return(response)

"""
get a list of groups from a speciffied account and add the group id to a list and return that list
Need to modify to allow disabling of certain groups
"""
def list_groups(accountID):
    logging.info("List Groups")
    groups = []
    url = '/groups'
    response = app.send_get_request(url, accountID)
    print('response is : %s' % response)
    encoded_data=json.loads(response)
    for item in encoded_data['groups']:
        group = item['id']
        if group not in DO_NOT_REPLICATE:
            groups.append(group)
    return(groups)

"""
get settings from a specified group on a specified acount
"""
def get_group_settings(accountID, group):
    logging.info("Get Group Settings")
    url = 'groups/%s/settings' % group
    response = app.send_get_request(url, accountID)
    return(response)

"""
update the settings of a specified group on a specified account with a specified payload
"""
def update_group_settings(accountID, group, payload):
    logging.info("Update Group Settings: %s : %s" % accountID, group)
    url = '/groups/%s/settings' % group
    response = app.send_patch_request(url, json.dumps(payload), accountID)
    return(response)

"""
Match Group settings in fromAccount to group settings in toAccount
"""

def match_groups(fromAccount,toAccount):
    groups=list_groups(fromAccount)
    for group in groups:
        logging.info("match groups: from %s : %s to %s : %s" % fromAccount, group, toAccount, group)
        payload = get_group_settings(fromAccount,group)
        create_group(toAccount, group)
        response = create_group(toAccount, group)
        encoded_data=json.loads(response)
        for item in encoded_data:
            toRoleID = item["id"]
            update_group_settings(toAccount, toRoleID, payload)

