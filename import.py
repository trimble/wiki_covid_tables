import pandas as pandas
import datetime

url = "https://github.com/CSSEGISandData/COVID-19/raw/web-data/data/cases.csv"

data = pandas.read_csv(url)[['Province_State', 'Admin2', 'Confirmed', 'Deaths']]

indiana = data[data.Province_State.eq('Indiana')]
totals = indiana.sum()

print(f"{{| class=\"wikitable sortable\" style=\"text-align:right\"\n|+Coronavirus disease 2019 (COVID-19) cases in Indiana<ref>{{{{Cite web|url={url}|title=2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE|access-date={datetime.datetime.today().strftime('%Y-%m-%d')}}}}}</ref>\n! County || Confirmed Cases || Deaths")
for index, row in indiana.iterrows():
  print(f"|-\n|style=\"text-align:left;\"|[[{row['Admin2']} County, Indiana|{row['Admin2']}]]||{row['Confirmed']}||{row['Deaths']}")
print(f"|-\n! style=\"text-align:right;\" |Total\n! style=\"text-align:right;\" |{totals.Confirmed}\n! style=\"text-align:right;\" |{totals.Deaths}\n|}}")