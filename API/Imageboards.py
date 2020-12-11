import requests
import json

class Imageboards:
    syte = ""
    with open('API/API.json', 'r') as file:
            api = json.load(file)
    def __init__(self, syte, **param):
        """
        docstring
        """
        self.syte = syte
    
    
    def getImages(self, **param):
        """
        Получение артов
        """
        return requests.get(self.syte + self.api[self.syte] + ' ' + param.get('tags','') + '&limit=' + str(param['limit'])).json()


    def getTags(self, id):
        """
        Получение тегов определенного арта по айди
        """
        tag = ''
        try:
            for tags in requests.get(self.syte + self.api[self.syte] + ' id:' + str(id)).json()[0]["tags"].split():
                tag += '#' + tags + ' '
            return tag[:4096]
        except:
            for tags in requests.get(self.syte + self.api[self.syte] + ' id:' + str(id)).json()[0]["tag_string"].split():
                tag += '#' + tags + ' '
            return tag[:4096]

    
    def getFileUrl(self, id):
        """
        Получение прямой ссылки на арт
        """
        return requests.get(self.syte + self.api[self.syte] + ' id:' + str(id)).json()[0]["file_url"]