from flask import Flask, request, abort

from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	MessageEvent, TextMessage, TextSendMessage,
)
import gameCrawler
import gsheet
import helper
import datetime
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')
spreadsheet_key_path = 'GOOGLE_SHEET_KEY_PATH'
spreadsheet_favorite_key_path = 'GOOGLE_SHEET_KEY_PATH'
gss_client = gsheet.auth_gss_client('linebot-auth.json', ['https://spreadsheets.google.com/feeds'])


@app.route("/callback", methods=['POST'])
def callback():
	signature = request.headers['X-Line-Signature']
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)
	return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
	gsheet.update_sheet(gss_client, spreadsheet_key_path, time.split(' ')[0]
		, time.split(' ')[1], event.message.text)
	if event.message.text in helper.helps:
		message = TextSendMessage(text=helper.hint)
		line_bot_api.reply_message(
			event.reply_token, message
		)
	elif event.message.text in helper.ts:
		print('Read word 神魔之塔!')
		t, l, i = gameCrawler.getTowerSavior(4)
		carousel_message = gameCrawler.createCarousel(t, l, i, 4)
		line_bot_api.reply_message(
			event.reply_token, carousel_message
		)
	elif event.message.text in helper.fgo:
		print('Read word FGO!')
		t, l, i = gameCrawler.getFGO(4)
		carousel_message = gameCrawler.createCarousel(t, l, i, 4)
		line_bot_api.reply_message(
			event.reply_token, carousel_message
		)
	elif event.message.text in helper.ro:
		print('Read word RO!')
		t, l, i = gameCrawler.getRO(4)
		carousel_message = gameCrawler.createCarousel(t, l, i, 4)
		line_bot_api.reply_message(
			event.reply_token, carousel_message
		)
	elif event.message.text in helper.aov:
		print('Read word 傳說對決')
		t, l, i = gameCrawler.getAoV(3)
		carousel_message = gameCrawler.createCarousel(t, l, i, 3)
		line_bot_api.reply_message(
			event.reply_token, carousel_message
		)
	elif event.message.text in helper.lineageM:
		print('Read word 天堂')
		t, l, i = gameCrawler.getLineageM(4)
		carousel_message = gameCrawler.createCarousel(t, l, i, 4)
		line_bot_api.reply_message(
			event.reply_token, carousel_message
		)
	elif event.message.text in helper.pokemongo:
		print('Read word 寶可夢')
		t, l, i = gameCrawler.getPokemon(4)
		carousel_message = gameCrawler.createCarousel(t, l, i, 4)
		line_bot_api.reply_message(
			event.reply_token, carousel_message
		)
	elif event.message.text == '我的最愛':
		if gsheet.check_favorite(gss_client, spreadsheet_favorite_key_path, event.source.user_id):
			choose = gsheet.check_favorite(gss_client, spreadsheet_favorite_key_path, event.source.user_id)
			if choose == 1:
				print('Read word 神魔之塔!')
				t, l, i = gameCrawler.getTowerSavior(4)
				carousel_message = gameCrawler.createCarousel(t, l, i, 4)
				line_bot_api.reply_message(
					event.reply_token, carousel_message
				)
			elif choose == 2:
				print('Read word FGO!')
				t, l, i = gameCrawler.getFGO(4)
				carousel_message = gameCrawler.createCarousel(t, l, i, 4)
				line_bot_api.reply_message(
					event.reply_token, carousel_message
				)
			elif choose == 3:
				print('Read word RO!')
				t, l, i = gameCrawler.getRO(4)
				carousel_message = gameCrawler.createCarousel(t, l, i, 4)
				line_bot_api.reply_message(
					event.reply_token, carousel_message
				)
			elif choose == 4:
				print('Read word 傳說對決')
				t, l, i = gameCrawler.getAoV(3)
				carousel_message = gameCrawler.createCarousel(t, l, i, 3)
				line_bot_api.reply_message(
					event.reply_token, carousel_message
				)
			elif choose == 5:
				print('Read word 天堂')
				t, l, i = gameCrawler.getLineageM(4)
				carousel_message = gameCrawler.createCarousel(t, l, i, 4)
				line_bot_api.reply_message(
					event.reply_token, carousel_message
				)
			elif choose == 6:
				print('Read word 寶可夢')
				t, l, i = gameCrawler.getPokemon(4)
				carousel_message = gameCrawler.createCarousel(t, l, i, 4)
				line_bot_api.reply_message(
					event.reply_token, carousel_message
				)
		else:
			line_bot_api.reply_message(
			event.reply_token, TextSendMessage(text="你還沒有設定我的最愛喔！"))
	elif event.message.text == '我變心了':
		line_bot_api.reply_message(
			event.reply_token, TextSendMessage(text="範例：設定最愛-編號(only one)"))
	elif event.message.text.find('設定最愛') != -1:
		seg = event.message.text.split('-')
		if len(seg) != 2 or not seg[1].isdigit():
			line_bot_api.reply_message(
			event.reply_token, TextSendMessage(text="格式不符喔！"))
		elif not (int(seg[1]) in range(1,7)):
			line_bot_api.reply_message(
			event.reply_token, TextSendMessage(text="編號不在提供的服務項目中喔！"))
		else:
			gsheet.update_favorite(gss_client, spreadsheet_favorite_key_path, event.source.user_id, int(seg[1]))
			line_bot_api.reply_message(
			event.reply_token, TextSendMessage(text="設定完成！"))
	elif event.message.text.find('聯絡作者') != -1:
		line_bot_api.reply_message(
			event.reply_token, TextSendMessage(text="可以將問題或建議透過email回報給我！非常感謝！\nEmail:\nanderson08121995@gmail.com"))
	else:
		message = TextSendMessage(text=helper.hint)
		line_bot_api.reply_message(
			event.reply_token,
			message)
if __name__ == "__main__":
	app.run()