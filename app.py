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
		carousel_message = gameCrawler.createCarousel(t, l, i)
		line_bot_api.reply_message(
			event.reply_token, carousel_message
		)
	elif event.message.text in helper.fgo:
		print('Read word FGO!')
		t, l, i = gameCrawler.getFGO(4)
		carousel_message = gameCrawler.createCarousel(t, l, i)
		line_bot_api.reply_message(
			event.reply_token, carousel_message
		)
	elif event.message.text in helper.ro:
		print('Read word RO!')
		t, l, i = gameCrawler.getRO(4)
		carousel_message = gameCrawler.createCarousel(t, l, i)
		line_bot_api.reply_message(
			event.reply_token, carousel_message
		)
	else:
		gameCrawler.test()
		message = TextSendMessage(text=event.message.text)
		line_bot_api.reply_message(
			event.reply_token,
			message)
if __name__ == "__main__":
	app.run()