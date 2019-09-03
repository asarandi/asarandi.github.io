#!/usr/bin/env python3

import requests

html_file = "index.html"
m3u8_file = "nrj.m3u8"

def make_m3u8(radios):
    if not radios:
        return
    with open(m3u8_file, "w") as fp:
        print("#EXTM3U\n", file=fp)
        for r in radios:
            print("#EXTINF:-1,%s" % (r["name"],), file=fp)
            print(r["url"],"\n", file=fp)
        fp.close()            

def make_html(radios):
    if not radios:
        return
    before = "<!DOCTYPE html>\n<html>\n<head>\n<meta charset=\"UTF-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n</head>\n<body>\n<ul>"
    after = "</ul>\n</body>\n</html>"
    with open(html_file, "w") as fp:
        print(before, file=fp)
        for r in radios:
            print("<li><a href=\"%s\" target=\"_blank\">%s</a></li>" % (r["url"], r["name"]), file=fp)
        print(after, file=fp);
        fp.close()

def get_radios():
    url = "https://players.nrjaudio.fm/wr_api/live/fr?act=get_setup&id_radio=1&ver=3&cp=utf8&fmt=json"
    req = requests.get(url)
    if req.status_code != 200:
        print("error")
        return
    result = []
    for r in req.json()["webradios"]:
        k = "url_128k_mp3"
        if r[k]:
            result.append({"name": "%s" % (r["name"],), "url": "%s%s" % (r[k], "?origine=playerweb") })
    return result                

if __name__ == "__main__":
    radios = get_radios()
    make_m3u8(radios)
    make_html(radios)
