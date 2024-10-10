import os
import json
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

skills = [
    # Hard Skills
    "Golang", "TDD", "REST", "gRPC",
    "JSON", "GORM", "Docker",
    "Gin", "Echo", "Redis", "GoKit",
    "CI/CD", "JWT", "RabbitMQ", "Git",
    "Swagger", "CLI", "WebSockets",
    "OAuth2", "GoLand", "GoVet",
    # Soft skills
    "Коммуникация", "Командная работа", "Английский", "Адаптивность"
]

content_text = ' '.join(skills)

def clear_text(text):
    # Очищаем текст от всех символов, кроме букв и цифр
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    # Разделяем текст на слова
    words = cleaned_text.split()
    return words


# Функция определения близости текстов
def compare_texts(content_text, job_description):
    text_list = [content_text, job_description]
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text_list)
    match_percentage = cosine_similarity(count_matrix)[0][1] * 100
    match_percentage = round(match_percentage, 2)
    return match_percentage


def similarity():

    # Проход по всем файлам в папке vacancies
    cnt_docs = len(os.listdir('./vacancies'))
    percentage = []
    i = 0

    # Список для хранения данных о вакансиях
    vacancy_data = []

    for fl in os.listdir('./vacancies'):
        # Открываем, читаем и закрываем файл
        with open('./vacancies/{}'.format(fl), encoding='utf8') as vac_file:
            json_text = vac_file.read()

        # Текст файла переводим в справочник
        json_obj = json.loads(json_text)

        # Получаем ID, название и описание вакансии
        ID = json_obj['id']
        vacancy_name = json_obj['name']  # Получаем название вакансии
        job_description = json_obj['description']

        # С помощью регулярных выражений очищаем от html-тегов
        job_description = re.sub(r"<[^>]+>", "", job_description, flags=re.S)

        # И очищаем текст ранее созданной функцией clear_text
        words = clear_text(job_description)

        job_description = " ".join(words)
        # Увеличиваем счетчик обработанных файлов на 1
        i += 1

        # Вызов функции определения близости текстов
        match_percentage = compare_texts(content_text, job_description)

        # Добавляем данные о вакансии в список
        vacancy_data.append({
            "Vacancy ID": ID,
            "Vacancy Name": vacancy_name,
            "Match Percentage": match_percentage
        })

        # Вывод результата, включая название вакансии
        print(
            'Вакансия "{}" (ID: {}). ({} из {}). Близость: {} %.'.format(vacancy_name, ID, i, cnt_docs,
                                                                                              str(match_percentage)))

    return vacancy_data

def assign_group(vacancy_data):

    for vacancy in vacancy_data:
        vacancy_name = vacancy["Vacancy Name"].lower()  # Приводим к нижнему регистру для удобства
        match vacancy_name:
            case vacancy_name if "qa" in vacancy_name:
                vacancy["Group"] = "QA"
            case vacancy_name if "devops" in vacancy_name:
                vacancy["Group"] = "DevOps"
            case vacancy_name if "frontend" in vacancy_name:
                vacancy["Group"] = "Frontend"
            case vacancy_name if "python" in vacancy_name:
                vacancy["Group"] = "Python"
            case vacancy_name if "backend" in vacancy_name:
                vacancy["Group"] = "Backend"
            case vacancy_name if "java" in vacancy_name:
                vacancy["Group"] = "Java"
            case vacancy_name if "c#" in vacancy_name:
                vacancy["Group"] = "C#"
            case vacancy_name if "golang" in vacancy_name or "go" in vacancy_name:
                vacancy["Group"] = "Golang"
            case _:
                vacancy["Group"] = "Другие"

    return vacancy_data


def save_to_excel(grouped_vacancies):
    # Преобразуем данные в DataFrame для экспорта в Excel
    df = pd.DataFrame(grouped_vacancies)

    # Сохраняем результат в Excel
    df.to_excel("vacancies_similarity.xlsx", index=False)

    print("Данные успешно сохранены в файл 'vacancies_similarity.xlsx'.")


def main():
    vacancies_sim = similarity()
    grouped_vacancies = assign_group(vacancies_sim)
    save_to_excel(grouped_vacancies)


if __name__ == '__main__':
    main()