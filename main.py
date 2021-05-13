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
# from markupsafe import escape
import requests
import os
import time
import yaml

passkey = os.environ.get("SHAREWOOD_PASSKEY")
app = Flask(__name__)

# Create xml file with the api info. TODO


def prase_Xml_file(apiData, passkey, category, subcategory, name):
    # For correct title.
    with open('config.yml', 'r') as ymlfile:
        cfgTitle = yaml.load(ymlfile, Loader=yaml.FullLoader)
    titleDict = dict()
    titleDict = cfgTitle['title']
    keyTitleDict = str(category) if category is True else str(
        subcategory) if subcategory is True else str(0)
    
    rss = et.Element("rss", version="2.0")
    channel = et.SubElement(rss, "channel")
    title = et.SubElement(channel, "title")
    if not name: 
        title.text = f"ShareWood RSS : {titleDict.get(keyTitleDict)}"
    else:
        title.txt = f"ShareWood Search : {str(name)}"
    description = et.SubElement(channel, "description")
    description.text = "Flux RSS Sharewood"
    lastBuildDate = et.SubElement(channel, "lastBuildDate")
    lastBuildDate.text = str(time.ctime)
    link = et.SubElement(channel, "link")
    link.text = "https://sharewood.tv"
    for torrent in apiData:
        et.Comment("News Torrents Item")
        item = et.subElement(channel, "item")
        title = et.SubElement(item, "title")
        title.text = str(torrent.get('name'))
        descrition = et.SubElement(item, "description")
        descrition.text = str(torrent.get('slug'))
        link = et.SubElement(item, "link")
        link.text = f"https://sharewood.tv/torrents/{str(torrent.get('slug'))}.{str(torrent.get('id'))}"
        size = et.SubElement(item, "size")
        size.text = str(torrent.get('size'))
        url = f"https://www.sharewood.tv/api/{str(passkey)}/{str(torrent.get('id'))}/download"
        et.SubElement(item, "enclosure", url=url, type="application/x-bittorrent")


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
    else:
        return abort(404)

    renderTxt = prase_Xml_file(apiData, passkey, category, subcategory, name)
    return renderTxt

# print(et.tostring(rss, pretty_print=True, encoding='utf-8', xml_declaration=True))


if __name__ == '__main__':
    # init working environement

    app.run(debug=True, port=5000)
