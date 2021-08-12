#Credentials
FROM_API_KEY= ""
FROM_API_SECRET=""

TO_API_KEY= ""
TO_API_SECRET=""

#jwt variables
API_ALG = 'HS256'
TIMEZONE = 'America/Denver'
JWT_EXPIRY = 60
BASE_URL = 'https://api.zoom.us/v2/'

#Account IDs' for Migration
FROMACCOUNTID =""
TOACCOUNTID=""

#List of groups and roles that will not be replicated to sub accounts
# list each group and role  name here
DO_NOT_REPLICATE = ['groupname1','groupname2','groupname3']
DO_NOT_REPLICATE_ROLE = ['rolename1','rolename2','rolename3']

#Boolean migration Settings Set to false if you would not like to migrate specific portions of your configurations
migrate_settings = True
migrate_groups = True
migrate_roles = True