from pymongo import MongoClient
import json
from pprint import pprint
from bson.objectid import ObjectId



db = MongoClient(host='140.143.225.98',port=27017).students
# db = MongoClient(host='111.193.230.146',port=27017).shangjiaosuo
# coll = db.sse_page
# coll = db.named
# data_list = coll.find()
# for i in data_list:
#     data = json.loads(i['page'])
#     pprint(data)
# print(coll)
# ret = coll.insert({'name':'laowang'})
# print(ret)
# coll.close()
# db.close()

def get_page():
    with open('hello.txt', 'r') as f:
        while True:
            data = f.readline()
            if not data:
                break
            data = json.loads(data)
            code = data['code']
            _id = data['_id']
            print(_id)
            page = list(db.test.find({'_id':ObjectId(_id)}))
            print(page)
            page = page[0]['page']
            yield int(page)**2


def save_page(code, page):
    _id = db.test.insert({'code': code, 'page': page})
    print(_id)
    with open('hello.txt', 'a+') as f:
        f.write(json.dumps({'_id': str(_id), 'code': code}))
        f.write('\r\n')


# for i in range(5):
#     save_page('a', str(i))
#
# for page in get_page():
#     print(page)
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


basic_url = 'https://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w={}'

# dcap = dict(DesiredCapabilities.PHANTOMJS)
# dcap["phantomjs.page.settings.userAgent"] = (
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
# )

# browser = webdriver.PhantomJS(desired_capabilities=dcap)
option = webdriver.FirefoxOptions()
option.headless = True
browser = webdriver.Firefox(firefox_options=option)
# browser = webdriver.PhantomJS()
browser.get(basic_url.format('000001'))
# # time.sleep(7)
page_source = browser.page_source
browser.close()
browser.quit()
print(page_source)


from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def editUserAgent():
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap['phantomjs.page.settings.userAgent'] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36")
    driver = webdriver.PhantomJS(desired_capabilities=dcap,
                                 service_args=['--ignore-ssl-errors=true'])
    driver.get('https://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w=000001')
    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')
    user_agent = soup.find_all('td', attrs={
        'style': 'height:40px;text-align:center;font-size:16px;font-weight:bolder;color:red;'})
    for u in user_agent:
        print(u.get_text().replace('\n', '').replace(' ', ''))
    driver.close()
    print(source)


# editUserAgent()
