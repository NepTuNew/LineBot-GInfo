import gspread
from oauth2client.service_account import ServiceAccountCredentials


def auth_gss_client(path, scopes):
	credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scopes)
	return gspread.authorize(credentials)

def update_sheet(gss_client, key, date, time, message):
	wks = gss_client.open_by_key(key)
	sheet = wks.sheet1
	sheet.insert_row([date, time, message], 2)