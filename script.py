import random
import concurrent.futures
import requests
import sys
from bs4 import BeautifulSoup

class WebpageTitleExtractor:
    def __init__(self, url):
        self.url = url

    def get_title(self):
        try:
            response = requests.get(self.url, timeout=3)
            soup = BeautifulSoup(response.text, "html.parser")
            title_element = soup.title
            if title_element is not None:
                title = title_element.text
            else:
                h1_tag = soup.find("h1")
                if h1_tag is not None:
                    title = h1_tag.text
                else:
                    title = ""
            return title
        except:
            return ""

def generate_random_ips(number):
    ips = []
    while len(ips) < number:
        ip = ".".join([str(random.randint(0, 255)) for x in range(4)])
        if ip not in ips:
            ips.append(ip)
    return ips

if len(sys.argv) == 3:
    option = sys.argv[1]
    if option == "-L":
        ips = []
        file = sys.argv[2]
        with open(file, "r") as f:
            for line in f:
                ip = line.strip()
                ips.append(ip)
    elif option == "-R":
        number = int(sys.argv[2])
        ips = generate_random_ips(number)
    else:
        ips = []
else:
    ips = []

def get_title(ip):
    url = f"http://{ip}:80"
    extractor = WebpageTitleExtractor(url)
    title = extractor.get_title()
    print(f"Title for IP {ip}: {title}")

with concurrent.futures.ThreadPoolExecutor() as executor:
    try:
        executor.map(get_title, ips)
    except Exception as e:
        print(f"Error: {e}")
        pass
