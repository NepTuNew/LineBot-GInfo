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

line_bot_api = LineBotApi('ZExvrX3JjRJ0f4Qk8kGMSby3cJV7AyeqAaeBQx/zfyMO46IC4Jqf9WqNUKlZ8Ve8uIZ8M/QqVUacBTEtDf17hYIEjZT4C402DygjUjgqDRhpAFghh8RJeYhjwufFVceynNloh91IWbaSW8Zx2VDPXgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('839eeb12b33722f7cc347c0899cc10f8')
spreadsheet_key_path = '1lpqhd_ZUGTVayeNfBfAMXhz4Foidhbn4Aixb3NGsopc'
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
	time = datetime.datetime.now()
	gsheet.update_sheet(gss_client, spreadsheet_key_path, str(datetime.date.today())
		, str(time.hour)+':'+str(time.minute), event.message.text)
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