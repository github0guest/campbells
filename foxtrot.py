from bs4 import BeautifulSoup
import requests
import time
import sqlite3
from datetime import timezone, datetime

download_directory = '/Users/shirley/Desktop/foxtrot/'
base_url = 'https://www.gocomics.com'
conn = sqlite3.connect('foxtrot.db')


def main(start_url):
    date_url = start_url
    with open(download_directory + "missing_images.txt", 'a') as f:
        while True:
            time.sleep(5)

            # Converting a URL into soup object
            try:
                page = requests.get(base_url + date_url)
            except requests.RequestException as ex:
                print(ex)
                print("Error on date: %s" % date_url)
                continue
            except ConnectionError as err:
                print(err)
                print("Error on date: %s" % date_url)
                continue
            soup = BeautifulSoup(page.text, 'html.parser')

            # Extract image URL and transcript
            select_image_div = soup.select_one('div[data-image]')
            try:
                transcript = select_image_div.attrs['data-transcript']
            except AttributeError as err:
                print(err)
                print("Error on date: %s" % date_url)
                date_url = find_next_date(soup)
                continue
            image_url = select_image_div.attrs['data-image']

            # Download image
            # Special case: Missing images' dates noted
            if image_url == "https://assets.gocomics.com/content-error-missing-image.jpeg":
                f.write(date_url + "\n")
                print("Error: Missing image")
                try:
                    date_url = find_next_date(soup)
                except DoneException:
                    break
                continue
            # Otherwise, image URL is considered valid and eventually downloaded/DB updated
            try:
                image_response = requests.get(image_url)
            except requests.RequestException as ex:
                print(ex)
                print("Error on date: %s" % date_url)
                continue
            except ConnectionError as err:
                print(err)
                print("Error on date: %s" % date_url)
                continue
            if image_response.status_code == 200:
                download_image_update_db(date_url, image_response, transcript)
            try:
                date_url = find_next_date(soup)
            except DoneException:
                break
    conn.close()


def find_next_date(soup):
    """Find the next date's URL from the navigation button."""
    select_next_div = soup.find('a', "fa btn btn-outline-secondary btn-circle fa-caret-right sm ")
    if select_next_div is None:
        raise DoneException()
    return select_next_div.attrs['href']


def download_image_update_db(url, image_response, transcript):
    """Download image locally and inserts entry in DB."""
    # Date in YYYY/mm/dd format
    date_slash = str(url.lstrip('/foxtrot/'))
    # Image downloaded here
    with open(download_directory + datetime.strptime(date_slash, '%Y/%m/%d').strftime('%Y-%m-%d') + '.gif', 'wb') as f:
        f.write(image_response.content)
    # Convert date to Unix time
    dt_obj = datetime.strptime(date_slash, '%Y/%m/%d')
    unix_time = datetime(dt_obj.year, dt_obj.month, dt_obj.day, tzinfo=timezone.utc).timestamp()
    # Insert the date and transcript into database
    c = conn.cursor()
    values = (unix_time, transcript)
    c.execute('REPLACE INTO comic VALUES (?,?)', values)
    conn.commit()


class DoneException(Exception):
    pass


if __name__ == '__main__':
    pass
