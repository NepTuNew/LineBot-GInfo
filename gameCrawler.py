import requests
from bs4 import BeautifulSoup
from imgurpython import ImgurClient
import json
import time

from linebot.models import (
	CarouselTemplate, TemplateSendMessage, CarouselColumn, URITemplateAction
)

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

def createCarousel(titles, links, imgs):
	carousel_message = TemplateSendMessage(
		type = 'template',
		alt_text = 'TowerSaviors Template',
		template = CarouselTemplate(
			type = 'carousel',
			columns = [
				CarouselColumn(
					thumbnail_image_url = imgs[0],
					title = 'Lastest Activity',
					text = titles[0],
					actions = [
						URITemplateAction(
							type = 'uri',
							label = 'Detail',
							uri = links[0]
						)
					]
				),
				CarouselColumn(
					thumbnail_image_url = imgs[1],
					title = 'Second Activity',
					text = titles[1],
					actions = [
						URITemplateAction(
							type = 'uri',
							label = 'Detail',
							uri = links[1]
						)
					]
				),
				CarouselColumn(
					thumbnail_image_url = imgs[2],
					title = 'Third Activity',
					text = titles[2],
					actions = [
						URITemplateAction(
							type = 'uri',
							label = 'Detail',
							uri = links[2]
						)
					]
				),
				CarouselColumn(
					thumbnail_image_url = imgs[3],
					title = 'Fourth Activity',
					text = titles[3],
					actions = [
						URITemplateAction(
							type = 'uri',
							label = 'Detail',
							uri = links[3]
						)
					]
				)

			]
		)
	)
	return carousel_message

if __name__ == '__main__':
	t, l, i = getTowerSavior()