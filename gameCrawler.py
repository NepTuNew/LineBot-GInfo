import requests
from bs4 import BeautifulSoup
from imgurpython import ImgurClient
import json
import time

from linebot.models import (
	CarouselTemplate, TemplateSendMessage, CarouselColumn, URITemplateAction
)
import helper

no_image = 'https://i.imgur.com/j0tfIPQ.jpg'

def test():
	print('GameCrawler Model Loader!')
def upload_photo(image_url, image_name):
	client_id = 'YOUR_CLIENT_ID'
	client_secret = 'YOUR_CLIENT_SECRET'
	access_token = 'YOUR_ACCESS_TOKEN'
	refresh_token = 'YOUR_REFRESH_TOKEN'
	client = ImgurClient(client_id, client_secret, access_token, refresh_token)
	album_id = 'YOUR_ALBUM_ID'
	album = client.get_album(album_id)
	# check whether image have been upload ever 
	for image in album.images:
		if image['name'] == image_name:
			print('Find image in Album {}!'.format(album_id))
			return image['link']

	# set configuration
	config = {
		'album': album_id,
		'name': image_name
	}
	print('Uploading image to imgur.com ... ...')
	image = client.upload_from_url(image_url, config=config, anon=False)
	print('Upload Done~')
	return image['link']

def getTowerSavior(push_num):
	ts_url = 'http://www.towerofsaviors.com/zh/event'
	ts_prefix = 'http://www.towerofsaviors.com'
	res = requests.get(ts_url)
	soup = BeautifulSoup(res.text, 'lxml')

	events = soup.find_all('tr')
	titles = []
	links = []
	imgs = []
	# init ImgurClient

	for i in range(push_num):
		titles.append(events[i].find_all('a')[1].text)
		links.append(ts_prefix + events[i].find_all('a')[1].get('href'))
		url = links[-1]
		res = requests.get(url)
		soup = BeautifulSoup(res.text, 'lxml')
		img_name = 'TS_' + events[i].find_all('a')[1].get('href').split('/')[-1]
		img_dom = soup.find_all('img', {'alt': titles[i]})
		if img_dom:
			https_url = upload_photo(img_dom[0].get('src'), img_name)
			print(https_url)
			imgs.append(https_url)
		else:
			imgs.append(no_image)
			print(no_image)
	return titles, links, imgs

def getFGO(push_num):
	FGO_url = 'https://www.fate-go.com.tw/newsmng/index.json'
	FGO_link_prefix = 'https://www.fate-go.com.tw/news.html#!news/4/1/'
	FGO_img_prefix = 'https://www.fate-go.com.tw/newsmng/'

	res = requests.get(FGO_url)
	all_infos = json.loads(res.text)
	activities = []
	for i, info in enumerate(all_infos):
		if info['title'].find('公告') == -1 and info['title'].find('維護') == -1:
			activities.append(info)
	titles = []
	links = []
	imgs = []
	for index in range(push_num):
		data = activities[-(index+1)]
		titles.append(data['title'])
		links.append(FGO_link_prefix+str(data['id']))
		res = requests.get(FGO_img_prefix+str(data['id'])+'.json')
		data = json.loads(res.text)
		soup = BeautifulSoup(data['content'], 'lxml')
		if soup.find('img'):
			imgs.append('https:' + soup.find('img').get('src'))
		else:
			imgs.append(no_image)
	return titles, links, imgs

def getRO(push_num):
	RO_url = 'https://rom.gnjoy.com.tw/news/index/type/event'
	RO_link_prefix = 'https://rom.gnjoy.com.tw'
	RO_img_prefix = 'https://rom.gnjoy.com.tw'

	titles = []
	links = []
	imgs = []
	res = requests.get(RO_url)
	soup = BeautifulSoup(res.text, 'lxml')
	tmp = soup.find_all('li')
	lists = []
	title_index = 2
	link_index = 0
	img_index = 1
	for content in tmp:
		if content.find('span'):
			lists.append(content)
	# check the 'a' element href values is valid for our code format
	check_index = []
	for index, content in enumerate(lists):
		if content.find('a').get('href').find('news') == -1 or  content.find('a').get('href').find('id') == -1:
			check_index.append(index)
	for i in range(len(check_index)):
		del lists[check_index[-(i+1)]]

	for i in range(push_num):
		titles.append(lists[i].find_all('span')[title_index].text)
		links.append(RO_link_prefix+lists[i].find_all('a')[link_index].get('href'))
		res = requests.get(links[i])
		soup = BeautifulSoup(res.text, 'lxml')
		img_name = 'RO_' + lists[i].find_all('a')[link_index].get('href').split('/')[-1]
		if soup.find_all('img')[img_index].get('src'):
			https_url = upload_photo(RO_img_prefix+soup.find_all('img')[img_index].get('src'), img_name)
			imgs.append(https_url)
		else:
			imgs.append(no_image)
	return titles, links, imgs

def getAoV(push_num):
	# push_num must be three, beacause of the website format
	aov_url = 'https://moba.garena.tw/news/Activity#guild'
	res = requests.get(aov_url)
	soup = BeautifulSoup(res.text, 'lxml')
	result = soup.find_all('div', {'class': 'event'})

	titles= []
	links = []
	imgs = []
	for i in range(push_num):
		title = result[i].find('div', {'class': 'event_title'}).text.replace(' ', '')
		titles.append(title.replace('\n', ''))
		links.append(result[i].a.get('href'))
		imgs.append(result[i].a.img.get('src'))
	return titles, links, imgs

def getLineageM(push_num):
	url = 'https://tw.beanfun.com/LineageM/Bulletins/include/Bulletins_Proxy.aspx?ServiceType=562&alt=0&Page=1&method=3&Kind=564&Pagesize=30'
	res = requests.get(url)
	data = json.loads(res.text)
	data = data['MyDataSet']['Table']

	titles = []
	links = []
	imgs = []

	for i in range(push_num):
		titles.append(data[i]['Title'])
		links.append(data[i]['UrlLink'])
		imgs.append(no_image)
	return titles, links, imgs

def getPokemon(push_num):
	pokemon_url = 'https://pokemongolive.com/zh_hant/post'
	links_prefix = 'https://pokemongolive.com'
	imgs_prefix = 'https://pokemongolive.com'
	date_class = 'grid__item--12-cols grid__item--2-cols--gt-lg grid__item post-list__date-item'
	title_class = 'grid__item--12-cols grid__item--10-cols--gt-lg grid__item post-list__title '
	res = requests.get(pokemon_url)
	res.encoding=('utf-8') # website encoding problem
	soup = BeautifulSoup(res.text, 'lxml')
	date = soup.find_all('div', {'class': date_class})
	title = soup.find_all('div', {'class': title_class})

	titles = []
	links = []
	imgs = []
	for i in range(push_num):
		if len(title[i].a.text) > 60:
			tmp = title[i].a.text[:57]+'...'
			titles.append(tmp)
		else:
			titles.append(title[i].a.text)
		links.append(links_prefix+title[i].a.get('href'))
		res = requests.get(links[i])
		res.encoding=('utf-8')
		soup = BeautifulSoup(res.text, 'lxml')
		img_url = soup.find('img', {'class': 'image__image '}).get('src')
		imgs.append(imgs_prefix+img_url)

	return titles, links, imgs

def createCarousel(titles, links, imgs, push_num):
	carousel_message = TemplateSendMessage(
		type = 'template',
		alt_text = 'TowerSaviors Template',
		template = CarouselTemplate(
			type = 'carousel',
			columns = [
				CarouselColumn(
					thumbnail_image_url = imgs[i],
					title = helper.activity_order[i],
					text = titles[i],
					actions = [
						URITemplateAction(
							type = 'uri',
							label = 'Detail',
							uri = links[i]
						)
					]
				) for i in range(push_num)
			]
		)
	)
	return carousel_message

if __name__ == '__main__':
	t, l, i = getTowerSavior()