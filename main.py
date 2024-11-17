from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('DEVELOPER_TOKEN')
print(token)
auth = BoxDeveloperTokenAuth(token=token)
client = BoxClient(auth=auth)

bullfrog_training_folder_id='293782113236'
coyote__training_folder_id='293777823612'
woodhouse_toad_training_folder_id = '293921660447'
# pacific_chorus_frog__training_folder_id = ''

os.makedirs('training_sets', exist_ok=True)

training_folders = client.folders.get_folder_items(bullfrog_training_folder_id)
os.makedirs(os.path.join('training_sets', 'bullfrog'), exist_ok=True)

for training_set in training_folders.entries:
    subfolders = client.folders.get_folder_by_id(training_set.id)
    os.makedirs(os.path.join('training_sets/bullfrog', training_set.name),exist_ok=True)

    for item in subfolders.item_collection.entries:
        neg_pos_folders = client.folders.get_folder_items(item.id)
        os.makedirs(os.path.join(f'training_sets/bullfrog/{training_set.name}', item.name), exist_ok=True)

        for audio_file in neg_pos_folders.entries:
            audio_clip = client.downloads.download_file(audio_file.id)

            with open(f'training_sets/bullfrog/{training_set.name}/{item.name}/{audio_file.name}', 'bw') as new_file:
                for chunk in audio_clip:
                    new_file.write(chunk)

            #this is where the audio padding code should go

folder = client.folders.get_folder_items('293780792480')
print(folder)