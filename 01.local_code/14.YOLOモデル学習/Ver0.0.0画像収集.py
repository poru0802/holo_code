import requests  
from bs4 import BeautifulSoup  
import os  
import time  
  
def download_image(url, file_path):    
    r = requests.get(url, stream=True)    
    if r.status_code == 200:      
        with open(file_path, "wb") as f:        
            for chunk in r.iter_content(1024):  
                f.write(chunk)  
  
def get_image_urls(page_url):  
    r = requests.get(page_url)  
    soup = BeautifulSoup(r.text, 'html.parser')  
  
    img_tags = soup.find_all("img")  
    img_urls = []  
  
    for img_tag in img_tags:    
        url = img_tag.get("src")    
        if url is not None and not url.startswith('data:'):  # データURLを除外  
            if not url.startswith(('http://', 'https://')):  
                url = 'https://www.bing.com' + url  
            img_urls.append(url)  
  
    return img_urls  
  
# 検索ページURL  
search_word = 'がうるぐら'  
save_file_path = './画像'  
base_url = 'https://www.bing.com/images/search?q={}&first={}'  
num_pages = 10  # ダウンロードするページ数  
images_per_page = 200  # 1ページあたりの画像数  
  
if not os.path.exists(save_file_path):  
    os.makedirs(save_file_path)  
  
img_urls = []  
for page in range(0, num_pages):  
    page_url = base_url.format(search_word, page * images_per_page)
    print(page_url)  
    img_urls.extend(get_image_urls(page_url))  
    time.sleep(1)  # サーバーへの負荷を軽減するための遅延  
  
for index, url in enumerate(img_urls):    
    file_name = "{}.jpg".format(index)    
    print(f'\r{file_name}',end='')    
    image_path = os.path.join(save_file_path, file_name)     
    download_image(url=url, file_path=image_path)  