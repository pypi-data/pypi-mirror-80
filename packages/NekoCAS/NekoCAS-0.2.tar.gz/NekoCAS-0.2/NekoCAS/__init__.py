name = "NekoCAS"

import requests


class CAS:
    def __init__(self, domain, secret):
        self.domain = domain
        self.secret = secret

    def set_domain(self, domain):
        self.domain = domain

    def set_secret(self, secret):
        self.secret = secret

    def validate(self, ticket):
        params = {
            'service': self.secret,
            'ticket': ticket
        }
        target_url = self.domain + "/validate"
        try:
            r = requests.get(target_url, params=params)
            r.raise_for_status()
            r = r.json()

            if not r['success']:
                return None, 'invalid ticket'

            return {
                       'name': r['data']['name'],
                       'email': r['data']['email'],
                       'token': r['data']['token'],
                       'message': r['message']
                   }, None
        except requests.RequestException as e:
            return None, e.message
