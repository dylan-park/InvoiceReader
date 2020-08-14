from datetime import timedelta
import calendar, credentials, requests, json, webbrowser, time


# adds a month to any input date 
def add_month(dt0):
    start_date = dt0
    days_in_month = calendar.monthrange(start_date.year, start_date.month)[1]
    dt1 = start_date + timedelta(days=days_in_month)
    return dt1


# clear error file
def clear_errors():
    open('OUTPUT/ERRORS.txt', 'w').close()


# adds file names to error file
def append_error(filename):
    with open('OUTPUT/ERRORS.txt', 'a') as file:
        file.write(filename + '\n')


# checks if access token is still valid, gets new token if not
def check_access_token():
    with open('access_token.json', 'r') as file:
        if (time.time() >= float(json.load(file)['expires'])):
            get_access_token()
        file.seek(0)
        return json.load(file)['access_token']


# gets a new access token (valid for 12 hours)
def get_access_token():
    # opens web browser and prompt user to complete auth verification and to input the returned code
    webbrowser.open(credentials.get_auth_url())
    code = input('Enter the auth code from URL: ')
    # url for post request
    x = requests.post('https://api.freshbooks.com/auth/oauth/token',
                      # JSON data to send
                      json={"grant_type": "authorization_code",
                    "client_secret": credentials.get_client_secret(),
                    "code": code,
                    "client_id": credentials.get_client_id(),
                    "redirect_uri": credentials.get_redirect_uri()},
                      # header to send with request
                      headers={"Api-Version": "alpha",
                               "Content-Type": "application/json"})
    expires = int(x.json()['expires_in']) + int(x.json()['created_at'])
    
    # run the get method, and replace access_token file with new token
    with open('access_token.json', 'w') as file:
        file.write(json.dumps({'access_token': x.json()['access_token'], 'expires': expires}))
    print('New auth code set')


# upload an image for use in FreshBooks post requests
def upload_image():
    access_token = check_access_token()
    x = requests.post('https://api.freshbooks.com/uploads/account/' + credentials.get_account_id() + '/images',
                data={},
                files=[('content', open('INPUT/test.jpg', 'rb'))],
                headers={"Authorization": "Bearer " + access_token})
    return (x.json()["image"])
