from invoice2data import extract_data
from invoice2data.extract.loader import read_templates
from invoice2data.input import pdftotext as pdftotextdef
from invoice2data.output import to_json
from datetime import datetime, timedelta
import pdftotext, os, calendar, credentials, requests, json, webbrowser, time


# reads a pdf file and parses the data to JSON
def read_file(filename, debug):
    # If debug is active, get PDF as string for debugging/template creation
    if debug is True:
        with open('INPUT/' + filename, 'rb') as f:
            pdf = pdftotext.PDF(f)
        print('\n\n'.join(pdf))
        
    templates = read_templates('TEMPLATES/')
    result = extract_data('INPUT/' + filename, templates, pdftotextdef)
    # if pdf read successful write JSON file
    if result != False:
        to_json.write_to_file(result, 'OUTPUT/' + os.path.splitext(filename)[0] + '.json', '%Y-%m-%d')
        
        # checks if due_date present in JSON and if not sets due date 1 month after invoice date
        with open('OUTPUT/' + os.path.splitext(filename)[0] + '.json', 'r+') as file:
            data = json.load(file)
            if "date_due" not in data:
                date = data["date"]
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                json_in = {"date_due":add_month(date_obj).strftime('%Y-%m-%d')}
                data.update(json_in)
                file.seek(0)
                json.dump(data, file, indent=4, sort_keys=True)
    # else add file name to error list and move on
    else:
        append_error(filename)


# clear error file
def clear_errors():
    open('OUTPUT/ERRORS.txt', 'w').close()


# adds file names to error file
def append_error(filename):
    with open('OUTPUT/ERRORS.txt', 'a') as file:
        file.write(filename + '\n')


# adds a month to any input date 
def add_month(dt0):
    start_date = dt0
    days_in_month = calendar.monthrange(start_date.year, start_date.month)[1]
    dt1 = start_date + timedelta(days=days_in_month)
    return dt1


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
    with open('access_token.json', 'r') as file:
        # check if current access token is expired
        if (time.time() >= float(json.load(file)['expires'])):
            get_access_token()
        file.seek(0)
        access_token = json.load(file)['access_token']
    x = requests.post('https://api.freshbooks.com/uploads/account/' + credentials.get_account_id() + '/images',
                      files={'test.jpg': open('INPUT/test.jpg', 'rb')},
                      headers={"Api-Version": "alpha",
                               "Content-Type": "application/json",
                               "Authorization": "Bearer " + access_token},
                      allow_redirects=True)
    print(x.text)


# add new expense to Catalyst Content FreshBooks account
def add_expense(amount, date, vendor):
    # read access_token file to get most recent access token
    with open('access_token.json', 'r') as file:
        # check if current access token is expired
        if (time.time() >= float(json.load(file)['expires'])):
            get_access_token()
        file.seek(0)
        access_token = json.load(file)['access_token']
        
    # url for post request   
    x = requests.post('https://api.freshbooks.com/accounting/account/' + credentials.get_account_id() + '/expenses/expenses',
                      # JSON data to send
                      json={"expense": 
                            {"amount": { "amount": amount},
                             "categoryid": credentials.get_categoryid(),
                             "staffid": credentials.get_staffid(),
                             "date": date,
                             "vendor": vendor}},
                      # header to send with request
                      headers={"Api-Version": "alpha",
                               "Content-Type": "application/json",
                               "Authorization": "Bearer " + access_token})
    # print the returned data from the post request for verification
    print(x.text)
