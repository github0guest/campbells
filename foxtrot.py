import ssl

from bs4 import BeautifulSoup
import requests
import time
import sqlite3
from datetime import timezone, datetime

download_directory = '/Users/shirley/Desktop/foxtrot/'
base_url = 'https://www.gocomics.com'
conn = sqlite3.connect('foxtrot.db')


def warm_up_soup(start_url):
    date_url = start_url
    with open(download_directory + "missing_images.txt", 'w') as f:
        while True:
            print(date_url)
            time.sleep(5)
            try:
                page = requests.get(base_url + date_url)
            except requests.RequestException as ex:
                print(ex)
                print("Error on date: %s" % date_url)
                continue
            soup = BeautifulSoup(page.text, 'html.parser')
            # The div block that has all the good stuff
            select_image_div = soup.select_one('div[data-image]')
            # Transcript collected here
            transcript = select_image_div.attrs['data-transcript']
            # Image URL collected here first
            image_url = select_image_div.attrs['data-image']
            if image_url == "https://assets.gocomics.com/content-error-missing-image.jpeg":
                f.write(date_url + "\n")
                print("Error: Missing image")
                try:
                    date_url = find_next_image(soup)
                except DoneException:
                    break
                continue
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                download_image_update_db(date_url, image_response, transcript)
            try:
                date_url = find_next_image(soup)
            except DoneException:
                break
    conn.close()


def find_next_image(soup):
    # Finds the next URL from the navigation button
    select_next_div = soup.find('a', "fa btn btn-outline-secondary btn-circle fa-caret-right sm ")
    if select_next_div is None:
        raise DoneException()
    return select_next_div.attrs['href']


def download_image_update_db(url, image_response, transcript):
    # Date in YYYY/mm/dd format
    date_slash = str(url.lstrip('/foxtrot/'))
    # Image downloaded here
    with open(download_directory + datetime.strptime(date_slash, '%Y/%m/%d').strftime('%Y-%m-%d') + '.gif', 'wb') as f:
        f.write(image_response.content)
    # Insert the date and transcript into database
    # Convert date to Unix time
    date = datetime.strptime(date_slash, '%Y/%m/%d')
    unix_time = datetime(date.year, date.month, date.day, tzinfo=timezone.utc).timestamp()
    insert_row(unix_time, transcript, conn)


def insert_row(date, transcript, connection):
    c = connection.cursor()
    values = (date, transcript)
    c.execute('REPLACE INTO comics VALUES (?,?)', values)
    connection.commit()


class DoneException(Exception):
    pass


warm_up_soup('/foxtrot/1996/04/13')
