import requests
# import lxml
from bs4 import BeautifulSoup
from urllib.parse import unquote

#Here is >> URL (DON'T FORGET "/" IN THE END)
URL = 'http://reactor.cc/tag/%D0%BA%D0%BE%D1%82%D1%8D/'

#U must change it on user-agent and accept from ur browser
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
    'accept': 'image/avif,image/webp,*/*'
}


def main(src_, i):

    #saving html to save data, if server try to stop scrapping

    with open('index' + str(i) + '.html', 'w', encoding='utf-8') as file:
        file.write(src_)
    soup = BeautifulSoup(src_, 'lxml')

    items = soup.find_all('div', class_='image')

    images = []
    for item in items:
        if item.find('img') is None:
            continue
        elif item.find('a', class_='prettyPhotoLink'):
            images.append(
                item.find('img').get('src').replace("/post/", "/post/full/")
            )
        else:
            images.append(
                item.find('img').get('src')
            )
    print(images)

    for item in images:
        p = requests.get(str(item))
        item = unquote(str(item))
        print(item)
        filename = item.split("/")[-1]
        filename = filename.replace('"', "")
        # here is name of folder where we'll save our images (parsed_cats/)
        # i didn't use os module so if this folder doesn't exists program will break
        # that's fast-made parser so i don't think what i must thinking about users who can get scared by this exception so...
        # and customer will just get what he want as archive with images so this program may be used only by me, and idk how u can read it///
        out = open('parsed_cats/' + filename, "wb")
        out.write(p.content)
        out.close()
    print("Images scraped")


req = URL

# selector - that's is starting page
page_selector = 1
# all pages:
page_all = 5224
while True:
    try:
        req = requests.get(URL+str(page_selector), stream=True, headers=headers)
        src = req.text
        main(src, page_selector)
        if page_selector == page_all:
            break
        page_selector += 1
    except req.status_code == 403:
        print("something went wrong on page: " + URL + str(page_selector))




