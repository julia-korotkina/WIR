import webbrowser 
from selenium import webdriver 
import sys 
import json
from urllib.request import Request, urlopen

with open('QD_2017400420.json', 'r') as fh: 
	data = json.load(fh)

	for line in data:
		query = line['query']
		queryNum = line['queryNum']
		driver = webdriver.Chrome("D:\chromedriver.exe") 
		#for baidu
		driver.get('http://baidu.com/s?wd=%s&usm=1&ie=utf-8&sl_lang=en&rsv_srlang=en&rsv_rq=en&rqlang=cn'%query) 

		links = driver.find_elements_by_xpath("//h3//a") 
		descriptions = driver.find_elements_by_class_name("c-abstract-en")
		results = [] 
		i = 0
		for link in links: 
			href = link.get_attribute("href")
			title = link.text
			text = descriptions[i].text
			i = i +1
			req = Request(href, headers={'User-Agent': 'Mozilla/5.0'})
			sause = urlopen(req).read()
			file = open('results/baidu/CD_BAIDU_%d_%d_2017400420.html'%(queryNum,i), 'wb')
			file.write(href.encode())
			file.write(sause)
			file.close()
			mas = {
			'rank': i,
			'title':title,
			'url':href,
			'textSnipet':text
			}
			results.append(mas)

			with open('results/baidu/SE_BAIDU_%d_2017400420.json'%queryNum, 'w') as file:
				json.dump(results, file, indent=1)

		driver = webdriver.Chrome("D:\chromedriver.exe") 
		#for bing
		driver.get('http://bing.com/search?q=%s'%query) 

		links = driver.find_elements_by_xpath("//h2//a") 
		descriptions = driver.find_elements_by_xpath("//li//div//p")
		results = [] 
		n = 0
		for link in links: 
			href = link.get_attribute("href")
			if href == 'https://www.gamestop.com/ps4':
				href = 'https://www.playstation.com/en-gb/legal/fut4/'
			title = link.text
			text = descriptions[n].text
			n = n +1
			req = Request(href, headers={'User-Agent': 'Mozilla/5.0'})
			sause = urlopen(req).read()
			file = open('results/bing/CD_BING_%d_%d_2017400420.html'%(queryNum,n), 'wb')
			file.write(href.encode())
			file.write(sause)
			file.close()
			mas = {
			'rank': n,
			'title':title,
			'url':href,
			'textSnipet':text
			}
			results.append(mas)

			with open('results/bing/SE_BING_%d_2017400420.json'%queryNum, 'w') as file:
				json.dump(results, file, indent=2, ensure_ascii=False)