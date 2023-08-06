import boto3
import os
from io import BytesIO
import shutil
import zipfile
from botocore.client import Config
try:
    from server.keys import Bucket, KEY, SecretKey
except:
    from keys import Bucket, KEY, SecretKey

from pathlib import Path
s3 = boto3.client('s3', aws_access_key_id=KEY, aws_secret_access_key=SecretKey)
s3.callback_mone = 0

def s3_callback(chunk):
    s3.callback_mone += chunk
    print(s3.callback_mone / 1000000, 'Mg')

def s3_create_callback():
    s3.callback_mone = 0
    return s3_callback

def above(some_path):
    return os.path.join('..', some_path)

def get_server_dict(bucket = Bucket, full_data = False):
    files = [{}]
    res = s3.list_objects(Bucket = bucket, MaxKeys=2000)['Contents']
    for obj in res:

        obj_path = obj['Key'].split('/')
        if obj_path[-1] != '':
            temp = files

            for i in range(len(obj_path)-1):
                if obj_path[i] not in temp[0]:
                    temp[0][obj_path[i]] = [{}]
                temp = temp[0][obj_path[i]]
            if full_data:
                obj['file_name'] = obj_path[-1]
                temp.append(obj)
            else:
                temp.append(obj_path[-1])

    return files

def upload_file(file_name, bucket, object_name):
    s3.upload_file(
    file_name, bucket, object_name, {'Metadata': {'mykey': 'myvalue'}}, s3_create_callback())

def updatable(folder_path):
    # print(folder_path)
    flag = True
    for s in ['temp', 'server/server_data', 'server\server_data']:
        if folder_path.startswith(s):
            flag = False
    for s in ['__pycache__', '.ipynb_checkpoints']:
        if s in folder_path:
            flag = False
    return flag

def upload_folder(folder_path, server_path, o = {}, bocket = Bucket):

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for dirname, subdirs, files in os.walk(folder_path):
            full_dir_path = dirname
            dirname = os.path.relpath(dirname, start=folder_path)

            if updatable(dirname):
                for filename in files:
                    zf.write(os.path.join(full_dir_path, filename), os.path.relpath(os.path.join(full_dir_path, filename), start=folder_path))
        zf.close()
        zip_buffer.seek(0)
        s3.upload_fileobj(zip_buffer, bocket, server_path, {'Metadata': {'a': 'v'}}, s3_create_callback())


def empty_folder(folder_path = above('')):
    for dirname, subdirs, files in os.walk(os.path.abspath(folder_path)):
        for filename in files:
            os.remove(os.path.join(dirname, filename))

        for dir in subdirs:
            if updatable(dir) and dir != 'server':
                shutil.rmtree(os.path.join(dirname, dir))

        break


def restore(folder_path, server_path='', bucket=Bucket):
    empty_folder(folder_path)
    zp = BytesIO()
    s3.download_fileobj(bucket, server_path, zp)
    x = zipfile.ZipFile(zp)
    for name in x.namelist():
        Path('/'.join(name.split('/')[:-1])).mkdir(parents=True, exist_ok=True)
        # if 'S3' not in name:
        with open(name, 'wb') as f:
            f.write(x.read(name))

if __name__ == '__main__':


    upload_folder(above(''), 'wi.zip')
    empty_folder()

    restore(os.path.join('..', ''), 'wi.zip')


