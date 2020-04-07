import argparse
import datetime
import pandas as pd

def get_data():
  url = "https://coronavirus.in.gov/map-test/covid_report_county.csv"
  return pd.read_csv(url)[['county','case_count','death_cases']]


def generate_county_table(data, state):
  totals = data.sum()
  print(f"{{| class=\"wikitable sortable\" style=\"text-align:right\"\n|+Coronavirus disease 2019 (COVID-19) cases in {state}<ref>{{{{Cite web|url=https://coronavirus.in.gov/map-test/covid_report_county.csv|title=ISDH - Novel Coronavirus: Novel Coronavirus (COVID-19)|access-date={datetime.datetime.today().strftime('%Y-%m-%d')}}}}}</ref>\n! County || Confirmed Cases || Deaths")
  for index, row in data.iterrows():
    county_name = row['county'].title()
    print(f"|-\n|style=\"text-align:left;\"|[[{county_name} County, {state}|{county_name}]]||{row['case_count']}||{row['death_cases']}")
  print(f"|-\n! style=\"text-align:right;\" |Total\n! style=\"text-align:right;\" |{totals.case_count}\n! style=\"text-align:right;\" |{totals.death_cases}\n|}}")

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--county_table', help='generate county-by-county infection table in wikimedia format', action='store_true')
args = parser.parse_args()

if args.county_table:
  df = get_data()
  generate_county_table(df, 'Indiana')
else:
  print("THis part needs to be repaired to work with the new data source")
  # dates = pd.date_range(datetime.datetime(2020, 4, 2), datetime.datetime.today() - datetime.timedelta(days=1))

  # for i in dates:
  #   df = get_data_for_date(i).assign(Date = i)
  #   state = df[df.Province_State.eq(args.state)]
  #   frame = frame.append(state, ignore_index=True)

  # frame = frame[frame.Province_State.eq('Indiana')]
  # totals = frame.groupby(['Date'], as_index=False).sum()
  # totals = totals.assign(cases_change=totals.Confirmed.pct_change())
  # totals = totals.assign(deaths_change=totals.Deaths.pct_change())

  # for index, row in totals.iterrows():
  #   print(f"{row['Date'].strftime('%Y-%m-%d')};{row['Deaths']};;{row['Confirmed']};;;{row['Confirmed']};{row['cases_change']:.0%};{row['Deaths']};{row['deaths_change']:.0%}")
