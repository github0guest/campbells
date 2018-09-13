from bs4 import BeautifulSoup
import requests
import re

base_url = 'https://www.gocomics.com'

# Start URL
url = '/foxtrot/1988/04/11'

page = requests.get(base_url + url)
soup = BeautifulSoup(page.text, 'html.parser')
select_div = soup.select_one('div[data-image]')
image_url = select_div.attrs['data-image']
response = requests.get(image_url)

if response.status_code == 200:
    content_disp = response.headers['Content-Disposition']
    filename = re.findall('filename=(.+)', content_disp)
    formatted_filename = str(filename[0]).strip('\"')
    with open('/Users/shirley/Desktop/foxtrot/%s' % formatted_filename, 'wb') as f:
        f.write(response.content)

# Finds the next URL from the navigation button
select_next_div = soup.find('a', "fa btn btn-outline-secondary btn-circle fa-caret-right sm ")
url = select_next_div.attrs['href']