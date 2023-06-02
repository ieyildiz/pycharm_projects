import sys
from urllib import response
import requests

if len(sys.argv) != 2:
    sys.exit()

response = requests.get("https://itunes.apple.com/search?entity=song&limit=1&term=weezer" + sys.argv[1])
print(response.json())