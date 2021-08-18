# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 11:35:23 2021

@author: SKY_SHY
"""

"""
Модуль с реализацией класса Record
Использовать как библиотеку
"""
class Record():
    
    """
    класс, предназначенный для отправки данных на запись на пользовательский 
    сервер.* 
    В конструктор класса передаются экз. класса Load_Data, заисываемые в перем.:
        
        self.receiver = receiver #запрашивает данные у внеш. сервера
        self.sender = sender #отправляет полученные данные от внеш. сервера
                             #на целевой сервер пользователя
                             
        self.self.external_api_data_key = external_api_data_key #см. ниже
    
        # ключ, по которому лежат данные в словаре, полученный в результате 
        сериализации ответа от внешнего сервера
        
        
    * Предполагается, что url-адрес post и put запроса на сервер пользователя
    совпадают
    """
    
    def __init__(self, receiver, sender, external_api_data_key):
        self.receiver = receiver
        self.sender = sender
        self.external_api_data_key = external_api_data_key
    
    
    def get_method(self, method):
        """
        возвращает вызываемый метод экз. класса, записанный в перем. self.sender 
        в зависимости от значения переданного аргумента method
        """
        
        if method not in ("post", "put",):
            raise ValueError("Переданное символьное имя метода недопустимо"\
                             "Допустимые: 'post', 'put'")
                
        method = "_".join((method, "data"))
        
        return getattr(self.sender, method)
    
    
    def send(self, method, data):
        """
        вызывает метод в экз. класса, который записан в перем. self.sender
        и отправляет данные на сервер для их записи или обновления, в
        зависимости от переданнного метода в арг. method
        """
        sending = self.get_method(method)
        sending(data)
        
        
    def main(self, method):
        """
        производит редактирование или добавление обектов пользовательскую БД,
        в зависимости от значения переданного аргумента method
        """
        self.receiver.set_params({"offset": 0})
        
        offset = 0
        while True:
    
            data_json = self.receiver.get_data_by_current_page(offset)
    
    
            for item in data_json[self.external_api_data_key]:
                
                self.send(method, item)
        
            offset += len(data_json[self.external_api_data_key])
            if not data_json[self.external_api_data_key]:
                break
        