# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 11:46:57 2021

@author: SKY_SHY
"""

"""
Главный модуль, выполняющий запрос данных с внеш. сервиса
и отправляющий данные на сервер пользователя для их записи
и обновления
"""
from initialize_load_data import (receiver, 
                                  sender, 
                                  external_api_data_key, 
                                  record_method)
from recorder import Record

record = Record(receiver, sender, external_api_data_key)



if __name__ == "__main__":
    
    record.main(record_method)
