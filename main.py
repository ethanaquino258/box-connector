from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('DEVELOPER_TOKEN')
auth = BoxDeveloperTokenAuth(token=token)
client = BoxClient(auth=auth)

for item in client.folders.get_folder_items('0').entries:
    print(item.name)

file_id = '1700350086517'

file = client.downloads.download_file(file_id)
print(file)

with open('myfile.wav', 'bw') as new_file:
    for chunk in file:
        new_file.write(chunk)