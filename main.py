import requests
from bs4 import BeautifulSoup
import csv
CSV = 'cards.csv'

headers = {
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
url = 'https://malvina-club.ru/hours/'
def girl_pars():
    session = requests.Session()
    request = session.get(url, headers=headers)
    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'lxml')
        hours_table = soup.find_all('tr', class_='hours')
        cards = []
        for girl in hours_table:
            hours = [x['data-hours'] for x in girl.find_all("td", {'data-rest': 'false'})]
            date = [x['data-date'] for x in girl.find_all("td", {'data-rest': 'false'})]
            work_time = dict(zip(date, hours))
            cards.append({
                'name': girl.span.text,
                'work_time': work_time,
                'foto': girl.a['href']
            })
            save_doc(cards, CSV)


def save_doc(hours_table, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Имя', 'График работы', 'фото'])
        for girl in hours_table:
            writer.writerow([girl['name'], girl['work_time'], girl['foto']])


girl_pars()