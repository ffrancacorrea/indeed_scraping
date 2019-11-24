#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests

def count(salaries):
    print('returning mean of salaries')
    list_sal = []
    for i in salaries:
        for j in i:
            list_sal.append(j[0:6])

    salaries = [float(x.replace(u'\xa0', u'')) for x in list_sal]
    print(salaries)
    result = sum(salaries)/len(salaries)
    return result

def get_job_title(soup):
    titles = []
    for div in soup.find_all(name='div', attrs={'class': 'title'}):
        for a in div.find_all(name='a', attrs={'data-tn-element': 'jobTitle'}):
            titles.append(a['title'])
    return titles

def get_salary(soup):
    salaries = []
    for span in soup.find_all(name="span", attrs={'class': "salaryText"}):
        try:
            salary = span.text.strip()
            salaries.append(salary)
        except:
            salaries.append(None)
    #case_to_ignore = [u'heure', u'jour', u'mois']
    temp_sal_list = []
    for salary in salaries:
        if ('an' in salary):  # any(x not in salary for x in case_to_ignore)
            temp_sal_list.append(salary)

    return temp_sal_list

pages = []
for page in range(10, 50, 10):
    pages.append(page)

urls = []
for page in pages:
    url = 'https://www.indeed.fr/jobs?q=data+engineer&l=Paris&start={}'.format(
        page)
    urls.append(url)
# get data from site using requests
salaries = []
for url in urls:
    data_source = requests.get(url).text
# make it readable
    soup = BeautifulSoup(data_source, 'html.parser')  # .prettify()
    jobs = soup.find(class_='result')
    salary = get_salary(soup)
    salaries.append(salary)
    count(salaries)
