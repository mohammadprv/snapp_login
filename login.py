import re, requests
from bs4 import BeautifulSoup


#* URLs
get_otp_url = "https://app.snapp.taxi/api/api-passenger-oauth/v2/otp"
auth_url = "https://app.snapp.taxi/api/api-passenger-oauth/v2/auth"
balance_ulr = "https://app.snapp.taxi/api/api-base/v2/passenger/balance"
get_client_info = "https://app.snapp.taxi/service-worker.js"


#? REGEX PATTERNS
client_id_pattern = r'CLIENT_ID:"(\s*(\w+))"'
client_secret_pattern = r'CLIENT_SECRET:"([A-Za-z0-9!@#$%^&*()_+=-]+)"'


#? Validate phone number
phone_pattern = r'^\+98\d{10}$'
user_input = input("Enter phone number with +98: ")
if re.match(phone_pattern, user_input):
    print("Valid Iran phone number:", user_input)

    phone_number = {
        'cellphone': user_input
    }

    #? Send phone number to /api/api-passenger-oauth/v2/otp
    response_otp = requests.post(get_otp_url, data=phone_number);
    if response_otp.status_code == 200:
        print("POST request to < /api/api-passenger-oauth/v2/otp > was successful")
        print("Response content:", response_otp.text)
    else:
        print("POST request to < /api/api-passenger-oauth/v2/otp > failed with status code:", response_otp.status_code)
        print("Response content:", response_otp.text)


    #? Searching for client_id and client secret
    client_work_js = requests.get(get_client_info).text

    client_id_match = re.search(client_id_pattern, client_work_js)
    client_secret_match = re.search(client_secret_pattern, client_work_js)

    if client_id_match:
        client_id = client_id_match.group(1)
        print("Client_id Value:", client_id)
    else:
        print("Client_id not found in the response.")

    if client_secret_match:
        client_secret = client_secret_match.group(1)
        print("Client_secret Value:", client_secret)
    else:
        print("Client_secret not found in the response.")


    #? Send Data to /api/api-passenger-oauth/v2/auth
    otp = input("Enter OTP: ")

    data = {
        "grant_type":"sms_v2",
        "client_id": client_id,
        "client_secret": client_secret,
        "cellphone": user_input,
        "token": otp
    }

    auth_response = requests.post(auth_url, data=data)

    if auth_response.status_code == 200:
        
        print("POST request to < /api/api-passenger-oauth/v2/auth > was successful")
        response_json = auth_response.json();
        access_token = f'Bearer {response_json["access_token"]}'

        #? Request to /api/api-base/v2/passenger/balance
        custom_headers = {
            'Authorization': access_token,
        }

        balance_response = requests.post(balance_ulr, headers=custom_headers);
        if balance_response.status_code == 200:
            print("POST request to < /api/api-base/v2/passenger/balance > was successful")
            status = balance_response.json()['status']
            balance = balance_response.json()['data']['balance']
            transfer_credit = balance_response.json()['data']['transfer_credit']
            final_result = {
                'status': status,
                'balance': balance,
                'transfer_credit': transfer_credit
            }
            print(final_result);
        else: 
            print("POST request to < /api/api-base/v2/passenger/balance > failed with status code:", balance_response.status_code)
            print("Response content:", balance_response.text)

    else:
        print("POST request to < /api/api-passenger-oauth/v2/auth > failed with status code:", auth_response.status_code)
        print("Response content:", auth_response.text)








else:
    print("Invalid Iran phone number. Please enter a valid number.")
