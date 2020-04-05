import pandas as pandas
import datetime

def get_data_for_date(targetDate):
  # url = "https://github.com/CSSEGISandData/COVID-19/raw/web-data/data/cases.csv"
  url = f"https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_daily_reports/{targetDate}.csv"
  return pandas.read_csv(url)[['Province_State', 'Admin2', 'Confirmed', 'Deaths']].rename(columns={"Admin2": "County"})


def county_table(df, targetDate, state):
  data = df[df.Province_State.eq(state)]
  totals = data.sum()
  print(f"{{| class=\"wikitable sortable\" style=\"text-align:right\"\n|+Coronavirus disease 2019 (COVID-19) cases in {state}<ref>{{{{Cite web|url=https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_daily_reports/{targetDate}.csv|title=2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE|access-date={datetime.datetime.today().strftime('%Y-%m-%d')}}}}}</ref>\n! County || Confirmed Cases || Deaths")
  for index, row in data.iterrows():
    print(f"|-\n|style=\"text-align:left;\"|[[{row['County']} County, {state}|{row['County']}]]||{row['Confirmed']}||{row['Deaths']}")
  print(f"|-\n! style=\"text-align:right;\" |Total\n! style=\"text-align:right;\" |{totals.Confirmed}\n! style=\"text-align:right;\" |{totals.Deaths}\n|}}")

date = "04-04-2020"
df = get_data_for_date(date)
totals = df.sum()
# print(date, totals.Confirmed, totals.Deaths)
county_table(df, date, 'Indiana')

# for i in range(1, 4):
#   date = f"04-{i:02d}-2020"
#   df = get_data_for_date(date, 'Indiana')
#   print(date, df.sum().Confirmed, df.sum().Deaths)