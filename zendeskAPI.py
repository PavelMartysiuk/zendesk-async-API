import aiohttp

import asyncio

import json


class Abstract:

    def __init__(self):
        self.headers = {
            'Authorization':
                'Bearer 6b500accbb3340c5ac99ba822ab50996bbe6c6a862c5052b1105dea2e1f73f89',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    async def fetch(self, client, url, method, data):
        if method == 'get':
            async with client.get(url) as resp:
                return await resp.text()
        elif method == 'post':
            async with client.post(url, data=json.dumps(data)) as resp:
                return await resp.text()
        elif method == 'put':
            async with client.put(url, data=json.dumps(data)) as resp:
                return await resp.text()

    async def response(self, url, method, data=None):
        async with aiohttp.ClientSession(headers=self.headers) as client:
            response = await self.fetch(client, url, method, data)
            return response


class AccountAPI(Abstract):

    async def get_account(self):
        """Func returns account data by token"""
        method = 'get'
        url = 'https://api.getbase.com/v2/accounts/self'
        response = await self.response(url, method)
        print(response, 'account get')
        return response


class LeadsAPI(Abstract):
    def __init__(self):
        self.url = 'https://api.getbase.com/v2/leads'
        super().__init__()

    async def get_leads(self):
        method = 'get'
        response = await self.response(self.url, method)
        print(response, 'lead get')
        return response

    async def post_leads(self):
        method = 'post'
        data = {
            "data": {
                "first_name": "Mark",
                "last_name": "Johnson",
                "organization_name": "Design Services Company",
                "source_id": 10,
                "title": "CEO",
                "description": "I know him via Tom",
                "industry": "Design Services",
                "website": "http://www.designservice.com",
                "email": "mark@designservices.com",
                "phone": "508-778-6516",
                "mobile": "508-778-6516",
                "fax": "+44-208-1234567",
                "twitter": "mjohnson",
                "facebook": "mjohnson",
                "linkedin": "mjohnson",
                "skype": "mjohnson",
                "address": {
                    "line1": "2726 Smith Street",
                    "city": "Hyannis",
                    "postal_code": "02601",
                    "state": "MA",
                    "country": "US"
                },
                "tags": [
                    "important"
                ],
                "custom_fields": {
                    "known_via": "tom"
                }
            }
        }
        response = await self.response(self.url, method, data)
        print(response, 'lead post')
        return response

    async def get_one_lead(self):
        method = 'get'
        post_lead = await self.post_leads()
        lead_id = json.loads(post_lead)['data']['id']
        self.one_lead_url = self.url + f'/{lead_id}'
        response = await  self.response(self.one_lead_url, method)
        print(response, 'lead get one')
        return response

    async def update_lead(self):
        method = 'put'
        data = {
            "data": {
                "tags": [
                    "important",
                    "friend"
                ]
            }
        }
        await self.get_one_lead()
        response = await self.response(self.one_lead_url, method, data)
        print(response, 'update lead')
        return response


class ContactAPI(Abstract):
    def __init__(self):
        self.url = 'https://api.getbase.com/v2/contacts'
        super().__init__()

    async def post_contact(self):
        method = 'post'
        data = {
            "data": {
                "contact_id": 1,
                "name": "Mark Johnson",
                "first_name": "Mark",
                "last_name": "Johnson",
                "title": "CEO",
                "description": "I know him via Tom",
                "industry": "Design Services",
                "website": "http://www.designservice.com",
                "email": "mark@designservices.com",
                "phone": "508-778-6516",
                "mobile": "508-778-6516",
                "fax": "+44-208-1234567",
                "twitter": "mjohnson",
                "facebook": "mjohnson",
                "linkedin": "mjohnson",
                "skype": "mjohnson",
                "address": {
                    "line1": "2726 Smith Street",
                    "city": "Hyannis",
                    "postal_code": "02601",
                    "state": "MA",
                    "country": "US"
                },
                "tags": [
                    "contractor",
                    "early-adopter"
                ],
                "custom_fields": {
                    "referral_website": "http://www.example.com"
                }
            }
        }
        response = await  self.response(self.url, method, data)
        self.one_cotacts_url = self.url + f'/{json.loads(response)["data"]["id"]}'
        print(response, 'contact post')
        return response

    async def get_contacts(self):
        method = 'get'
        await self.post_contact()
        response = await self.response(self.url, method)
        print(response, 'contact get')
        return response

    async def get_one_contact(self):
        method = 'get'
        await self.get_contacts()
        response = await self.response(self.one_cotacts_url, method)
        print(response, 'get_one_contact ')
        return response

    async def update_one_contact(self):
        method = 'put'
        data = {
            "data": {
                "customer_status": "current",
                "tags": [
                    "contractor",
                    "early-adopter"
                ],
                "custom_fields": {
                    "referral_website": "http://www.example.com"
                }
            }
        }
        await self.get_one_contact()
        response = await self.response(self.one_cotacts_url, method, data)
        print(response, 'update contact')
        return response


if __name__ == '__main__':
    account = AccountAPI()
    lead = LeadsAPI()
    contact = ContactAPI()
    aioloop = asyncio.get_event_loop()
    tasks = (aioloop.create_task(account.get_account()),
             aioloop.create_task(lead.get_leads()),
             aioloop.create_task(lead.update_lead()),
             aioloop.create_task(contact.update_one_contact()),

             )
    aioloop.run_until_complete(asyncio.wait(tasks))
