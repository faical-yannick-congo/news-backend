import bs4
import requests

def fetchCNN_USA(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    interests = []
    for spt in soup.find_all('script'):
        if "\"headline\":" in spt.get_text():
            for sp1 in spt.get_text().split("\","):
                if "\"headline\":" in sp1:
                    news_1 = sp1.split("\"headline\":\"")[1]
                    if news_1 != "":
                        interests.append(news_1)
    return interests

def fetchCNNCSS_USA(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    interests = []
    for desc in soup.find_all('description'):
        desc_content = desc.string.split('&lt;div')[0].split('<div')[0]
        if desc_content != "":
            interests.append(desc_content)
    return interests

def fetchRTB_BFA(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    content = soup.find_all("a", rel="bookmark")
    interests = [n['title'] for n in content]
    return interests

def fetchOMEGA_BFA(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    uls = soup.find_all("ul")
    interests = []
    for ul in uls:
        for li in ul.find_all("li"):
            a_content = li.find("a")
            if a_content:
                if a_content.string != "" and a_content.string and ':' in a_content.string:
                    interests.append(a_content.string)
    return interests

def fetchRFI_FRANCE(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    content = soup.find_all("title")
    interests = []
    for n in content:
        if n != "None" and n != "" and n != "\n":
            interests.append(n.string)
    return interests[:-2]

def fetchF24_FRANCE(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    content = soup.find_all("title")
    interests = []
    for n in content:
        if n != "None" and n != "" and n != "\n":
            interests.append(n.string)
    return interests

def fetchAF24_AFRIQUE(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    interests = []
    uls = soup.find_all("ul")
    interests = []
    for ul in uls:
        try:
            ul['class']
            select = True
        except:
            select = False
        if select and "fil-info-list" in ul['class']:
            for li in ul.find_all("li"):
                a_content = li.string
                if a_content != "" and a_content and '-' in a_content:
                    interests.append(a_content)
    return interests

def fetch2MFr_MA(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    interests = []
    As = soup.find_all("a")
    interests = []
    for a in As:
        try:
            a['href']
            a['title']
            select = True
        except:
            select = False

        if select and "/fr/news" in a['href']:
            a_content = a['title']
            if a_content != "":
                interests.append(a_content)
    return interests

def fetch2MAr_MA(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    interests = []
    As = soup.find_all("a")
    interests = []
    for a in As:
        try:
            a['href']
            a['title']
            select = True
        except:
            select = False

        if select and "/ar/news" in a['href']:
            a_content = a['title']
            if a_content != "":
                interests.append(a_content)
    return interests[:-1]

def fetchBFM_FRANCE(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    content = soup.find_all("title")
    interests = []
    for n in content:
        if n != "None" and n != "" and n != "\n":
            interests.append(n.string)
    return interests

def fetchArte_FRANCE(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    interests = []
    H3s = soup.find_all("h3")
    interests = []
    for h3 in H3s:
        try:
            h3['class']
            select = True
        except:
            select = False

        if select and "node-title" in h3['class']:
            if h3.a.string != "":
                interests.append(h3.a.string)
    return interests[:-1]

def fetchNYCTimes_USA(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    interests = []
    for desc in soup.find_all('description'):
        desc_content = desc.string
        interests.append(desc_content)
    return interests

def fetchF24CSS_En(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    interests = []
    for desc in soup.find_all('description'):
        if desc.string != None:
            try:
                desc_content = desc.string.split("</p>")[0].split("<p>")[1]
                if desc_content != "":
                    interests.append(desc_content)
            except:
                pass

    return interests
