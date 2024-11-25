from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth, CreateFolderParent, UploadFileAttributes, UploadFileAttributesParentField
from dotenv import load_dotenv
from io import BytesIO
from pydub import AudioSegment
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

training_folders = client.folders.get_folder_items(bullfrog_training_folder_id)

for training_set in training_folders.entries:
    subfolders = client.folders.get_folder_by_id(training_set.id)
    print(subfolders.item_collection.entries)
    for item in subfolders.item_collection.entries:
        neg_pos_folders = client.folders.get_folder_items(item.id)
        new_folder = client.folders.create_folder(name=f'{item.name}_5_seconds',parent= CreateFolderParent(id=item.id))
        
        for audio_file in neg_pos_folders.entries:
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

            file_to_upload = new_audio.export(f'{audio_file.name}',format='wav')
            client.uploads.upload_file(
                UploadFileAttributes(
                    name=audio_file.name, parent=UploadFileAttributesParentField(id=new_folder.id)
                ), 
                file_to_upload
            )
        

