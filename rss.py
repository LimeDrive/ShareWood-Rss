#!/usr/bin/env python3
# By LimeCat

# http://localhost:5000/rss/<PASSKEY>/last-torrents?category=1&limit=10
# http://localhost:5000/rss/<PASSKEY>/last-torrents?subcategory=6&limit=10
# http://localhost:5000/rss/<PASSKEY>/search?name=watchmen&subcategory=9&limit=10


from lxml import etree as et
from flask import Flask, request, abort, Response
from retry import retry
# from markupsafe import escape
import requests
import time
import yaml
import humanize

with open('config.yml', 'r') as ymlfile:
    cfgTitle = yaml.load(ymlfile, Loader=yaml.FullLoader)

titleDict = cfgTitle['title']

app = Flask(__name__)

@retry(ValueError, delay=1, jitter=2, tries=4)
def get_Json_Api(arguments, url):
    response = requests.get(url, params=arguments)
    if not response.ok:
        return ValueError
    return response.json()


@app.route('/')
def how_to():
    return '<strong>Exemples :</strong><br>http://localhost:4000/rss/PASSKEY/last-torrents?category=1&limit=10<br>http://localhost:4000/rss/PASSKEY/last-torrents?subcategory=6&limit=10<br>http://localhost:4000/rss/PASSKEY/search?name=watchmen&subcategory=9&limit=10'

@app.route('/rss/<string:passkey>/<string:apiAction>', methods=['GET'])
def return_Rss_File(passkey, apiAction):

    # passkey = os.environ.get("SHAREWOOD_PASSKEY")
    if passkey == None or len(passkey) != 32:
        return abort(404)
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
        subcategory = str(
            subcategory) if subcategory > 8 and subcategory <= 36 else False
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
        url = f"https://www.sharewood.tv/api/{passkey}/last-torrents"
    elif apiAction == "search":
        if name:
            url = f"https://www.sharewood.tv/api/{passkey}/search"
    else:
        return abort(404)

    if category:
        keyTitleDict = category
    elif subcategory:
        keyTitleDict = subcategory
    else:
        keyTitleDict = 0

    rss = et.Element("rss", version="2.0")
    channel = et.SubElement(rss, "channel")
    title = et.SubElement(channel, "title")
    if not name:
        title.text = "ShareWood RSS : " + titleDict.get(str(keyTitleDict))
    else:
        title.text = f"ShareWood Search : {str(name)}"
    description = et.SubElement(channel, "description")
    description.text = "Flux RSS Sharewood"
    lastBuildDate = et.SubElement(channel, "lastBuildDate")
    named_tuple = time.localtime()
    time_string = time.strftime("%Y-%m-%d,%H:%M:%S", named_tuple)
    lastBuildDate.text = time_string
    link = et.SubElement(channel, "link")
    link.text = "https://sharewood.tv"
    apiData = get_Json_Api(arguments, url)
    for torrent in apiData:
        channel.append(et.Comment("News Torrents Item"))
        item = et.SubElement(channel, "item")
        title = et.SubElement(item, "title")
        title.text = str(torrent.get('name'))
        sizeTorrent = torrent.get('size') if type(torrent.get(
            'size')) is str else humanize.naturalsize(torrent.get('size'), binary=True)
        description = et.SubElement(item, "description")
        description.text = f"Nom de l'upload: <strong><a href='https://sharewood.tv/torrents/{str(torrent.get('slug'))}.{str(torrent.get('id'))}'>{torrent.get('name')}</a></strong> <br/> Taille de l'upload: {sizeTorrent}<br/> Status: {str(torrent.get('seeders'))} seeders et {str(torrent.get('leechers'))} leechers <br/> Ajouté le: {torrent.get('created_at')}"
        description.text = et.CDATA(description.text)
        link = et.SubElement(item, "link")
        link.text = f"https://sharewood.tv/torrents/{str(torrent.get('slug'))}.{str(torrent.get('id'))}"
        size = et.SubElement(item, "size")
        size.text = sizeTorrent
        url = f"https://www.sharewood.tv/api/{str(passkey)}/{str(torrent.get('id'))}/download"
        et.SubElement(item, "enclosure", url=url,
                    type="application/x-bittorrent")

    txt = et.tostring(rss, pretty_print=True,
                    encoding='utf-8', xml_declaration=True)

    return Response(txt, mimetype='text/xml')


if __name__ == '__main__':

    app.run(debug=True, port=5000)
