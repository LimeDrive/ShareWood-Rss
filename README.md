# ShareWood Rss Fetch

Sarewood API to RSS for torrents clients auto-dl

## Install

### Docker : 

```
docker run -d --name=sharewood -p 4000:4000 limedrive/sharewood-rss
```

### Docker-compose : 

```yml
---
version: "3.8"
services: 
  sharewood:
    container_name: sharewood
    image: limedrive/sharewood-rss
    restart: on-failure
    ports:
      - '4000:4000'
```

## Usage :

Same as the api, simply replace https://www.sharewood.tv/api by http://localhost:4000/rss if you are in local or by your domaine name and path /rss/ ( exemple : https://myprettydomain/rss/PASSKEY/last-torrents?category=1 )

enjoy ;)
