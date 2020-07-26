import credentials, requests, json


# add new expense to Catalyst Content FreshBooks account
def add_contractor_expense(amount, date, vendor):
    # read access_token file to get most recent access token
    with open('access_token.json', 'r') as file:
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
