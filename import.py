import argparse
import datetime
import pandas as pd

def get_data():
  url = "https://coronavirus.in.gov/map-test/covid_report_county.csv"
  return pd.read_csv(url)[['COUNTY_NAME','COVID_COUNT','COVID_DEATHS']]


def generate_county_table(data, state):
  totals = data.sum()
  print(f"{{| class=\"wikitable sortable\" style=\"text-align:right\"\n|+Coronavirus disease 2019 (COVID-19) cases in {state}<ref>{{{{Cite web|url=https://coronavirus.in.gov/map-test/covid_report_county.csv|title=ISDH - Novel Coronavirus: Novel Coronavirus (COVID-19)|access-date={datetime.datetime.today().strftime('%Y-%m-%d')}}}}}</ref>\n! County || Confirmed Cases || Deaths")
  for index, row in data.iterrows():
    county_name = row['COUNTY_NAME'].title().replace("Dekalb", "DeKalb").replace("Laporte", "LaPorte").replace("Lagrange", "LaGrange")
    print(f"|-\n|style=\"text-align:left;\"|[[{county_name} County, {state}|{county_name}]]||{row['COVID_COUNT']}||{row['COVID_DEATHS']}")
  print(f"|-\n! style=\"text-align:right;\" |Total\n! style=\"text-align:right;\" |{totals.COVID_COUNT}\n! style=\"text-align:right;\" |{totals.COVID_DEATHS}\n|}}")

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--county_table', help='generate county-by-county infection table in wikimedia format', action='store_true')
args = parser.parse_args()

if args.county_table:
  df = get_data()
  generate_county_table(df, 'Indiana')
else:
  df = pd.read_csv('incovid.csv')
  df = df.assign(cases_change=df.cases.pct_change())
  df = df.assign(deaths_change=df.deaths.pct_change())
  df = df.fillna(0)

  for index, row in df.iterrows():
    row['deaths_change'] = f"{row['deaths_change']:.0%}" if row['deaths_change'] else ''
    row['cases_change'] = f"{row['cases_change']:.0%}" if row['cases_change'] else ''
    print(f"{row['date']};{row['deaths']};;{row['cases']};;;{row['cases']};{row['cases_change']};{row['deaths']};{row['deaths_change']}")
