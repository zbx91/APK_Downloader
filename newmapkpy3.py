import re
import progressbar
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error

download_apk_from_url = "http://m.apk.tw/top"
progress_bar = None


def getInformationFromAPk(url):

    content = urllib.request.urlopen(url)
    html_code = content.read().decode("utf-8")

    soup = BeautifulSoup(html_code, "html.parser")

    apk_url = soup.find(
        "div", attrs={
            'class': 'download'
        }).find(
            "a", href=True)['href']

    apk_name = soup.find("h3", attrs={'class': 'mt-10'}).string

    #get property from web
    apk_property = soup.find("div", attrs={'class': 'property'}).find_all('li')
    prolist = []

    for li in apk_property:
        prolist.append(str(li))

    #slice string from ':' and end with '</'

    version = prolist[0][prolist[0].index("：") + 1:prolist[0].index("</")]
    filesize = prolist[1][prolist[1].index("：") + 1:prolist[1].index("</")]
    download_times = prolist[2][prolist[2].index("：") +
                                1:prolist[2].index("</")]
    classification = prolist[3][prolist[3].index("\">") +
                                2:prolist[3].index("</")]
    system = prolist[4][prolist[4].index("：") + 1:prolist[4].index("</")]
    package_name = prolist[5][prolist[5].index("：") + 1:prolist[5].index("</")]
    date = prolist[6][prolist[6].index("：") + 1:prolist[6].index("</")]

    return {
        'apk_url': apk_url,
        'apk_name': apk_name,
        'version': version,
        'filesize': filesize,
        'download_times': download_times,
        'classification': classification,
        'system': system,
        'package_name': package_name,
        'date': date
    }


# download apk file from m.apk.tw/top


def downloadApkFromUrl(url_to_download, filename, total_size):
    print("Downloading  %s  file , size is %s" % (filename, total_size))
    urllib.request.urlretrieve(url_to_download, filename,
                               callback_download_complete)
    print("Finish donloading")


def callback_download_complete(block_num, block_size, total_size):
    global progress_bar
    if progress_bar is None:
        progress_bar = progressbar.ProgressBar(maxval=total_size).start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        progress_bar.update(downloaded)
    else:
        progress_bar.finish()
        progress_bar = None


def Main():
    # 取得全部要下載的APP url


    # 取得單一APP資訊
    result_information = getInformationFromAPk(
        "https://m.apk.tw/app/com.madhead.tos.zh/")
    # 開始下載
    downloadApkFromUrl(result_information['apk_url'],
                       result_information['apk_name'] + '.apk',
                       result_information['filesize'])


if __name__ == '__main__':
    Main()