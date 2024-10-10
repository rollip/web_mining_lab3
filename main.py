# Библиотека для работы с HTTP-запросами. Используем для обращения к API hh.ru
import requests
# Модуль для работы с данными в формате json
import json
# Модуль для работы со значением времени
import time
# Модуль для работы с операционной системой. Используем для работы с файлами
import os



def getPage(page = 0):
    """
    Создаем метод для получения страницы со списком вакансий.
    Аргументы:
    page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
    """
    # Справочник для параметров GET-запроса
    params = {
        'text': '"golang" OR "GORM" OR "Docker" OR "Redis" OR "Kafka" OR "Git"' ,  # Текст фильтра. Отбираем вакансии по слову "golang"
        'search_field': ['description'],
        'area': 1,  # Поиск осуществляется по вакансиям в г. Москве
        'page': page,  # Индекс страницы поиска на hh.ru
        'per_page': 100  # Кол-во вакансий на 1 странице
    }
    req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
    data = req.content.decode()  # Декодируем ответ, чтобы кириллица отображалась корректно
    req.close()
    return data

# Если отсутствует, то создаем папку pagination в папке с проектом для сохранения страниц поиска.
if not os.path.isdir("pagination"):
    os.mkdir("pagination")

# Если отсутствует, то создаем папку vacancies в папке с проектом для сохранения вакансий.
if not os.path.isdir("vacancies"):
    os.mkdir("vacancies")

# Считываем первые 100 вакансий. Для считывания 2000 вакансий увеличить границу до 20.
for page in range(0, 10):
    # Преобразуем текст ответа запроса в справочник
    jsObj = json.loads(getPage(page))
    # Сохраняем файлы в папку pagination
    nextFileName = './pagination/{}.json'.format(len(os.listdir('./pagination')))
    # Создаем новый документ, записываем в него ответ запроса, после закрываем
    f = open(nextFileName, 'w', encoding = 'utf-8')
    f.write(json.dumps(jsObj, ensure_ascii = False))
    f.close()
    # Проверка на последнюю страницу, если вакансий меньше 2000
    if (jsObj['pages'] - page) <= 1:
        break
    # Задержка, чтобы не нагружать сервисы hh.ru
    time.sleep(0.25)

print('Страницы поиска собраны. Далее получаем список вакансий...')

# Получаем перечень ранее созданных файлов со списком вакансий и проходимся по нему в цикле
for fl in os.listdir('./pagination'):
    # Открываем файл, читаем его содержимое, закрываем файл
    f = open('./pagination/{}'.format(fl), encoding = 'utf-8')
    jsonText = f.read()
    f.close()
    # Преобразуем полученный текст в объект справочника
    jsonObj = json.loads(jsonText)
    # Получаем и проходимся по непосредственно списку вакансий
    for v in jsonObj['items']:
        # Обращаемся к API и получаем детальную информацию по конкретной вакансии
        req = requests.get(v['url'])
        data = req.content.decode()
        req.close()
        # Создаем файл в формате json с идентификатором вакансии в качестве названия
        fileName = './vacancies/{}.json'.format(v['id'])
        f = open(fileName, 'w', encoding = 'utf-8')
        f.write(data)
        f.close()
        time.sleep(0.25)

print('Вакансии собраны')


