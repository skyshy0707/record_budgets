# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 23:58:54 2021

@author: SKY_SHY
"""

"""
Модуль с реализованным классом Load_Data
Использовать как библиотеку
"""
import json
import logging
import logging.config
import requests
import time


logging.config.fileConfig('logging.ini')
logger = logging.getLogger('record_data')


class Load_Data():
    """
    класс предназначен для отправки get, post, put-запросов на 
    url REST API формата "http://hostname?"
    и выводу данных в формат словаря python постранично
    """
    
    def __init__(self,):
        self.headers = {}
        self.base_url = "http://budget.gov.ru/epbs/registry/7710568760-BUDGETS/data?"
        self.params = {}
        
    
    def set_headers(self, headers):
        """
        устанавливает заголовки в тело запроса
        """
        self.headers.update(headers)
    
    
    def set_base_url(self, base_url):
        """
        устанавливает базовый url REST API
        """
        self.base_url = base_url
        
        
    def set_params(self, params):
        """
        устанавливает параметры строки запроса к REST API
        """
        self.params.update(params)
    
    
    def get_raw_data_fromPage(self,):
        """
        получает данные с одной страницы с номером pageNum
        """
        
        return requests.get(self.base_url, 
                            params=self.params, 
                            headers=self.headers)
    
    
            
    def get_json(self, raw_data):
        """
        конвертирует данные в словарь python
        """
        return json.loads(raw_data.text)
    
    
    def secure_request(self,):
        """
        производит запрос к удалённому серверу:
        "http://hostname?"
        и возвращает необработанные данные
        """
        
        raw_data = self.get_raw_data_fromPage()
        
        # если статус ответа 4XX, то ждём:
        while raw_data.status_code in range(400, 452):
            time.sleep(30)
            raw_data = self.get_raw_data_fromPage()
        else:
            return raw_data
        
    
    def get_data(self,):
        """
        производит запрос к REST API с учётом 
        получения кода ответа 429 и возвращает
        данные в виде словаря python
        """
        
        raw_data = self.secure_request()
        return self.get_json(raw_data)
        
    
    def next_offset(self, offset=0):
        """
        обновляет параметры запроса, меняя смещение данных
        """
        
        self.params["offset"] = offset
        
        
    def get_data_by_current_page(self, offset=0):
        """
        получает данные с текущей страницы и возвращает их в формате 
        словаря python
        """

        data_json = self.get_data()
        self.next_offset(offset)
            
        
        if 'error' in data_json:
            raise KeyError("Неверная комбинация параметров REST API")
            
        return data_json
    
    def post_data(self, data):
        """
        отправляет данные на сервер пользователя, производя post-запрос
        """
        
        req = requests.post(self.base_url,
                            json=data,
                            params=self.params, 
                            headers=self.headers)
        
        if req.status_code in range(400, 600):
            
            
            logger.error(f"Данные {data}, полученные от внеш. api "\
                         f"вызвали ошибку с кодом ответа от целевого сервера "\
                         f"пользователя {req.status_code} при отправке "\
                         f"post-запроса")
                
        elif req.status_code == 200:
            logger.info(f"Данные {data} были успешно отправлены")

        
    def put_data(self, data):
        """
        отправляет данные на сервер пользователя, производя put-запрос
        """
        
        req = requests.put(self.base_url,
                           json=data,
                           params=self.params, 
                           headers=self.headers)
        
        # для добавления данных в журнал, вызвавшие ответ отличный от кода 200:
        if req.status_code in range(400, 600):
            
            """
            self.journal.append(("method=put", data, req.status_code))
            """
            
            logger.error(f"Данные {data}, полученные от внеш. api "\
                         f"вызвали ошибку с кодом ответа от целевого сервера "\
                         f"пользователя {req.status_code} при отправке "\
                         f"post-запроса")
                
        elif req.status_code == 200:
            logger.info(f"Данные {data} были успешно отправлены")