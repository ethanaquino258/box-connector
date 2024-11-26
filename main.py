from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth, CreateFolderParent, UploadFileAttributes, UploadFileAttributesParentField
from dotenv import load_dotenv
from pydub import AudioSegment
import os
import io
from io import BytesIO

load_dotenv()

token = os.getenv('DEVELOPER_TOKEN')
print(token)
auth = BoxDeveloperTokenAuth(token=token)
client = BoxClient(auth=auth)

bullfrog_folder_id='293779149413'
bullfrog_training_folder_id = '293782113236'
coyote_folder_id=''
coyote_training_folder_id = '293777823612'
woodhouse_toad_folder_id = ''
woodhouse_toad_trianing_folder_id = '293921660447'
pacific_chorus_frog_training_folder_id = ''

main_folder = client.folders.get_folder_items(bullfrog_folder_id)

training_folders = client.folders.get_folder_items(bullfrog_training_folder_id)
# print(training_folders.entries)
matching_folder = next((entry for entry in main_folder.entries if entry.name == 'train_5sec'), None)
# print(matching_folder)
if matching_folder:
    fivesec_folder = matching_folder
else:
    fivesec_folder = client.folders.create_folder(name='train_5sec', parent = CreateFolderParent(id = bullfrog_folder_id))

for set in training_folders.entries:
    training_set = client.folders.get_folder_by_id(set.id)
    print(f'Now in: {set.name}')
    fivesec_folder_items = client.folders.get_folder_items(fivesec_folder.id)
    fivesec_matching_folder = next((entry for entry in fivesec_folder_items.entries if entry.name == set.name), None)
    if fivesec_matching_folder:
        new_set = fivesec_matching_folder
    else:
        new_set = client.folders.create_folder(name = f'{set.name}', parent = CreateFolderParent(fivesec_folder.id))

    for neg_pos_folders in training_set.item_collection.entries:
        files = client.folders.get_folder_items(neg_pos_folders.id, limit=500)

        fivesec_folder_negpos_items = client.folders.get_folder_items(new_set.id)
        fivesec_negpos_matching_folder = next((entry for entry in fivesec_folder_negpos_items.entries if entry.name == neg_pos_folders.name), None)
        if fivesec_negpos_matching_folder:
            new_neg_pos_folder = fivesec_negpos_matching_folder
        else:
            new_neg_pos_folder = client.folders.create_folder(name=f'{neg_pos_folders.name}',parent= CreateFolderParent(id=new_set.id))
       
        print(f'Now in: {neg_pos_folders.name}')
       

        for audio_file in files.entries:

            fivesec_audio_files = client.folders.get_folder_items(new_neg_pos_folder.id, limit = 500)
            
            audio_file_names = {entry.name for entry in fivesec_audio_files.entries}
            if audio_file.name in audio_file_names:
                continue
            else:
                audio_clip = client.downloads.download_file(audio_file.id)
                audio_buffer = BytesIO()
                for chunk in audio_clip:
                    audio_buffer.write(chunk)
                
                audio_buffer.seek(0)
                audio = AudioSegment.from_file(audio_buffer)
                if len(audio) < 5000:
                    total_padding = 5000 - len(audio)
                    padding_start = total_padding // 2
                    padding_end = total_padding - padding_start

                new_audio = AudioSegment.silent(duration=padding_start) + audio + AudioSegment.silent(duration=padding_end)
                upload_buffer = io.BytesIO()
                new_audio.export(upload_buffer,format='wav')
                upload_buffer.seek(0)
                client.uploads.upload_file(
                    UploadFileAttributes(
                        name=audio_file.name, parent=UploadFileAttributesParentField(id=new_neg_pos_folder.id)
                    ), 
                    upload_buffer
                )
        

