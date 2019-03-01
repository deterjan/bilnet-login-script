import requests

STUDENT_ID = ""
PASSWORD = ""

session = requests.Session()
response = session.get('https://auth.bilkent.edu.tr/auth/login')

if "Off-Campus Access" in response.text:
	print("Login failed. Cause: Not connected to campus network.")
	exit(0)

cookie = session.cookies.get_dict()['bilnet-user']
headers = {'Cookie': 'bilnet-user=' + cookie}
data = {'next': '/auth/status', 'UserName': STUDENT_ID, 'Password': PASSWORD, 'agree': 'on'}

response = session.post('https://auth.bilkent.edu.tr/auth/login', headers=headers, data=data)

if "Login successful" in response.text:
	print("Login successful.")
elif "Invalid Username or Password" in response.text:
	print("Login failed. Cause: Invalid student ID or password.")
else:
	print("Login failed.")