import requests
from bs4 import BeautifulSoup
import random
from base64 import b64decode, b64encode
import os, re

USER_AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0"}

proxyof = "https://proxyof2.com/kickasstorrents-proxy-unblock/"

try:
    response = requests.get(url=proxyof, headers=USER_AGENT).content
except requests.exceptions.ConnectionError:
    print("Check Your Internet...")
    exit()

soup = BeautifulSoup(response, "lxml")

proxy_url = [ a.get("href") for a in soup.find_all("a", {"class": "proxy url"}) ]
random_proxy = random.choice(proxy_url)
response_url = requests.get(url=random_proxy, headers=USER_AGENT).url

user = input("Search : ")
payload = {
    "convertGET": "1",
    "q": "{}".format(user)
}

response = requests.post(url=random_proxy, headers=USER_AGENT, data=payload).url
identify_b64 = re.findall("[a-zA-Z0-9]+", response)
identify_b64.sort(key=len, reverse=True)

decode_actual_url = b64decode(identify_b64[0].encode()).decode()
decode_actual_url = decode_actual_url.split("|")
decode_actual_url[1] = "://kat.how/search?q={}".format('+'.join(user.split()))
decode_actual_url = b64encode("|".join(decode_actual_url).encode()).decode().replace("=", "%3D")
search_url = response.replace(identify_b64[0], decode_actual_url)

response = requests.post(search_url, headers=USER_AGENT)
soup = BeautifulSoup(response.content, "lxml")

topic_name = soup.find_all("a", {"class": "cellMainLink"})
topic_name = [ a.text for a in topic_name ] if topic_name != [] else ""

torrent_file = soup.find_all("a", {"title": "Torrent magnet link"})
torrent_file = [ a.get("href") for a in torrent_file ] if torrent_file != [] else ""

seeding = soup.find_all("td", {"class": "green center"})
seeding = [ seed.text for seed in seeding ] if seeding != [] else ""

merge_name_torrent = zip(topic_name, torrent_file, seeding)
key_value = dict(zip(topic_name, torrent_file))

count = 1
if merge_name_torrent:
    for name in merge_name_torrent:
        print(f"{count} : {name[0]} --> seed - [{name[2]}]")
        count += 1
else:
    print("no result..")

if key_value:
    torrent_name = input("Enter Torrent Name : ")
    magnetic_link = key_value[torrent_name]
    with open("magnetic_link.txt", "w") as link:
        link.write(magnetic_link)
        print(f"Magnetic Link File => '{os.getcwd()}'")