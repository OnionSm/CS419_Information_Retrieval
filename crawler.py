import requests
from bs4 import BeautifulSoup
import time
import json

DOMAIN = 'https://kenh14.vn'

def craw(url: str, DOMAIN: str, max_retries: int = 3, timeout: int = 10):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; MyCrawler/1.0; +https://yourdomain.com/crawler)"
    }
    retries = 0
    while retries < max_retries:        
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 429:
                print(f"[WARN] 429 Too Many Requests - sleeping 30s ({retries+1}/{max_retries})")
                time.sleep(30)
                retries += 1
                continue
            if response.status_code != 200:
                print(f"[ERROR] Status code: {response.status_code} at {url}")
                return None, None

            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.title.text if soup.title else None
            description_data = soup.find('h2', class_="knc-sapo")
            description = description_data.get_text(strip=True) if description_data else None

            all_content = soup.find('div', class_=["knc-content", "detail-content afcbc-body"])
            content = ""
            if all_content:
                for p_tag in all_content.find_all('p'):
                    content += p_tag.get_text(separator=' ', strip=True) + " "

            # Set tránh trùng link
            list_link = set()
            next_url_tags = soup.find_all('a')
            for link_tag in next_url_tags:
                href = link_tag.get('href')
                if href and href.startswith("/"):
                    link = f"{DOMAIN}{href}"
                    if link.endswith('.chn'):
                        list_link.add(link) 

            if title and description:
                return {"title": title, "description": description, "content": content.strip()}, list(list_link)
            return None, None
        except requests.exceptions.RequestException as ex:
            print(f"[EXCEPTION] Request failed for {url}: {ex}")
            retries += 1
            time.sleep(5)
        except Exception as ex:
            print(f"[EXCEPTION] Other error at {url}: {ex}")
            return None, None
    return None, None
    
current_url = "https://kenh14.vn/dong-thai-tra-dua-cua-nu-than-tuong-bi-che-gia-nai-nhat-kpop-215250528074331524.chn"
visited_urls = set() 
next_urls = set()

craw_data = []
current_index = 0
max_craw = 15000
while (current_url is not None) and (current_index < max_craw):
    if current_url not in visited_urls:
        print(f"Crawling: {current_index} {current_url}")
        visited_urls.add(current_url) 
        data, list_link = craw(current_url, DOMAIN) 
        if list_link:
            for link in list_link:
                next_urls.add(link)
        
        if data:
            data["id"] = current_index
            data["link"] = current_url
            craw_data.append(data)
            print(f"Title: {data['title']}")
            print(f"Description: {data['description']}")
            current_index += 1
    if len(next_urls) > 0:
        current_url = next_urls.pop()
    else:
        current_url = None

    time.sleep(1) 
    if (current_index + 1) % 50 == 0:
        output_file = "data_craw.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(craw_data, f, ensure_ascii=False, indent=4)
        print(f"\nĐã lưu dữ liệu vào file: {output_file}")

output_file = "data_craw.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(craw_data, f, ensure_ascii=False, indent=4)
print(f"\nĐã lưu dữ liệu vào file: {output_file}")