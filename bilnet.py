import requests
import argparse

STUDENT_ID = ""
PASSWORD = ""

EXAMPLE_URL = "http://example.org"
PORTAL_URL = "https://auth.bilkent.edu.tr/"
LOGIN_URL = "https://auth.bilkent.edu.tr/auth/login"
LOGOUT_URL = "https://auth.bilkent.edu.tr/auth/logout"

OK = 0
UNSPECIFIED_FAILURE = -1
OFF_CAMPUS = -2
INVALID_CREDENTIALS = -3
NO_COOKIE = -4
FAULTY_COOKIE = -5
BAD_REQUEST = -6
ALREADY_CONNECTED = -7

parser = argparse.ArgumentParser(description="script to manage Bilnet captive portal connection")
parser.add_argument('-l', '--logout', action='store_true', help="set this flag to logout")
parser.add_argument('-f', '--force', action='store_true', help="set this flag to skip internet connection check")
parser.add_argument('-i', '--id', action='store', dest="id", default=STUDENT_ID, help="manually input student id")
parser.add_argument('-p', '--password', action='store', dest="password", default=PASSWORD, help="manually input Bilnet password")
args = parser.parse_args()

def main():
	if args.logout:
		logout_result = logout()
		print(make_result_string("Logout", logout_result))
	else:
		session = requests.Session()
		request_cookie_result = request_cookie(session)
		cookie = extract_bilnet_cookie(session)

		if request_cookie_result != OK:
			print(make_result_string("Login", request_cookie_result))
		elif cookie is None:
			print(make_result_string("Login", NO_COOKIE))
		else:
			connected = False
			if not args.force:
				connected = check_connection()

			if args.force or not connected:
				login_result = login(args.id, args.password, cookie)
				print(make_result_string("Login", login_result))
			elif connected:
				print(make_result_string("Login", ALREADY_CONNECTED))

# check if internet connection exists
def check_connection():
	response = requests.get(EXAMPLE_URL)
	return "Example Domain" in response.text

# Check if on-campus and get login cookie if so
def request_cookie(session):
	response = session.get(PORTAL_URL)
	if "Bad Request" in response.text:
		return BAD_REQUEST
	if "Off-Campus Access" in response.text:
		return OFF_CAMPUS
	else:
		return OK

def extract_bilnet_cookie(session):
	cookies = session.cookies.get_dict()
	if 'bilnet-user' in cookies:
		return cookies['bilnet-user']
	else:
		return None

def login(username, password, cookie):
	headers = {'Cookie': 'bilnet-user=' + cookie}
	data = {'next': '/auth/status', 'UserName': username, 'Password': password, 'agree': 'on'}
	response = requests.post(LOGIN_URL, headers=headers, data=data)

	if "Login successful" in response.text:
		return OK
	elif "Invalid Username or Password" in response.text:
		return INVALID_CREDENTIALS
	else:
		return UNSPECIFIED_FAILURE

def logout():
	response = requests.get(LOGOUT_URL)
	if "Logout successful" in response.text:
		return OK
	elif "Off-Campus Access" in response.text:
		return OFF_CAMPUS
	else:
		return UNSPECIFIED_FAILURE

def make_result_string(operation, result):
	if result == 0:
		return operation + " successful."
	else:
		result_string = operation + " failed."
		if result == OFF_CAMPUS:
			return result_string + " Not connected to campus network."
		elif result == INVALID_CREDENTIALS:
			return result_string + " Invalid student ID or password."
		elif result == NO_COOKIE:
			return result_string + " Bilnet server didn't return required cookie."
		elif result == BAD_REQUEST:
			return result_string + " Something went wrong with the request."
		elif result == ALREADY_CONNECTED:
			return "You already have internet connection."
		else:
			return result_string
try:
	main()
except requests.ConnectionError:
	print("Failed. No network connection.")