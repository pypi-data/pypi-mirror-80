import requests
import os
import zipfile
import tensorflow as tf
import random
import string
import shutil
from tqdm import tqdm

API_DOMAIN = 'https://api.makinas.io'

class Client:

    def __init__(self, api_domain=API_DOMAIN,
                 makinas_key_id=None, makinas_secret=None,
                 makinas_session_token=None):
        self.domain = api_domain


    @staticmethod
    def _download_file(url, progress=False):
        chunksize = 8192
        local_filename = url.split('/')[-1]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            len = int(r.headers.get('content-length', 0))
            pbar = tqdm(total=len, unit='iB', unit_scale=True)
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=chunksize):
                    if chunk:
                        f.write(chunk)
                        pbar.update(chunksize)
            pbar.close()
        return local_filename


    def get_model(self, model_id):
        return self._download_file(self.domain + '/model/' + model_id)


    def push_model(self, model, model_id=None):
        # Save model
        tmpdir = ''.join(random.choices(string.ascii_letters, k=10))
        #tf.logging.set_verbosity(tf.logging.WARN)
        tf.saved_model.save(model, os.path.join(os.getcwd(), tmpdir))
        # Zip model
        zipf = zipfile.ZipFile(tmpdir+'.zip', 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(tmpdir):
            for file in files:
                zipf.write(os.path.join(root, file))
        zipf.close()
        # Upload model
        url = self.domain+"/model"
        if model_id is not None:
            url += "/"+model_id
        r = requests.post(url)
        assert r.status_code in [200, 201]
        rsp = r.json()
        putUrl = rsp['url']
        if model_id is None:
            model_id = rsp['id']
        with open(tmpdir+'.zip', 'rb') as zf:
            r = requests.put(putUrl, data=zf.read())
        # Cleanup
        shutil.rmtree(tmpdir)
        os.remove(tmpdir+'.zip')
        return model_id
