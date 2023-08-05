import re
import json
import os
import shutil
import requests
from joblib import Parallel, delayed
import random
import logging
import sys
import uuid
from PIL import Image

class DuckDuckGoImages:
    URL = "https://duckduckgo.com/"
    
    def download(self, query, folder='.', remove_folder=False, max_urls=None, thumbnails=False, shuffle=False, parallel_download=False):
        if thumbnails:
            urls = self.get_image_thumbnails_search_urls(query)
        else:
            urls = self.get_image_search_urls(query)
        
        if shuffle:
            random.shuffle(urls)
        
        if max_urls is not None and len(urls) > max_urls:
            urls = urls[:max_urls]
            
        if remove_folder:
            self.remove_folder(folder)
        
        self.create_folder(folder)
        if parallel_download:
            self.parallel_download_urls(urls, folder)
        else:
            self.download_urls(urls, folder)

    def _download(self, url, folder):
            try:
                filename = str(uuid.uuid4().hex)
                while os.path.exists("{}/{}.jpg".format(folder, filename)):
                    filename = str(uuid.uuid4().hex)

                response = requests.get(url, stream=True, timeout=1.0, allow_redirects=True)
                with open("{}/{}.jpg".format(folder, filename), 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                    del response
                    
                # validate if the file is a valid one
                try:
                    img =  Image.open("{}/{}.jpg".format(folder, filename))
                    img.close()
                except Image.UnidentifiedImageError:
                    os.remove("{}/{}.jpg".format(folder, filename))
            except:
                pass
    
    def download_urls(self, urls, folder):
        for url in urls:
            self._download(url, folder)

    def parallel_download_urls(self, urls, folder):
        Parallel(n_jobs=32, prefer="threads")(delayed(self._download)(url, folder) for url in urls)

    def get_image_search_urls(self, query):
        token = self.fetch_token(query)
        return self.fetch_search_urls(query, token)
    
    def get_image_thumbnails_search_urls(self, query):
        token = self.fetch_token(query)
        return self.fetch_search_urls(query, token, what="thumbnail")
    
    def fetch_token(self, query):
        res = requests.post(self.URL, data={'q': query})
        if res.status_code != 200:
            return ""
        match = re.search(r"vqd='([\d-]+)'", res.text, re.M|re.I)
        if match is None:
            return ""
        return match.group(1)
    
    def fetch_search_urls(self, query, token, what="image"):
        query = {
            "vqd": token,
            "q": query,
            "l": "wt-wt",
            "o": "json",
            "f": ",,,",
            "p": "2"
        }
        urls = []

        res = requests.get(self.URL+"i.js", params=query)
        if res.status_code != 200:
            return urls

        data = json.loads(res.text)
        for result in data["results"]:
            urls.append(result[what])

        while "next" in data:
            res = requests.get(self.URL+data["next"], params=query)
            if res.status_code != 200:
                return urls
            data = json.loads(res.text)
            for result in data["results"]:
                urls.append(result[what])
        return urls
    
    def remove_folder(self, folder):
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
            
    def create_folder(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)