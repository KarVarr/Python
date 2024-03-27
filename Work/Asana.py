import sys
sys.path.append('../Work/api')
from api import my_api
import asana
from asana.rest import ApiException

configuration = asana.Configuration()
configuration.access_token = my_api.token_asana
api_client = asana.ApiClient(configuration)

# Construct resource API Instance
users_api_instance = asana.UsersApi(api_client)
user_gid = "me"
opts = {}

tasks_api_instance = asana.TasksApi(api_client)

try:
    # me = users_api_instance.get_user(user_gid, opts)
    # print('Hello world, its me: ' + me['name'] + "!" )
    
    tasks = tasks_api_instance.get_tasks(opts)
    print("List taksk:")
    for task in tasks:
        print(task)
    

except ApiException as e:
    print("Exception when calling UsersApi->get_user: %s\n" % e)


