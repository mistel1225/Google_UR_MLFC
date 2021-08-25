from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import logging
#for community
'''
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get('https://us.community.samsung.com/t5/Samsung-Community/ct-p/us')
date_filter = driver.find_element_by_class_name('button__datefilter')
date_filter.click()
time.sleep(3)
from_filter = driver.find_element_by_class_name('date-filter-from')
from_filter.send_keys('12/01/2020')
from_filter.send_keys(Keys.ENTER)
to_filter = driver.find_element_by_class_name('date-filter-to')
to_filter.send_keys('08/01/2021')
to_filter.send_keys(Keys.ENTER)
date_button = driver.find_element_by_id('button__update')
date_button.click()
for i in range(10):
    load_button = driver.find_element_by_class_name('samsung-community-activity-load-more')
    load_button.click()
    time.sleep(1)
'''

def get_all_link(driver):
    thread_list = driver.find_element_by_id('grid')
    threads = thread_list.find_element_by_tag_name('tbody')
    thread_body = threads.find_elements_by_class_name('samsung-message-tile')
    links = []
    for t in thread_body:
        h3 = t.find_element_by_tag_name('a')
        links.append(h3.get_attribute('href'))
    return links
def get_content(driver, link):
    _ = driver.find_element_by_class_name('PageTitle')
    title = _.find_element_by_tag_name('span').text
    context = ""
    try:
        context = driver.find_element_by_id('bodyDisplay').text
    except:
        print("error: no content was found.")
        print("link = {0}".format(link))
    # for us
    '''
    flag = 0
    try:
        tag_list = driver.find_element_by_id('taglist')
        _ = tag_list.find_elements_by_tag_name('li')
        flag = 1
    except:
        pass
    tags=[]
    if flag == 1:
        for li in _:
            try:
                tags.append(li.find_element_by_tag_name('a').text)
            except:
                continue
    '''
    #for uk
    tags = []
    try:
        tag_list = driver.find_elements_by_class_name('label')
        for tag in tag_list:
            tags.append(tag.find_element_by_tag_name('a').text)
    except:
        logging.error(msg="",exc_info=True)
    print(title)
    print(context)
    print(tags)
    print('================================================================')
    return {'title':title, 'content':context, 'tag_list':tags, 'url': link}
if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)
    data_num = 0
    samsung_data = {}
    #for US
    '''
    link_list = [
    'https://us.community.samsung.com/t5/Galaxy-S21/bd-p/GalaxyS21',
    'https://us.community.samsung.com/t5/Note20/bd-p/get-help-galaxy-note20',
    'https://us.community.samsung.com/t5/Galaxy-S20/bd-p/get-help-galaxy-s20',
    'https://us.community.samsung.com/t5/Galaxy-Z-Flip/bd-p/get-help-galaxy-ZFlip',
    'https://us.community.samsung.com/t5/Galaxy-Fold/bd-p/Gethelp-galaxy-fold',
    'https://us.community.samsung.com/t5/Other-Mobile-Devices/bd-p/get-help-phones-other-mobile-devices',
    'https://us.community.samsung.com/t5/Galaxy-Note-Phones/bd-p/get-help-phones-galaxy-note-phones',
    'https://us.community.samsung.com/t5/Galaxy-S-Phones/bd-p/get-help-phones-galaxy-s-phones']
    for page in range(1, 65):
        driver.get(link_list[0]+'/page/{0}'.format(str(page)))
        links = get_all_link(driver)
        for link in links:
            driver.get(link)
            data = get_content(driver, link)
            samsung_data[data_num] = data
            data_num+=1
            print('{0}...'.format(data_num))
            time.sleep(0.25)
        with open('samsungdata.json', 'w') as f:
            json.dump(samsung_data, f, indent=2)
        time.sleep(5)
    for page in range(1, 33):
        driver.get(link_list[1]+'/page/{0}'.format(str(page)))
        links = get_all_link(driver)
        for link in links:
            driver.get(link)
            data = get_content(driver, link)
            samsung_data[data_num] = data
            data_num+=1
            print('{0}...'.format(data_num))
            time.sleep(0.1)
        with open('samsungdata.json', 'w') as f:
            json.dump(samsung_data, f, indent=2)
        time.sleep(5)

    for page in range(1, 45):
        driver.get(link_list[2]+'/page/{0}'.format(str(page)))
        links = get_all_link(driver)
        for link in links:
            driver.get(link)
            data = get_content(driver, link)
            samsung_data[data_num] = data
            data_num+=1
            print('{0}...'.format(data_num))
            time.sleep(0.25)
        with open('samsungdata.json', 'w') as f:
            json.dump(samsung_data, f, indent=2)
        time.sleep(5)
    for page in range(1, 4):
        driver.get(link_list[3]+'/page/{0}'.format(str(page)))
        links = get_all_link(driver)
        for link in links:
            driver.get(link)
            data = get_content(driver, link)
            samsung_data[data_num] = data
            data_num+=1
            print('{0}...'.format(data_num))
            time.sleep(0.1)
        with open('samsungdata.json', 'w') as f:
            json.dump(samsung_data, f, indent=2)
        time.sleep(5)
    for page in range(1, 7):
        driver.get(link_list[4]+'/page/{0}'.format(str(page)))
        links = get_all_link(driver)
        for link in links:
            driver.get(link)
            data = get_content(driver, link)
            samsung_data[data_num] = data
            data_num+=1
            print('{0}...'.format(data_num))
            time.sleep(0.25)
        with open('samsungdata.json', 'w') as f:
            json.dump(samsung_data, f, indent=2)
        time.sleep(5)
    for page in range(1, 64):
        driver.get(link_list[5]+'/page/{0}'.format(str(page)))
        links = get_all_link(driver)
        for link in links:
            driver.get(link)
            data = get_content(driver, link)
            samsung_data[data_num] = data
            data_num+=1
            print('{0}...'.format(data_num))
            time.sleep(0.1)
        with open('samsungdata.json', 'w') as f:
            json.dump(samsung_data, f, indent=2)
        time.sleep(5)
    for page in range(1, 59):
        driver.get(link_list[6]+'/page/{0}'.format(str(page)))
        links = get_all_link(driver)
        for link in links:
            driver.get(link)
            data = get_content(driver, link)
            samsung_data[data_num] = data
            data_num+=1
            print('{0}...'.format(data_num))
            time.sleep(0.25)
        with open('samsungdata.json', 'w') as f:
            json.dump(samsung_data, f, indent=2)
        time.sleep(5)
    for page in range(1, 92):
        driver.get(link_list[7]+'/page/{0}'.format(str(page)))
        links = get_all_link(driver)
        for link in links:
            driver.get(link)
            data = get_content(driver, link)
            samsung_data[data_num] = data
            data_num+=1
            print('{0}...'.format(data_num))
            time.sleep(0.1)
        with open('samsungdata.json', 'w') as f:
            json.dump(samsung_data, f, indent=2)
        time.sleep(5)
    '''
    #for uk
    driver.get('https://eu.community.samsung.com/t5/smartphones/ct-p/smartphones-uk?fbclid=IwAR2qmQmH8dTSISWXPOq3ufA0YfW8YxWIGLp-uXRkfPK3sDj-I6MaLqbQ2FA')
    category = driver.find_element_by_class_name('category-wayfinding')
    _ = category.find_elements_by_tag_name('figure')
    #_ = _.find_elements_by_tag_name('a')
    category_links = []
    for i in _ :
        a = i.find_element_by_tag_name('a')
        link = a.get_attribute('href')
        category_links.append(link)
    for series in category_links:
        driver.get(series)
        _ = driver.find_element_by_class_name('lia-paging-full')
        _ = _.find_element_by_class_name('lia-paging-page-last')
        num_pages = _.find_element_by_tag_name('a').text
        for page in range(1, int(num_pages)):
            driver.get(series+'/page/{0}'.format(str(page)))
            links = get_all_link(driver)
            for link in links:
                driver.get(link)
                data = get_content(driver, link)
                samsung_data[data_num] = data
                data_num+=1
                print('{0}...'.format(data_num))
                time.sleep(0.001)
            with open('samsungdatauk.json', 'w') as f:
                json.dump(samsung_data, f, indent=2)
            time.sleep(5)







