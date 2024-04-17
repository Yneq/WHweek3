import urllib.request
import json
import re
import csv

def fetch_data(url):
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")
    return data

def tpe_district(address):
    match = re.search(r"\s(\w+區)", address) #正則表示法取地區名
    if match:
        return match.group(1)
    return None

def spider(data1, data2, spot_csv, mrt_csv):
    spots1 = json.loads(data1)
    spots2 = json.loads(data2)
    spots_list1 = spots1["data"]["results"]
    spots_list2 = spots2["data"]

    address_dict = {spot["SERIAL_NO"] : spot["address"] for spot in spots_list2}

    spot_data = []

    for spot1 in spots_list1:
        serial_no = spot1["SERIAL_NO"]
        address = address_dict.get(serial_no, "")
        district = tpe_district(address) #正則表示法

        title = spot1["stitle"]
        longitude = spot1["longitude"]
        latitude = spot1["latitude"]
        img_urls = spot1["filelist"].split("http")
        first_img = "http" + img_urls[1] if len(img_urls) > 1 else ""
        
        spot_data.append([title, district, longitude, latitude, first_img])

    #build two dicts to 映射, SERIAL_NO 為媒介
    mrt_dict = {spot["SERIAL_NO"] : spot["MRT"] for spot in spots_list2}
    title_dict = {spot["SERIAL_NO"] : spot["stitle"] for spot in spots_list1}
    mrt_to_attractions = {}
    for serial_no, mrt in mrt_dict.items():
        title = title_dict.get(serial_no)
        if title:
            if mrt in mrt_to_attractions:
                mrt_to_attractions[mrt].append(title)
            else:
                mrt_to_attractions[mrt] = [title]

    with open("spot.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        for title, district, longitude, latitude, first_img in spot_data:
            writer.writerow([title, district, longitude, latitude, first_img])


    with open("mrt.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        for mrt, attracitons in mrt_to_attractions.items():
            writer.writerow([mrt] + attracitons)
    

data1 = fetch_data("https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1")
data2 = fetch_data("https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2")
spider(data1, data2, 'spot.csv', 'mrt.csv')