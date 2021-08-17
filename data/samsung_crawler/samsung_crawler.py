from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
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
    print(title)
    '''
    _ = driver.find_element_by_id('bodyDisplay')
    context = _.find_element_by_tag_name('p').text
    '''
    context = driver.find_element_by_id('bodyDisplay').text
    print(context)
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
    print(tags)
    print('================================================================')
    return {'title':title, 'context':context, 'tag_list':tags, 'url': link}
if __name__ == '__main__':
    #for s21 forum
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)
    data_num = 0
    samsung_data = {}
    for page in range(1, 65):
        driver.get('https://us.community.samsung.com/t5/Galaxy-S21/bd-p/GalaxyS21'+'/page/{0}'.format(str(page)))
        links = get_all_link(driver)
        for link in links:
            driver.get(link)
            data = get_content(driver, link)
            samsung_data[data_num] = data
            data_num+=1
            print('{0}...'.format(data_num))
            time.sleep(1.5)
        with open('samsungdata.json', 'w') as f:
            json.dump(samsung_data, f, indent=2)
        time.sleep(5)
