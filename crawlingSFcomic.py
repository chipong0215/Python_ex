# coding=utf-8

import sys, os, requests, time
from selenium import webdriver
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')#, filename='crawlingLog.txt')

requests.adapters.DEFAULT_RETRIES = 5

def mkdir(path):
    
    ###   Opening a new document if there isn't one.

    if not os.path.exists(path):
        logging.info('Now is opening the new document.\n')
        os.makedirs(path)


def SavePic(filename, url):
    
    ###   Saving the pics by crawling them by the requests libraray.

    logging.info('Now is saving the content.\n')


    try:
        content = requests.get(url).content
    except:
        print("Connection refused by the server..")
        print("Let me sleep for 5 seconds")
        print("ZZzzzz...")
        time.sleep(5)
        print("Was a nice sleep, now let me continue...")
        content = requests.get(url).content
        # continue

    with open(filename, 'wb') as f:
        f.write(content)

def get_TOF(index_url):

    logging.info('Now is going to call the PhantomJS.\n')

    ###   Gaining the urls of each chapters and returns a dictionary -- k: comic name, v: chapter url

    url_list = []

    # Imitating the browser to open the website
    browser = webdriver.PhantomJS()
    browser.get(index_url)
    browser.implicitly_wait(3)

    logging.info('After implicitly_wait.\n')


    # Find the comic thread and create the directory
    title = browser.title.split(',')[0]
    print(title)
    mkdir(title)
    

    logging.info('Give me the title: ' + title + '\n')


    # Find the chapters. P.S. there may be many of them.
    # For instance the extra chapters
    comics_lists = browser.find_elements_by_class_name('serialise_list')

    logging.info('Printout the comics_lists: \n')
    print(comics_lists)

    # Find the standard contents
    for part in comics_lists:
        # Find the urls which are wrapped in the tabs
        links = part.find_elements_by_tag_name('a')
        # Find each independent urls
        for link in links:
            url_list.append(link.get_attribute('href'))

    browser.quit()

    logging.info('Browser quit.\n')
    logging.info('Printout the url_lists: \n')

    print(url_list)

    Comics = dict(name=title, urls=url_list)

    return Comics


def get_pic(Comics):
    
    ###   Open every url and crawling them

    comic_list = Comics['urls']
    basedir = Comics['name']

    browser = webdriver.PhantomJS()
    # self.driver = webdriver.PhantomJS('/Users/chancriss/Phantomjs/bin/phantomjs')
    # driver = webdriver.PhantomJS(executable_path=r"D:\phantomjs\bin\phantomjs.exe")
    for url in comic_list:
        browser.get(url)
        browser.implicitly_wait(3)

        # Create the chapter directory
        dirname = basedir + '/' + browser.title.split('-')[1]
        mkdir(dirname)

        # Figure out how many pages
        pageNum = len(browser.find_elements_by_tag_name('option'))

        # Find the url of "nextpage button"
        # nextpage = browser.find_element_by_xpath('//*[@id="AD_j1"]/div/a[4]')
        nextpage = browser.find_element_by_xpath('/html/body/div[3]/div[2]/a[4]')

        # Find the pics address and click on the "nextpage button"
        for i in range(pageNum):
            pic_url = browser.find_element_by_id('curPic').get_attribute('src')
            filename = dirname + '/' + str(i) + '.png'
            SavePic(filename, pic_url)

            # Click the "nextpage button"
            # print('A chapter is finished downloaded: ' + browser.title) 
            nextpage.click()

        print('debug: ' + browser.title)
        # print('A chapter {} is finished downloaded.'.format(browser.title))
        print('A chapter is finished downloaded.\n')


    browser.quit()
    print('All the chapters is finished.')

def main():
    url = str(input('Please input the comic url： \n'))
    Comics = get_TOF(url)
    get_pic(Comics)


if __name__ == '__main__':
    main()