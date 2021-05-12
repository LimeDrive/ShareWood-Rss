#!/usr/bin/env python3
# By LimeCat

#### TODO
## Fonction pour récupérer le dico de l'api.
## Mise en place du serveur flask.

from lxml import etree as et
from flask import Flask, request, send_file, Response

app = Flask(__name__)

@app.route('/rss', methods=['GET'])
def return_Rss_File():
    renderTxt = "rss"
    return renderTxt

# Torrents items block for xml
def get_Torrent_Item(data):
    item = et.Element("item")
    title = et.SubElement(item, "title")
    descrition = et.SubElement(item, "description")
    link = et.SubElement(item, "link")
    dllLink = et.SubElement(item, "dllLink")
    category = et.SubElement(item, "category")
    size = et.SubElement(item, "size")
    return item

# Simule api data
apiData = [ {}, {}, {} ]

# Create xml file with the api info.
rss = et.Element("rss")
channel = et.SubElement(rss, "channel")
title = et.SubElement(channel, "title")
description = et.SubElement(channel, "description")
lastBuildDate = et.SubElement(channel, "lastBuildDate")
link = et.SubElement(channel, "link")
for torrent in apiData:
    channel.append(et.Comment("News Torrents Items"))
    channel.append(get_Torrent_Item(torrent))



print(et.tostring(rss, pretty_print=True, encoding='utf-8', xml_declaration=True))


if __name__=='__main__':
    # init working environement
    
    app.run(host='0.0.0.0', port=5000)
