import requests

headers = {
            "authority": "dl.opensubtitles.org",
            "Connection": "keep-alive",
            "path": "/en/download/sub/7164785",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "referer": "https://www.opensubtitles.org/en/subtitles/7164785/pardes-en/short-on"
           }

session = requests.Session()

url1 = 'https://dl.opensubtitles.org/en/download/sub/7164785'
url2 = 'https://dl.opensubtitles.org/en/download/sub/7164785'

#the website sets the cookies first
req1 = session.get(url1, headers = headers)

req1

#Request again to download
req2 = session.get(url2, headers = headers)

req2

print(len(req1.content))     # This is the size of the mdi file
print(len(req2.content))     # This is the size of the mdi file

with open("testFile.zip", "wb") as saveMidi:
    saveMidi.write(req2.content)

u = 'https://yts-subtitles.com'
a = requests.get(u)
