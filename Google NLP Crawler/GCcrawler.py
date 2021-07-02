from selenium import webdriver
import time
import pickle
import json

def scrollbottom(driver):
    js="var q=document.documentElement.scrollTop=10000000"
    driver.execute_script(js)

def waitloading_google_com(driver):
    loading=None
    loading_xpath = '/html/body/div[2]/div/section/div/div[1]/article/div[7]/div[2]/div[11]'
    while (loading==None):
        try:
            driver.find_element_by_xpath(loading_xpath)
            loading=1
        except:
            time.sleep(3)
    print('waiting over')

def get_all_link(driver,num):
    links = []
    links_obj=driver.find_element_by_class_name('thread-list__threads')
    all_links_obj = links_obj.find_elements_by_class_name('thread-list-thread')
    for idx,link_obj in enumerate(all_links_obj):
        if idx%100==0:
            print(idx+1,'/',len(all_links_obj))
        links.append(link_obj.get_attribute('href'))
    print('Total page # : ',len(links))
    return links

def browse_all_link(driver,links):
    all_data=[]
    for idx,link in enumerate(links):
        print(idx+1,'/',len(links),' ',link)
        driver.get(link)
        ready=None
        while (ready==None):
            try:
                driver.find_element_by_class_name('thread-question__disclaimer').text
                ready=1
            except:
                time.sleep(1)
        current_link=driver.current_url
        title = driver.find_element_by_class_name('thread-question__title').text
        content_ele = driver.find_element_by_class_name('thread-question__payload')
        content = content_ele.text
        try:
            content_ele.find_element_by_tag_name('img')
            is_img=1
        except:
            is_img=0
        cate = driver.find_element_by_class_name('thread-question__details-list').text
        post_time = driver.find_element_by_tag_name('time').get_attribute('datetime')
        try:
            reply = driver.find_element_by_class_name('thread-counts.thread-counts--show-replies').text
        except:
            reply=''
        if reply=='':
            reply = driver.find_element_by_class_name('thread-counts__count.thread-counts__count--recommended').text
        data = {'url':current_link,
                'title':title,
                'content':content,
                'is_img':is_img,
                'category':cate,
                'post_time':post_time,
                'reply':reply}
        all_data.append(data)
        time.sleep(1)
    return all_data

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
#driver = webdriver.Chrome('./chromedriver')
result_num=50000
google_community_url = 'https://support.google.com/pixelphone/threads?hl=en&max_results='+str(result_num)
driver.get(google_community_url)
waitloading_google_com(driver)
links = get_all_link(driver,result_num)
all_data = browse_all_link(driver,links)
print('browse over')
all_data = {'data':all_data}
print('starting save data...')
with open('data{}.json'.format(result_num), 'w') as fp:
    json.dump(all_data, fp)

time.sleep(1)
driver.quit()
