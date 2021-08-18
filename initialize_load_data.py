# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 11:11:06 2021

@author: SKY_SHY
"""

"""
модуль, инициализирующий параметры для передачи их в конструкторы 
экз. класса Load_Data
Используется как библиотека
"""


import json

from load_data import Load_Data
from receive_cmd_parameters import CMD_PARAMS

           
#параметры строки запроса к внешнему REST API:

external_api_data_key = CMD_PARAMS["data_key"]
external_api_base_url = CMD_PARAMS["url"]
external_api_headers = json.loads(CMD_PARAMS["headers"])
external_api_params = json.loads(CMD_PARAMS["params"])


#параметры строки запроса к REST API пользователя, принимающего данные:

cli_api_url = CMD_PARAMS["cli_url"]
cli_api_headers = json.loads(CMD_PARAMS["cli_headers"])
edit_instance_by_fields = CMD_PARAMS["edit_instance_by_fields"]

#параметры для записи данных, полученных от REST API в пользовательскую БД
cli_api_params = dict(model = CMD_PARAMS["model"],
                      serialize_fields = CMD_PARAMS["serialize_fields"],
                      renaming_fields = CMD_PARAMS["renaming_fields"],
                      refilling_fields = CMD_PARAMS["refilling_fields"], 
                      edit_instance_by_fields = edit_instance_by_fields)

record_method = CMD_PARAMS["record_method"]


# инициализация экз.-в класса Load_Data --- для получения и для отправки данных:
receiver = Load_Data()
sender = Load_Data()

receiver.set_headers(external_api_headers)
receiver.set_base_url(external_api_base_url)
receiver.set_params(external_api_params)

sender.set_headers(cli_api_headers)
sender.set_base_url(cli_api_url)
sender.set_params(cli_api_params)