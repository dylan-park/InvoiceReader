import credentials, requests, json, webbrowser


# gets a new access token (valid for 12 hours)
def get(code):
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
    return x.json()['access_token']

    
# opens web browser and prompt user to complete auth verification and to input the returned code
webbrowser.open(credentials.get_auth_url())
code = input('Enter the auth code from URL: ')

# run the get method, and replace access_token file with new token
access_token = get(code)
with open('access_token.json', 'w') as file:
    file.write(json.dumps({'access_token': access_token}))
print('New auth code set')
