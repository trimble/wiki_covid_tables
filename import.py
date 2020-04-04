import pandas as pandas
import datetime

def get_data_for_date(targetDate, state):
  # url = "https://github.com/CSSEGISandData/COVID-19/raw/web-data/data/cases.csv"
  url = f"https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_daily_reports/{targetDate}.csv"
  df = pandas.read_csv(url)[['Province_State', 'Admin2', 'Confirmed', 'Deaths']].rename(columns={"Admin2": "County"})
  return df[df.Province_State.eq(state)]

def template_table(df, targetDate):
  data = df
  totals = data.sum()
  print(f"{{| class=\"wikitable sortable\" style=\"text-align:right\"\n|+Coronavirus disease 2019 (COVID-19) cases in Indiana<ref>{{{{Cite web|url=https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_daily_reports/{targetDate}.csv|title=2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE|access-date={datetime.datetime.today().strftime('%Y-%m-%d')}}}}}</ref>\n! County || Confirmed Cases || Deaths")
  for index, row in df.iterrows():
    print(f"|-\n|style=\"text-align:left;\"|[[{row['County']} County, Indiana|{row['County']}]]||{row['Confirmed']}||{row['Deaths']}")
  print(f"|-\n! style=\"text-align:right;\" |Total\n! style=\"text-align:right;\" |{totals.Confirmed}\n! style=\"text-align:right;\" |{totals.Deaths}\n|}}")

df = get_data_for_date('04-02-2020', 'Indiana')
template_table(df,  '04-02-2020')
