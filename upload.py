import requests, helper_functions, credentials


# add new expense to Catalyst Content FreshBooks account
def add_expense(amount, date, vendor):
    access_token = helper_functions.check_access_token()
    # url for post request  
    image_object = helper_functions.upload_image()
    x = requests.post('https://api.freshbooks.com/accounting/account/' + credentials.get_account_id() + '/expenses/expenses',
                      # JSON data to send
                      json={"expense": 
                            {"amount": { "amount": amount},
                             "categoryid": credentials.get_categoryid(),
                             "staffid": credentials.get_staffid(),
                             "date": date,
                             "vendor": vendor,
                             "attachment":
                            {"jwt": image_object["jwt"],
                             "media_type": image_object["media_type"]
                                }}},
                      # header to send with request
                      headers={"Api-Version": "alpha",
                               "Content-Type": "application/json",
                               "Authorization": "Bearer " + access_token})
    # print the returned data from the post request for verification
    print(x.text)
