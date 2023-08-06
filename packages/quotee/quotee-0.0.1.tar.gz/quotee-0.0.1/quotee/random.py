import json
import requests

class Quotee:
    def __init__(self):
        self.url = 'https://zenquotes.io/api/random'
        self.page = requests.get(self.url).json()
        self.random = self.page[0]
        self.quote = self.random['q']
        self.author = self.random['a']

if __name__ == '__main__':
	Quotee()