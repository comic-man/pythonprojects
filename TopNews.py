import requests
import xml.etree.ElementTree as ET

# url of news rss feed
RSS_FEED_URL = "https://www.patreon.com/rss/LastStandMedia?auth=zst_dTODj8FlqN5Upu-mZYWaBwQoo7cV"

def loadRSS():
    '' ''
    utility function to load RSS feed
    '' ''
    resp = requests.get(RSS_FEED_URL)

    # return response