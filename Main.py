from pprint import pprint
import os
import json
import requests
import bs4
from fake_headers import Headers

def get_fake_headers():
    return Headers(browser="chrome", os="win").generate()

# 1.Формируем запрос и собираем ссылки на вакансии
def url_requests(url):
    response = requests.get(f'{url}', headers=get_fake_headers())
    main_page_data = bs4.BeautifulSoup(response.text, features='lxml')
    divs_tags = main_page_data.findAll('div', class_="font-inter")
    links = []
    for div_tag in divs_tags:
        h2_tag = div_tag.find('h2', class_='bloko-header-section-2')
        a_tag = h2_tag.find('a', class_='bloko-link')
        links.append(a_tag['href'])
    return links

# 2.Получаем актуальные ссылки
def keywords(url_request):
    the_right_vacancies = []
    for link in url_request:
        response = requests.get(f'{link}', headers=get_fake_headers())
        main_page_data = bs4.BeautifulSoup(response.text, features='lxml')
        div_tags = main_page_data.findAll('div', class_='magritte-tag___WdGxk_3-0-5 magritte-tag_style-neutral___cw1Bt_3-0-5 magritte-tag_size-medium___Splpy_3-0-5')
        for div_tag in div_tags:
            ddiv_tag = div_tag.find('div', class_='magritte-tag__label___YHV-o_3-0-5')
            for tag in ddiv_tag:
                if tag == 'Django' and link not in the_right_vacancies:
                    the_right_vacancies.append(link)
                elif tag == 'Flask' and link not in the_right_vacancies:
                    the_right_vacancies.append(link)
                else:
                    False
    return the_right_vacancies

# Собираем словарь и записываем файл
def parsed_data(keyword):
    with open('vacancy.json', 'w', encoding="utf8") as outfile:
        parsed_data = []
        translation_table = dict.fromkeys(map(ord, '\xa0'), None)
        for link in keyword:
            response = requests.get(f'{link}', headers=get_fake_headers())
            main_page_data = bs4.BeautifulSoup(response.text, features='lxml')
            div_tags = main_page_data.findAll('div', class_='HH-MainContent HH-Supernova-MainContent')
            for div_tag in div_tags:
                salary = div_tag.find('span', class_='magritte-text___pbpft_3-0-13 magritte-text_style-primary___AQ7MW_3-0-13 magritte-text_typography-label-1-regular___pi3R-_3-0-13').text.translate(translation_table)
                name_company = div_tag.find('span', class_='bloko-header-section-2 bloko-header-section-2_lite').text.translate(translation_table)
                city = div_tag.find('span', class_='magritte-text___tkzIl_4-2-4').text
                parsed_data.append({
                    'link': link,
                    'salary': salary,
                    'name_company': name_company,
                    'city': city
                })
        outfile.write(json.dumps(parsed_data, ensure_ascii=False, indent=4))
    return outfile


def main():
    url_request = url_requests('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2')
    keywords(url_request)
    keyword = keywords(url_request)
    parsed_data(keywords(url_request))

if __name__ == '__main__':
    main()