import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import zipfile
from subprocess import call
import sys
import os
import configuration as c


# Credits to https://github.com/HamidrezaMoradi/APK-Downloader        
def downloader(download_url, path):
    try:
        r_download_url = requests.get(download_url, stream=True)
        with open(path, "wb") as handle:
            for data in tqdm(r_download_url.iter_content()):
                handle.write(data)
        return True
    except Exception:
        return False


# Credits to https://github.com/HamidrezaMoradi/APK-Downloader        
def apkdl_in(package_id):
    try:
        apkdl = 'https://apkdl.in/app/details?id=' + package_id
        r = requests.get(apkdl)
        app_page = BeautifulSoup(r.text, 'html.parser')
        download_url = app_page.find("a", itemprop='downloadUrl')

        download_url = 'https://apkdl.in'+download_url['href']
        r = requests.get(download_url)
        download_page = BeautifulSoup(r.text, 'html.parser')
        download_url = download_page.find("a", rel='nofollow')
        return download_url if download_url is not None else None
    except:
        return None


# Credits to https://github.com/HamidrezaMoradi/APK-Downloader        
def apkplz_net(package_id):
    try:
        url = 'https://apkplz.net/app/' + package_id
        r = requests.get(url)
        app_page = BeautifulSoup(r.text, 'html.parser')
        download_url = app_page.find("div", attrs={'class':'col-sm-12 col-md-12 text-center'})

        download_url = download_url.find("a", rel='nofollow')['href']
        r = requests.get(download_url)
        download_page = BeautifulSoup(r.text, 'html.parser')
        download_url = download_page.find("a", string='click here')
        return download_url['href'] if download_url is not None else None
    except:
        return None


# Credits to https://github.com/HamidrezaMoradi/APK-Downloader        
def apktada_com(package_id):
    try: 
        url = 'https://apktada.com/download-apk/' + package_id
        r = requests.get(url)
        app_page = BeautifulSoup(r.text, 'html.parser')
        download_url = app_page.find("a", string='click here')
        return download_url['href'] if download_url is not None else None
    except:
        return None


# Credits to https://github.com/HamidrezaMoradi/APK-Downloader        
def m_apkpure_com(package_id):
    try:
        url = 'https://m.apkpure.com/android/' + package_id + '/download?from=details' 
        r = requests.get(url)
        app_page = BeautifulSoup(r.text, 'html.parser')
        download_url = app_page.find("a", string='click here')
        return download_url['href'] if download_url is not None else None
    except:
        return None


# Credits to Gian Luca Scoccia - https://github.com/S2-group/apkDownloader/
def apk_is_valid(_apk_name):
    with open(os.devnull, "w") as null:
        error_state = 1
        try:
            error_state = call(["aapt", "dump", "permissions", _apk_name], stdout=null, stderr=null)
            if error_state != 0:
                print("It seems we downloaded an XAPK, we unpack it now...")
        except:
            pass
        return error_state == 0


# Credits to Gian Luca Scoccia - https://github.com/S2-group/apkDownloader/
def xapk_is_valid(_xapk_name, _package_name):
    with zipfile.ZipFile(_xapk_name) as zfile:
        if _package_name in zfile.namelist():
            return True
        else:
            return False


# Credits to Gian Luca Scoccia - https://github.com/S2-group/apkDownloader/
def unpack_xapk(_xapk_name: str, _package_name: str) -> None:
    with zipfile.ZipFile(os.path.join(c.APKS_PATH, _xapk_name)) as zfile:
        zfile.extract(_package_name, c.APKS_PATH)


# Credits to Gian Luca Scoccia - https://github.com/S2-group/apkDownloader/
def verify_apk(apk_name: str, apk_path: str, app_suffix_path: str) -> bool:
    if not apk_is_valid(apk_path):
        if xapk_is_valid(apk_path, apk_name + ".apk"):
            new_name = apk_path.split(".apk")[0] + ".xapk"
            os.rename(apk_path, new_name)
            unpack_xapk(app_suffix_path + ".xapk", apk_name + ".apk")
            os.rename(c.APKS_PATH + apk_name + ".apk", apk_path)
            os.remove(new_name)
            if not apk_is_valid(apk_path):
                os.remove(apk_path)
                print("Invalid file {}, removed".format(apk_path))
                return False
            else:
                print("Xapk unpacked successfully!")
                return True
        else:
            os.remove(apk_path)
            print("Invalid file {}, removed".format(apk_path))
            return False
    else:
        return True


def download_apk(app_id, path):
    download_url = m_apkpure_com(app_id)
    if downloader(download_url, path):
        return True
    download_url = apkplz_net(app_id)
    if downloader(download_url, path):
        return True
    download_url = apktada_com(app_id)
    if downloader(download_url, path):
        return True
    download_url = apkdl_in(app_id)
    if downloader(download_url, path):
        return True
    return False
