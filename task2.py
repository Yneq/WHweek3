import urllib.request as req

def fetch_data(url):
    request = req.Request(url, headers = {
    "cookie":"over18=1",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    return data

import bs4

    
def getData(pageurl):
    data = fetch_data(pageurl)
    root = bs4.BeautifulSoup(data, "html.parser")
    titles = root.find_all("div", class_="title")
    results = []
    for title_div in titles:
        if title_div.find("a") != None:
            likecount_span = title_div.find("span", class_="hl f2")
            likecount_text = likecount_span.text if likecount_span else 0
            link = "https://www.ptt.cc"+title_div.find("a")["href"]
            results.append((title_div.find("a").string, likecount_text, fetch_publish_time(link)))
            print(title_div.find("a").string, likecount_text, fetch_publish_time(link))
                #比較好的寫法是設變數publish_time=fetch_pubhlish_time(link)
                #因為不用每印一次就要跑一次fetch_publish_time()

            
    pre_page = root.find("a", string="‹ 上頁")
    return results, ("https://www.ptt.cc"+pre_page["href"])

def fetch_publish_time(link):       #結果這個找時間弄最久
    article_data = fetch_data(link)
    article_soup = bs4.BeautifulSoup(article_data, "html.parser")
    meta_value = article_soup.find_all("span", class_="article-meta-value") #這裡程式一直崩，找不到資料，返回none
    if meta_value:  # 確認找到元素後再訪問 `.text`
        publish_time = meta_value[-1].text
    else:
        publish_time = "No Time" 
    return publish_time


pageurl="https://www.ptt.cc/bbs/Lottery/index.html"
all_titles = []
count=0
while count<3:
    new_titles, pageurl = getData(pageurl)
    all_titles.extend(new_titles)
    count+=1

with open ("article.csv", "w", encoding="utf-8") as file:
    for title, likecount, publishtime in all_titles:
        file.write(f"{title}, {likecount}, {publishtime} \n")