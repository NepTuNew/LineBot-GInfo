import gspread
from oauth2client.service_account import ServiceAccountCredentials


def auth_gss_client(path, scopes):
	credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scopes)
	return gspread.authorize(credentials)

def update_sheet(gss_client, key, date, time, message):
	wks = gss_client.open_by_key(key)
	sheet = wks.sheet1
	sheet.insert_row([date, time, message], 2)

def update_favorite(gss_client, key, user_id, favorite):
	wks = gss_client.open_by_key(key)
	sheet = wks.sheet1
	lists = sheet.get_all_values()
	del lists[0]
	for index, row in enumerate(lists):
		if row[0] == user_id:
			sheet.update_cell(index+2, 2, favorite)
			return
	sheet.insert_row([user_id, favorite], 2)

def check_favorite(gss_client, key, user_id):
	wks = gss_client.open_by_key(key)
	sheet = wks.sheet1
	lists = sheet.get_all_values()
	del lists[0]
	for row in lists:
		if row[0] == user_id:
			return int(row[1])
	return False