import requests
from bs4 import BeautifulSoup
import json
import re
import sys
import getopt
from packaging.version import Version

def get_releases(url):
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5'})
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.findAll("a", href=re.compile('^([.0-9]*)\/$'))
    releases = []

    for result in results:
        releases.append(result['href'].replace('/', ''))
    return releases

def get_pushed_tags(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5'})

    tags = []
    if (response.status_code != 404):
        tags = []
        json = response.json()
        tags = [container['name'] for container in json['results']]

    return tags

def main(argv):
    latestOnly = False
    force = False

    try:
        opts, args = getopt.getopt(argv, "hlft:r:", ["tags-url=", "releases-url=", "latest-only", "force"])
    except getopt.GetoptError:
        print
        'print_versions.py -t <dockerhub tags url> -r <releases url> [--latest-only] [--force]'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print
            'print_versions.py -t <dockerhub tags url> -r <release url> [--latest-only] [--force]'
            sys.exit()
        elif opt in ("-t", "--tags-url"):
            urlTags = arg
        elif opt in ("-f", "--force"):
            force = True
        elif opt in ("-r", "--releases-url"):
            urlReleases = arg
        elif opt in ("-l", "--latest-only"):
            latestOnly = True

    if force:
        # ignore pushed tags
        tags = []
    else:
        tags = get_pushed_tags(urlTags)

    releases = get_releases(urlReleases)
    result = [x for x in releases if x not in tags]
    result.sort(key=Version)

    if not result:
        print(json.dumps(""))
    else:
        if latestOnly:
            print(json.dumps(result[-1]))
        else:
            print(json.dumps(result))
    sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])