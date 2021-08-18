# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 11:33:44 2021

@author: SKY_SHY
"""

"""
модуль считывания параметров командной строки
Используется как библиотека
"""
import argparse
import configparser
import json
import inspect
import os
from urllib.parse import urlparse 


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)


parser = argparse.ArgumentParser()

config = configparser.ConfigParser()
config.read(os.path.join(parentdir, 'budgets\\config.ini'))


# методы проверки типа:
def is_model_fmt(model):
    """
    проверяет введённое значение параметра 
    --model на стиль записи  django
    """
    
    parts = model.split(".")
    
    if "" not in parts and len(parts) == 2:
        return model
    raise ValueError(f"Формат модели {model} не действителен")
    
    

def is_recitation(a_str):
    """
    проверяет, передана ли строка с перечитслением компонентов
    через разделитель
    """
    
    parts = a_str.split(",")
    
    if "" not in parts:
        return a_str
    raise ValueError(f"Строка {a_str} импеет не верный формат"\
                     "Используйте разделитель ',' для разделения компонентов")
    

def is_correct_json(a_str):
    """
    проверяет имеет ли строка a_str корректный json формат
    """
    
    try:
        json.loads(a_str)
    except json.JSONDecodeError:
        
        try:
            a_str = a_str.replace("\'", "\"")
            json.loads(a_str)
        except json.JSONDecodeError:
            print(f"Строка {a_str} имеет некорректный json формат")
        
        else:
            return a_str
        
    else:
        return a_str
    

def is_correct_record_method(record_method):
    """
    проверяет, входит ли record_method 
    в список допустимых значений
    """
    methods = {"create": "post", "update": "put"}
    
    if record_method not in methods:
        
        raise ValueError(f"Недопустимое значение {record_method} параметра "\
                         "--record_method "\
                          "Допустимыми являются \"update\", \"create\"")
            
    return methods[record_method]
    

def is_url(url):
    """
    проверяет на корректность url синтаксиса протокола http/https
    """
    url_attrs = urlparse(url)
    
    if not (url_attrs.scheme, url_attrs.netloc):
        raise ValueError(f"Введенный --url: {url} имеет некорректный формат")
    return url




parser.add_argument("--model", 
                    help="""
                         Модель, в которую загружаются данные с внеш. api. 
                         Следует указывать в синтаксисе django: 
                            \"<имя_приложения>.<Класс_модели>\"
                         """,
                    type=is_model_fmt,
                    default=config["record_params"]["model"])

parser.add_argument("--serialize_fields", 
                    help="Поля модели model, подлежащие сериализации. "\
                        "Следует указывать перечислением: "\
                            "\"field1, field2, ..., fieldn\"",
                    type=is_recitation,
                    default=config["record_params"]["serialize_fields"])

parser.add_argument("--renaming_fields", 
                    help="""
                         Переименуемые поля в данных, полученных от внеш. api.
                         Следует указать словарь, ключами которого являются 
                         имена полей данных, предоставленные внеш. api, а 
                         значениями  являются имена полей соотвествующие именам 
                         в классе модели:
                             \"{'api_field_name': 'actual_model_field_name'}\"
                         """,
                    type=is_correct_json,
                    default=config["record_params"]["renaming_fields"])

parser.add_argument("--refilling_fields", 
                    help="""
                         Поля, порядок заполнения которых в модели model 
                         отличается от их значений в данных, предоставленных
                         внешним api.
                         Следует указать словарь, ключами которого являются 
                         имена полей модели, данные которой загружаются на 
                         целевой сервер пользователя, а значения имеют след. 
                         структуру: \n
                             
                             "{'map': '<имя_приложения>.<Класс_модели>.<поле>', 
                               'fill': '<поле>'}", \n 
                             
                         где 'map' --- ключ, указывающий на поле, по которому, 
                         следует выбирать экз. модели 
                         <имя_приложения>.<Класс_модели> в БД целевого сервера 
                         пользователя. Значение поля 
                         <имя_приложения>.<Класс_модели>.<поле> будет 
                         соответсвовать значению в данных, полученных от 
                         внешнего сервера, которое находится там по имени 
                         ключа в refilling_fields,
                         
                         'fill' --- ключ, указывающий на имя поля в выбранном 
                         по ключу 'map' из БД целевого сервера пользователя 
                         экземпляре модели, значением которого следует 
                         заменить значение поля в данных, полученных от 
                         внешнего api.
                         
                         Подробнее см. описание метода 
                         <path_to_project>.for_serializer.update_data_serializer.rerecord_values,
                         
                         где path_to_project --- пусть к папке с проектом
                         целевого пользовательского сервера на django
                         """,
                    type=is_correct_json,
                    default=config["record_params"]["refilling_fields"])

parser.add_argument("--record_method", 
                    help="Метод записи данных, полученных от внеш. api в "\
                         "целевую БД пользователя.",
                    type=is_correct_record_method,
                    default=config["record_params"]["record_method"])


parser.add_argument("--url", 
                    help="URL-адрес REST API",
                    type=is_url,
                    default=config["external_api_params"]["base_url"])

parser.add_argument("--data_key", 
                    help="Ключ обращения к данным, пришедшим в теле ответа",
                    default=config["external_api_params"]["data_key"])

parser.add_argument("--headers", 
                    help="""
                         Заголовки тела запроса к REST API.
                         Укажите словарь с необходимыми заголовками обновления 
                         сессии и параметрами авторизации по необходимости:
                             \"{'User-Agent': 'value', 
                                'Authorization': 'Bearer XXXXXXXXXXXX'}\"
                         """,
                    type=is_correct_json,
                    default=config["external_api_params"]["headers"])

parser.add_argument("--params", 
                    help="""
                         Параметры строки запроса к REST API
                         Укажите словарь параметров, предъявляемый внешним 
                         сервером, для выполнения get-запроса на получение 
                         данных, например:
                             \"{'param1': int, 'param2': 'str', ...}\"
                         """,
                    type=is_correct_json,
                    default=config["external_api_params"]["params"])



parser.add_argument("--cli_url", 
                    help="URL-адрес REST API",
                    type=is_url,
                    default=config["cli_api_params"]["base_url"])

parser.add_argument("--cli_headers", 
                    help="""
                         Заголовки тела запроса к REST API.
                         Укажите словарь с необходимыми заголовками обновления 
                         сессии и параметрами авторизации по необходимости:
                             \"{'User-Agent': 'value', 
                                'Authorization': 'Bearer XXXXXXXXXXXX'}\"
                         """,
                    type=is_correct_json,
                    default=config["cli_api_params"]["headers"])

parser.add_argument("--edit_instance_by_fields", 
                    help="""
                         Имена полей, по которым выбирается объект для
                          обновления данных в БД пользователя. 
                         Их значения находятся по ключам в данных, 
                         полученных от внешнего сервера.
                         Следует указывать перечислением:
                             \"field1, field2, ..., fieldn\"
                         """,
                    type=is_recitation,
                    default=config["cli_api_params"]["edit_instance_by_fields"])

parser.parse_args()

CMD_PARAMS = dict(parser.parse_args()._get_kwargs())