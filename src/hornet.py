"""Hornet.py: Webservice for subdomain enumeration and screenshoting."""

__author__ = "Jannis Kirschner"
__version__ = "1.0.0"
__license__ = "GPL"
__credits__ = ["aboul3la","TheRook","Bitquark"] #Creators of Sublist3r which I included to enumerate subdomains

from flask import Flask
from flask_cors import CORS, cross_origin
from selenium import webdriver
import libs.sublist3r.sublist3r as sublist3r
from selenium.webdriver.chrome.options import Options
from flask import Response
from flask import request
import os
import shutil
import html
import requests
import datetime
import platform

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



class screenshots():
    def __init__(self):
        if(platform.system()=="Linux"):
            self.BASE_PATH = os.path.dirname(os.path.realpath(__file__))
            self.CHROMEDRIVER_PATH = r"%s/libs/selenium_drivers/chromedriver" % (self.BASE_PATH)
            self.WINDOW_SIZE = "1920,1080"

            self.chrome_options = Options()  
            self.chrome_options.add_argument("--headless") 
            self.chrome_options.add_argument("--no-sandbox")
            self.chrome_options.add_argument("--disable-dev-shm-usage") 
            self.chrome_options.add_argument("--window-size=%s" % self.WINDOW_SIZE)

        elif(platform.system()=="Windows"):
            self.BASE_PATH = os.path.dirname(os.path.realpath(__file__))
            self.CHROMEDRIVER_PATH = r"%s/libs/selenium_drivers/chromedriver.exe" % (self.BASE_PATH)
            self.WINDOW_SIZE = "1920,1080"

            self.chrome_options = Options()
            self.chrome_options.add_argument("--headless")
            self.chrome_options.add_argument("--window-size=%s" % self.WINDOW_SIZE)

        self.driver = webdriver.Chrome(
            executable_path=self.CHROMEDRIVER_PATH,
            chrome_options=self.chrome_options
        )

        
    def make_screenshot(self, url, baseoutput):
        """Takes screenshot of given url."""
        print("[*] Shooting: %s" % (url))
        if not url.startswith('http'):
            raise Exception('URLs need to start with "http"')
        try:
            self.driver.get(url)

            try:
                r = requests.get(url)
                status = r.status_code
            except requests.exceptions.SSLError as e:
                status = 403
            except requests.exceptions.ConnectionError as e:
                status = 503

            output = "%s_%s.png" % (baseoutput,status)
            os.makedirs(os.path.dirname(output), exist_ok=True)
            self.driver.save_screenshot(output)
            print("[+] Saved: %s" % (output))
        except Exception as e:
            print("[!] Shooting %s failed!" % (url))
            print(e)
            with open("error.log", "a") as log:
                log.write(str(datetime.datetime.utcnow()))
                log.write("[!] Shooting %s failed!" % (url))
                log.write(e)
                log.write("-----------")


    def screenshot_subdomains(self, subdomains, domain, ssl):
        """Takes screenshots given a list of subdomains."""
        i = 1
        for subdomain in subdomains:
            print("%d/%d" % (i,len(subdomains)))
            print(subdomain)
            if(ssl):
                self.make_screenshot("http://%s" % (subdomain), r"%s/shots/%s/%s" % (self.BASE_PATH, domain,subdomain))
            else:
                self.make_screenshot("https://%s" % (subdomain), r"%s/shots/%s/%s" % (self.BASE_PATH, domain,subdomain))
            i+= 1
            
    def clear(self, BASE_PATH):
        """Deletes every file in a directory."""
        directory = r"%s/shots" % (self.BASE_PATH)
        for the_file in os.listdir(directory):
            file_path = os.path.join(directory, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print("[!] Clearing failed!")
                print(e)
                with open("error.log", "a") as log:
                    log.write(str(datetime.datetime.utcnow()))
                    log.write("[!] Clearing failed!")
                    log.write(e)
                    log.write("-----------")


@app.route("/")
@cross_origin()
def run():
    site = request.args.get("site")
    ssl = request.args.get("ssl")
    if(ssl == "false"):
        usessl = False
    elif(ssl == "true"):
        usessl = True
    if(site != None):
        site = html.escape(site)
        s = screenshots()
        BASE_PATH = os.path.dirname(os.path.realpath(__file__))
        subdomains = sublist3r.main(site, 40, BASE_PATH + r'\cache.txt', ports= None, silent=False, verbose= False, enable_bruteforce= False, engines=None)
        print(subdomains)
        s.screenshot_subdomains(subdomains, site, usessl) 
        print("[*] Done")
        return "OK"
    else:
        return "Bad Input"

@app.route("/include")
@cross_origin()
def add():
    site = request.args.get("site")
    ssl = request.args.get("ssl")
    if(ssl == "false"):
        usessl = False
    elif(ssl == "true"):
        usessl = True
    if(site != None):
        site = html.escape(site)
        s = screenshots()
        domain = "%s.%s" % (site.split(".")[-2], site.split(".")[-1])
        s.screenshot_subdomains([site], domain, usessl) 
        print("[*] Done")
        return "OK"
    else:
        return "Bad Input"

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080, threaded=True)
