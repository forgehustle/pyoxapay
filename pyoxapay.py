import json
from decimal import Decimal
from typing import Dict, Literal, Tuple
import requests
from pydantic import BaseModel, EmailStr, PositiveInt


class Oxapay():
    # class variables
    merchant_api_endpoint: str = "https://api.oxapay.com/merchants"
    payout_api_endpoint : str = "https://api.oxapay.com/api"

    def __init__(self, api_key : Tuple[str,str]):
        class ApiKey(BaseModel):
           merchant_api_key : str
           payout_api_key : str
        api_key = ApiKey(merchant_api_key=api_key[0], payout_api_key=api_key[1])
        self.merchant_api_key = api_key.merchant_api_key
        self.payout_api_key = api_key.payout_api_key

    def create_invoice(self, invoice_data: Dict) -> Dict: #create invoice 
        class InvoicePayload(BaseModel):
            merchant: str
            amount: Decimal
            currency: str
            callbackUrl: str
            underPaidCover: Decimal
            feePaidByPayer: Literal[0,1]
            lifeTime: PositiveInt
            email: EmailStr
            orderId: PositiveInt
            description: str
            returnUrl: str
        invoice_data["merchant"] = self.merchant_api_key
        payload = InvoicePayload(**invoice_data)
        payload = payload.model_dump()
        payload["amount"] = str(payload["amount"])
        payload["underPaidCover"] = str(payload["underPaidCover"])
        url: str = f"{self.merchant_api_endpoint}/request"
        headers: Dict[str, str] = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        response = requests.post(url=url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
          return {
              "status" : "ok",
              "data" : response.json()
          }
        else:
          return {
              "status" : "failed",
              "data" : response.json()
          }

    def create_white_lable(self,white_lable_data : Dict) -> Dict: #create invoice with white lable
        class WhitelLablePayload(BaseModel):
            merchant: str
            email: EmailStr
            orderId: PositiveInt
            description: str
            callbackUrl: str
            underPaidCover: Decimal
            feePaidByPayer: Literal[0,1]
            lifeTime: PositiveInt
            network: str
            payCurrency : str
            currency: str
            amount: Decimal
        white_lable_data["merchant"] = self.merchant_api_key
        payload = WhitelLablePayload(**white_lable_data)
        payload = payload.model_dump()
        payload["amount"] = str(payload["amount"])
        payload["underPaidCover"] = str(payload["underPaidCover"])
        url : str = f"{self.merchant_api_endpoint}/request/whitelabel"
        headers: Dict[str, str] = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        response = requests.post(url=url,headers=headers,data=json.dumps(payload))
        if response.status_code == 200:
          return {
              "status" : "ok",
              "data" : response.json()
          }
        else:
          return {
              "status" : "failed",
              "data" : response.json()
          }
    def create_static_wallet(self,revoke_wallet_data : Dict) -> Dict: #create a static wallet address for each user
       class StaticWalletPayload(BaseModel):
           merchant : str
           callbackUrl : str
           network : str
           currency : str
       revoke_wallet_data["merchant"] = self.merchant_api_key
       payload = StaticWalletPayload(**revoke_wallet_data)
       payload = payload.model_dump()
       url : str = f"{self.merchant_api_endpoint}/request/staticaddress"
       headers: Dict[str, str] = {
            "accept": "application/json",
            "content-type": "application/json"
        }
       response = requests.post(url=url,headers=headers, data=json.dumps(payload))
       if response.status_code == 200:
          return {
              "status" : "ok",
              "data" : response.json()
          }
       else:
          return {
              "status" : "failed",
              "data" : response.json()
          }
       
    def revoke_static_wallet(self,static_wallet_data : Dict) -> Dict:  #delete the static wallet address
       class RevokeStaticWallet(BaseModel):
            merchant : str
            address : str
       static_wallet_data["merchant"] = self.merchant_api_key
       payload = RevokeStaticWallet(**static_wallet_data)
       payload = payload.model_dump()
       url : str = f"{self.merchant_api_endpoint}/revoke/staticaddress"
       headers: Dict[str, str] = {
            "accept": "application/json",
            "content-type": "application/json"
        }
       response = requests.post(url=url, headers=headers, data=json.dumps(payload))
       if response.status_code == 200:
          return {
              "status" : "ok",
              "address" : payload["address"],
              "data" : response.json()
          }
       else:
          return {
              "status" : "failed",
              "data" : response.json()
          }
    
    def create_payout(self, payout_data : Dict) -> Dict:  #create a withdraw
        class PayoutPayload(BaseModel):
            key: str
            address: str
            amount: Decimal
            currency: str
            network : str
            description : str
            callbackUrl : str
        payout_data["key"] = self.payout_api_key 
        payload = PayoutPayload(**payout_data)
        payload = payload.model_dump()
        payload["amount"] = str(payload["amount"])
        url : str = f"{self.payout_api_endpoint}/send"
        headers: Dict[str, str] = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        response = requests.post(url=url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
          return {
              "status" : "ok",
              "data" : response.json()
          }
        else:
           return {
              "status" : "failed",
              "data" : response.json()
              }
    
    def get_account_balance(self,currency : str): #get account balance from account
        class AccountBalance(BaseModel):
           key : str
           currency : str
        payload = AccountBalance(key=self.payout_api_key,currency=currency)
        payload = payload.model_dump()
        url : str = f"{self.payout_api_endpoint}/balance"
        headers: Dict[str, str] = {
             "accept": "application/json",
             "content-type": "application/json"
         }
        response = requests.post(url=url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
           return {
              "status" : "ok",
              "data" : response.json()
           }
        else:
           return {
              "status" : "failed",
              "data" : response.json()
              }