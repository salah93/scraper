"""
Check the status of each URL in a CSV file.
"""
import csv
import json
import os
import requests


JSON_FOLDER = "../../pyvideo-data/data"


def check_links(videos):
    status_codes = []
    # Check each url's validity
    for title, urls in videos:
        for url in urls:
            try:
                print(url)
                req = requests.head(url)
                status_codes.append((title, url, req.status_code))
            except requests.HTTPError as e:
                status_codes.append((title, url, e.status_code))
            except requests.ConnectionError as e:
                status_codes.append((title, url, "ConnectionError"))
    return status_codes


def get_urls():
    urls = {}
    for folder, dirs, files in os.walk(JSON_FOLDER):
        if os.path.basename(folder) == "videos":
            for jf in files:
                if jf[-5:] == ".json":
                    jsonfile = os.path.join(folder, jf)
                    with open(jsonfile, 'r') as f:
                        vid = json.load(f)
                        urls[vid["title"]] = [v["url"] for v in vid["videos"]]
    return urls


if __name__ == "__main__":
    urls = get_urls()
    status_codes = check_links(urls.items())
    with open("report-{0}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "url", "status code"])
        writer.writerows(status_codes)