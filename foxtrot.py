from bs4 import BeautifulSoup
import requests
import time


def download_images(start_url):
    base_url = 'https://www.gocomics.com'
    url = start_url
    while True:
        page = requests.get(base_url + url)
        soup = BeautifulSoup(page.text, 'html.parser')
        # Filename is created using URL date
        formatted_date = str(url).lstrip('/foxtrot').replace('/', '-')
        # The div block that has all the good stuff
        select_image_div = soup.select_one('div[data-image]')
        # Transcript collected here
        transcript = select_image_div.attrs['data-transcript']
        with open('/Users/shirley/Desktop/foxtrot/%s' % (formatted_date + '.txt'), 'w') as f:
            f.write(transcript)
        # Image URL collected here first
        image_url = select_image_div.attrs['data-image']
        image_response = requests.get(image_url)
        # Image downloaded here
        if image_response.status_code == 200:
            with open('/Users/shirley/Desktop/foxtrot/%s' % (formatted_date + '.gif'), 'wb') as f:
                f.write(image_response.content)
        # Finds the next URL from the navigation button
        select_next_div = soup.find('a', "fa btn btn-outline-secondary btn-circle fa-caret-right sm ")
        if select_next_div == None:
            break
        url = select_next_div.attrs['href']
        time.sleep(5)
