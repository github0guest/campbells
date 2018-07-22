from bs4 import BeautifulSoup
import requests
import re

url = 'https://www.gocomics.com/foxtrot/1988/04/11'
page = requests.get(url)

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