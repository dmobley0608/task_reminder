import requests
from bs4 import BeautifulSoup


class AutoDataRetrieval:
    def __init__(self):

        self.url = 'https://thinkkindness.org/all-things-kindness/a-list-of-100-compliments/'
        self.r = requests.get(self.url)
        self.page = BeautifulSoup(self.r.text, 'html.parser')
        self.complement_object = self.page.find_all('ol', class_='fancy_list')
        self.complements = []
    def get_complements(self):
        for complement in self.page.find_all('ol', class_='fancy_list'):
            for li in complement.findAll('li'):
                self.complements.append(li.text)
        return self.complements

