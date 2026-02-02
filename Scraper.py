import requests
from bs4 import BeautifulSoup
import json
import re
import time

def scrape():
    url = 'https://seekingalpha.com/market-news/notable-calls'

    # This makes it look like the request is coming from a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        print("Success!")
        print(soup)
    else:
        print(f"Failed with status code: {response.status_code}")

    #title = soup.select_one('h1').text
    #text = soup.select_one('p').text
    #link = soup.select_one('a').get('href')

    #print('Title:'+ title)
    #print(text)
    #print(link)

    #return{
    #    'title': title,
    #    'text': text,
    #    'link': link
    #}

def scrapeSeekingAlphaNotablePicks():
    # List of sub-urls we want to parse through
    #urls = ['https://seekingalpha.com/market-news/notable-calls']
    urls = ['https://seekingalpha.com/market-news/market-pulse']
    base_url = 'https://seekingalpha.com'
    
    for url in urls:
    # get article links
        article_links = getSeekingAlphaArticleLinks(url, base_url)
        time.sleep(3)
    # snatch article information and save
        article_info = scrapeSeekingAlphaArticleInfo(article_links[0])
        time.sleep(3)
    # give to LLM
        print(article_info)

                
def getSeekingAlphaArticleLinks(url, base_url):
    # return resposne
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    article_links=[]

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the script tag in the html, it uses hydration so the links aren't actually
        # populated until the page loads, but they're in this json
        script_tag = soup.find('script', string=re.compile('window.SSR_DATA'))

        if script_tag:
            # extract the json from the script
            json_text = re.search(r'window.SSR_DATA\s*=\s*({.*?});', script_tag.string, re.DOTALL)

            if json_text:
                data = json.loads(json_text.group(1))

                # navigate through the json
                # gotta go marketNews -> response -> data
                news_items = data.get('marketNews', {}).get('response', {}).get('data', [])

                # go thru every item and grab the link from 'links' -> 'self'
                for item in news_items:
                    relative_link = item.get('links', {}).get('self')
                    if relative_link:
                        article_links.append(base_url + relative_link)
            
        print(f"Successfully extracted {len(article_links)} article links from JSON.")
        return article_links
    else:
        print(f"Failed: {response.status_code}")
        return []

def scrapeSeekingAlphaArticleInfo(article_url):
 # return resposne
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    response = requests.get(article_url, headers=headers)
    response.encoding = 'utf-8' # fixes encoding issues
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the script tag in the html, it uses hydration so the links aren't actually
        # populated until the page loads, but they're in this json
        script_tag = soup.find('script', string=re.compile('window.SSR_DATA'))

        if script_tag:
            # extract the json from the script
            json_text = re.search(r'window.SSR_DATA\s*=\s*({.*?});', script_tag.string, re.DOTALL)

            if json_text:
                data = json.loads(json_text.group(1))

                # navigate through the json
                article_attr = data['article']['response']['data']['attributes']

                # grab the full article
                raw_full_article = article_attr.get('content', '')

                # clean up article content using beautifulsoup
                body_soup = BeautifulSoup(raw_full_article, "html.parser")
                article_body_text = body_soup.get_text(separator='\n').strip()
            
        print(f"Successfully parsed article!")
        return article_body_text
    else:
        print(f"Failed to parse and save article: {response.status_code}")
        return f"Failed to parse article with url {article_url}"




if __name__ == '__main__':
    #scrape()
    scrapeSeekingAlphaNotablePicks()
    