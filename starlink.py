import requests
import json
import tokens
import logging

class Starlink:

    def __init__(self):

        # Read tokens
        t = tokens.Tokens()
        token = t.read()

        form_data = {
            'grant_type': 'refresh_token',
            'client_id': 'mobileAppClientId',
            'refresh_token': token["refresh_token"]
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Send the POST request to auth get a new token
        response = requests.post("https://api.starlink.com/auth/connect/token", data=form_data, headers=headers)

        token = t.write(response.json()['access_token'], response.json()['refresh_token'])


        self.headers = {
            'Authorization': f'Bearer {token["access_token"]}'
        }

    def getUser(self, accNumber=""):
        cookies = {
            'starlink.com.account_number': accNumber
        }
        response = requests.get("https://api.starlink.com/webagg/v2/accounts/user?mobile=true", headers=self.headers, cookies=cookies)        
        json_data = response.json()

        return json_data

    def getUserAccounts(self, userSubjectId):

        response = requests.get("https://api.starlink.com/accounts/v1/accounts/contact/"+userSubjectId+"?limit=1000", headers=self.headers)
        json_data = response.json()

        return json_data
    
    def getServiceLines(self, accNumber=""):
        cookies = {
            'starlink.com.account_number': accNumber
        }
        response = requests.get("https://api.starlink.com/webagg/v2/accounts/service-lines", headers=self.headers, cookies=cookies)        
        json_data = response.json()

        return json_data

    def getUserInfo(self, userSubjectId, accNumber):
        cookies = {
            'starlink.com.account_number': accNumber
        }
        response = requests.get("https://api.starlink.com/webagg/v3/accounts/user/"+userSubjectId, headers=self.headers, cookies=cookies)
        logging.info(response.status_code)

        json_data = response.json()

        return json_data

    def getOrders(self, accNumber=""):
        cookies = {
            'starlink.com.account_number': accNumber
        }
        response = requests.get("https://api.starlink.com/webagg/v1/public/orders/customer-account", headers=self.headers, cookies=cookies)
        json_data = response.json()
        
        return json_data

    def getNextPayment(self, accNumber=""):
        cookies = {
            'starlink.com.account_number': accNumber
        }
        response = requests.get("https://api.starlink.com/webagg/v1/public/billing/next-payment", headers=self.headers, cookies=cookies)
        json_data = response.json()

        return json_data

    def getPaymentInfo(self, accNumber=""):
        cookies = {
            'starlink.com.account_number': accNumber
        }

        response = requests.get("https://api.starlink.com/accounts/v1/accounts/"+accNumber+"/payment-information", headers=self.headers, cookies=cookies)
        json_data = response.json()

        return json_data

    def getUsageData(self, assetNumber):
        response = requests.get("https://api.starlink.com/telemetryagg/v1/data-usage/asset/"+assetNumber+"/billing-cycle/all?includeUnknownDataBin=false", headers=self.headers)
        json_data = response.json()

        return json_data

    def pause(self, serviceLineNumber, accountNumber):

        cookies = {
            'starlink.com.account_number': accountNumber
        }

        # Define the payload
        payload = {
            'isPause': True
        }

        # Convert the payload to JSON format
        json_payload = json.dumps(payload)

        self.headers['Accept'] = 'application/json'
        self.headers['Content-Type'] = 'application/json'
        url = "https://api.starlink.com/webagg/v2/accounts/cancel-service/"+serviceLineNumber+"?returnEquipment=false"

        # Send the DELETE request
        response = requests.delete(url, headers=self.headers, data=json_payload, cookies=cookies)

        json_data = response.json()

        return json_data

    def resume(self, subscriptionReferenceId, accountNumber):
        # Send the PUT request
        cookies = {
            'starlink.com.account_number': accountNumber
        }

        response = requests.put("https://api.starlink.com/webagg/v1/public/subscriptions/line/"+subscriptionReferenceId+"/resume", headers=self.headers, cookies=cookies)
        
        logging.info('StarlinkResume HTTP trigger: ' + subscriptionReferenceId + " - " + str(response.status_code))

        json_data = response.json()

        return json_data

    def getAllInfo(self):

        # Get user contact info from default account
        serviceLines = self.getUser("")
        userInfo = serviceLines['content']['account']['contact']

        # Get Accounts associated with User
        acc = self.getUserAccounts(userInfo['subjectId'])
        accountInfo = acc['content']['results']

        # Loop through each account and get list of assets and services
        services = []

        for ai in accountInfo:
            sl = self.getServiceLines(ai['accountNumber'])
            np = self.getNextPayment(ai['accountNumber'])
            pi = self.getPaymentInfo(ai['accountNumber'])
            o = self.getOrders(ai['accountNumber'])

            ai['users'] = []
            for u in ai['contacts']:
                ui = self.getUserInfo(u['subjectId'], ai['accountNumber'])
                ai['users'].append(ui)

            for s in sl['content']['results'] :
                u = self.getUsageData(s['serviceLineNumber'])
                s['usageData'] = u['content']['billingCycles']
                s['accountNumber'] = ai['accountNumber']
                services.append(s)

            ai['paymentInfo'] = pi['content']
            ai['nextPayment'] = np['content']
            ai['orders'] = o['content']['results']
            
        # Merge all info into single json object
        obj = {
            'accounts': accountInfo,
            'services' : services
        }

        #logging.info(json.dumps(obj, indent=4))

        return obj