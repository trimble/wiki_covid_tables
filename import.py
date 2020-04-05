import argparse
import datetime
import pandas as pd

def get_data_for_date(targetDate):
  # url = "https://github.com/CSSEGISandData/COVID-19/raw/web-data/data/cases.csv"
  url = f"https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_daily_reports/{targetDate.strftime('%m-%d-%Y')}.csv"
  return pd.read_csv(url)[['Province_State', 'Admin2', 'Confirmed', 'Deaths']].rename(columns={"Admin2": "County"})


def generate_county_table(df, targetDate, state):
  data = df[df.Province_State.eq(state)]
  totals = data.sum()
  print(f"{{| class=\"wikitable sortable\" style=\"text-align:right\"\n|+Coronavirus disease 2019 (COVID-19) cases in {state}<ref>{{{{Cite web|url=https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_daily_reports/{targetDate}.csv|title=2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE|access-date={datetime.datetime.today().strftime('%Y-%m-%d')}}}}}</ref>\n! County || Confirmed Cases || Deaths")
  for index, row in data.iterrows():
    print(f"|-\n|style=\"text-align:left;\"|[[{row['County']} County, {state}|{row['County']}]]||{row['Confirmed']}||{row['Deaths']}")
  print(f"|-\n! style=\"text-align:right;\" |Total\n! style=\"text-align:right;\" |{totals.Confirmed}\n! style=\"text-align:right;\" |{totals.Deaths}\n|}}")

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--county_table', help='generate county-by-county infection table in wikimedia format', action='store_true')
parser.add_argument('state', help='US state for which to present data')
parser.add_argument('date', help='date for which to present data')
args = parser.parse_args()

if args.county_table:
  date = datetime.datetime.strptime(args.date, "%Y-%m-%d")
  df = get_data_for_date(date)
  generate_county_table(df, date, args.state)
else:
  frame = pd.DataFrame(data={'Date':[datetime.datetime(2020, 4, 1)],'Province_State':[args.state],'Confirmed':[3029],'Deaths':[113]})
  # Note: Older files  in Johns Hopkins data have weird data field name changes. So, just start here and move forward.
  dates = pd.date_range(datetime.datetime(2020, 4, 2), datetime.datetime.today() - datetime.timedelta(days=1))

  for i in dates:
    df = get_data_for_date(i).assign(Date = i)
    state = df[df.Province_State.eq(args.state)]
    frame = frame.append(state, ignore_index=True)

  frame = frame[frame.Province_State.eq('Indiana')]
  totals = frame.groupby(['Date'], as_index=False).sum()
  totals = totals.assign(cases_change=totals.Confirmed.pct_change())
  totals = totals.assign(deaths_change=totals.Deaths.pct_change())

  for index, row in totals.iterrows():
    print(f"{row['Date'].strftime('%Y-%m-%d')};{row['Deaths']};;{row['Confirmed']};;;{row['Confirmed']};{row['cases_change']:.0%};{row['Deaths']};{row['deaths_change']:.0%}")
