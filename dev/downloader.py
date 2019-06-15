import requests
import h5py

def download_hdf5(file_id, file_name=None):
    
    try:
        article_url = 'https://api.figshare.com/v2/articles/8206559/files/{}'.format(file_id)
        article_response = requests.get(article_url)
        
        name = article_response.json()['name']
        
        if name and not file_name:
            file_name = name
        elif not file_name:
            file_name = 'generic.h5'
        
        print('File name: {}\nFile size: {:.2f}MB'.format(name, float(article_response.json()['size'])/(1024**2)))
        
        url = 'https://api.figshare.com/v2/file/download/{}'.format(file_id)
        
        print('Downloading file...')
        response = requests.get(url, stream=True)
        print('Done!')
    except as e:
        print('Error while trying to download file: {}'.format(e))
    try:
        print('Saving file as {}'.format(file_name))
        with open(file_name, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)
        print('Done!')
    except as e:
        print('Error while trying to write file: {}'.format(e))
