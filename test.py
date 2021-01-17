from bs4 import BeautifulSoup
import requests
import csv

r = requests.get("https://covid19.ncdc.gov.ng/report/")
c = r.content

soup = BeautifulSoup(c, 'html.parser')
# soup.prettify

# all = soup.find_all("div", {"class" : "table-responsive"})
# print(all)

data = {}

tab_star = soup.find("table", attrs={"id": "custom1"})
tab_star_data = tab_star.tbody.find_all("tr")

#print(tab_star_data)


headings = []

for td in tab_star_data[0].find_all("td"):
    headings.append(td.text.replace('\n', ' ').strip())

for table, heading in zip(tab_star_data[1].find_all("table"), headings):
    t_header = []
    for th in table.find_all("th"):
        t_header.append(th.text.replace('\n', ' ').strip())

    table_data = []

    for tr in table.tbody.find_all("tr"):
        t_row = {}

        for td, th in zip(tr.find_all('td'), t_header):
            t_row[th] = td.text.replace('\n', ' ').strip()
        table_data.append(t_row)

    data[heading] = table_data

for topic, table in data.items():
    with open(f"{topic}.csv", 'w') as out_file:
        headers = ['States_Affected',
                   'No. of Cases (Lab Confirmed)',
                   'No. of Cases (on admission)',
                   'No. Discharged',
                   'No of Deaths'
                   ]

        writer = csv.DictWriter(out_file, headers)
        writer.writeheader()
        for row in table:
            if row:
                writer.writerow(row)
