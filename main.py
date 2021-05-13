#!/usr/bin/env python3
# By LimeCat

# TODO
# Fonction pour récupérer le dico de l'api.
# url : une route rss avec fonction /last-torrent et fonction /search
# https://localhost:5000/rss/last-torrent?category=1&limit=10
# https://localhost:5000/rss/last-torrent?subcategory=6&limit=10
# https://localhost:5000/rss/search?name=xxx+xxx&subcategory=6&limit=10
#
# Mise en place du serveur flask.

from lxml import etree as et
from flask import Flask, request, abort
from markupsafe import escape
import requests
import os
import time

passkey = os.environ.get("SHAREWOOD_PASSKEY")
app = Flask(__name__)

# Torrents items block for xml TODO


def get_Torrent_Item(data, passkey):
    item = et.Element("item")
    title = et.SubElement(item, "title")
    descrition = et.SubElement(item, "description")
    link = et.SubElement(item, "link")
    dllLink = et.SubElement(item, "dllLink")
    category = et.SubElement(item, "category")
    size = et.SubElement(item, "size")
    return item

# Create xml file with the api info. TODO


def prase_Xml_file(apiData, passkey):
    rss = et.Element("rss")
    channel = et.SubElement(rss, "channel")
    title = et.SubElement(channel, "title")
    description = et.SubElement(channel, "description")
    lastBuildDate = et.SubElement(channel, "lastBuildDate")
    lastBuildDate.text = str(time.ctime)
    link = et.SubElement(channel, "link")
    for torrent in apiData:
        channel.append(et.Comment("News Torrents Items"))
        channel.append(get_Torrent_Item(torrent))

    return et.tostring(rss, pretty_print=True, encoding='utf-8', xml_declaration=True)


@app.route('/rss/<string:apiAction>', methods=['GET'])
def return_Rss_File(apiAction):
    
    passkey = os.environ.get("SHAREWOOD_PASSKEY")
    arguments = {}
        
    try:
        category = request.args.get("category", "", type=int)
        subcategory = request.args.get("subcategory", "", type=int)
        limit = request.args.get("limit", "", type=int)
        name = request.args.get("name", "", type=str)
    except:
        print(f"bad request args")
        return abort(404)
    
    if category:
        category = str(category) if category <= 7 else False
        if category:
            arguments['category'] = category
        else:
            return abort(404)
    elif subcategory:
        subcategory = str(subcategory) if subcategory > 8 and subcategory <= 36 else False
        if subcategory:
            arguments['subcategory'] = subcategory
        else:
            return abort(404)
    if limit:
        limit = str(limit) if limit <= 25 else str(25)
        arguments['limit'] = limit
    if name:
        arguments['name'] = str(name)

    
    if apiAction == 'last-torrents':
        url = requests.get(f"https://www.sharewood.tv/api/{passkey}/last-torrents", params=arguments)
        print(url.url)
        apiData = url.json()
    elif apiAction == "search":
        if name:
            url = requests.get(f"https://www.sharewood.tv/api/{passkey}/search", params=arguments)
            print(url.url)
            apiData = url.json()
        else:
            return abort(404)

    # return str(apiData)
    renderTxt = prase_Xml_file(apiData)
    return renderTxt

# print(et.tostring(rss, pretty_print=True, encoding='utf-8', xml_declaration=True))


if __name__ == '__main__':
    # init working environement

    app.run(debug=True, port=5000)
