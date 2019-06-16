import requests
import h5py

def download_figshare(file_id, file_name=None):
    
    downloaded = 0.0
    try:
        article_url = 'https://api.figshare.com/v2/articles/8281070/files/{}'.format(file_id)
        article_response = requests.get(article_url)
        
        name = article_response.json()['name']
        
        if name and not file_name:
            file_name = name
        elif not file_name:
            file_name = 'generic.h5'
        
        size_in_bytes = float(article_response.json()['size'])
        
        print('File name: {}\nFile size: {:.2f}MB'.format(name, float(article_response.json()['size'])/(1024**2)))
        
        url = 'https://api.figshare.com/v2/file/download/{}'.format(file_id)
        
        print('Locating file...')
        response = requests.get(url, stream=True)
        print('Done!')
    except Exception as e:
        print('Error while trying to download file: {}'.format(e))
    try:
        print('Downloading file to {}'.format(file_name))
        with open(file_name, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=1024**2):
                downloaded += 1024**2
                fd.write(chunk)
                percent = (downloaded * 100) / size_in_bytes
                if percent > 100:
                    percent = 100
                print('{:.2f}%'.format(percent), end='\r')
        print('\nDone!')
    except Exception as e:
        print('Error while trying to write file: {}'.format(e))
