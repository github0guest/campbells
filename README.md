# Campbells
Transcript search for the [Foxtrot comic strip](https://en.wikipedia.org/wiki/FoxTrot).
Campbells is named after the web scraper [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) which started it all.


### Introduction
As a kid, I read a daily comic strip called Foxtrot and owned nearly all of the collections (nearly 1 comic a day from 1988-2006). However I often found it difficult to find a specific comic when it came to mind.

A few months ago I discovered that nearly all of the comics strips were published since the comic's [inception in 1988](https://www.gocomics.com/foxtrot/1988/04/11). Right-clicking on the image revealed that it was unable to be saved directly. But the image URL *along with the transcripts of character dialogue* were available in the DOM.

I had just heard of the Python library Beautiful Soup, a scraper for HTML and XML files, and thought to use it to gather image URLs and the associated dialogues.

### File overview

##### foxtrot.py
Scrapes DOM, fetches image, associates it with the published date, the character dialogue, and inserts these into a database

##### storage.py
Provides function which searches transcripts for a given search term and returns dates (the unique identifier of the comic strips)

##### web.py
[Flask](http://flask.pocoo.org/docs/1.0/) application exposing APIs for searching transcript and (the beginnings of) pagination


### Miscellaneous
This Python webserver is hosted on pythonanywhere.com
 
Please see the corresponding front-end: https://github.com/shirleyleu/shirleyleu.github.io
