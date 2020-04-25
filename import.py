import argparse
import datetime
import pandas as pd

def get_data():
  url = f"https://hub.mph.in.gov/dataset/89cfa2e3-3319-4d31-a60d-710f76856588/resource/8b8e6cd7-ede2-4c41-a9bd-4266df783145/download/corona"
  return pd.read_excel(url)[['COUNTY_NAME','COVID_COUNT','COVID_DEATHS','COVID_TEST']]

# def get_data_from_api():
#   import io
#   import urllib
#   url = 'https://hub.mph.in.gov/api/3/action/datastore_search?resource_id=8b8e6cd7-ede2-4c41-a9bd-4266df783145'
#   fileobj = urllib.urlopen(url)
#   print io.read()

def generate_county_table(data):
  totals = data.sum()
  print("==Statistics==")
  print(f"{{| class=\"wikitable sortable\" style=\"text-align:right\"\n|+Coronavirus disease 2019 (COVID-19) cases in Indiana Counties<ref>{{{{Cite web|url=https://hub.mph.in.gov/dataset/89cfa2e3-3319-4d31-a60d-710f76856588/resource/8b8e6cd7-ede2-4c41-a9bd-4266df783145/download/corona|title=ISDH - Novel Coronavirus: Novel Coronavirus (COVID-19)|access-date={datetime.datetime.today().strftime('%Y-%m-%d')}}}}}</ref>\n! County || Confirmed Cases || Deaths")
  for index, row in data.iterrows():
    county_name = row['COUNTY_NAME'].title().replace("Dekalb", "DeKalb").replace("Laporte", "LaPorte").replace("Lagrange", "LaGrange").replace("St Joseph", "St. Joseph")
    print(f"|- \n|style=\"text-align:left;\"|[[{county_name} County, Indiana|{county_name}]]||{row['COVID_COUNT']:,}||{row['COVID_DEATHS']:,}")
  print(f"|- \n! style=\"text-align:right;\" |Total\n! style=\"text-align:right;\" |{totals.COVID_COUNT:,}\n! style=\"text-align:right;\" |{totals.COVID_DEATHS:,}\n|}}")

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--county_table', help='generate county-by-county infection table in wikimedia format', action='store_true')
args = parser.parse_args()

if args.county_table:
  #df = get_data_from_api()
  df = get_data()
  generate_county_table(df)
else:
  df = pd.read_csv('incovid.csv')
  df = df.assign(cases_change=df.cases.pct_change())
  df = df.assign(deaths_change=df.deaths.pct_change())
  df = df.fillna(0)

  for index, row in df.iterrows():
    row['deaths_change'] = f"{row['deaths_change']:.0%}" if row['deaths_change'] else ''
    row['cases_change'] = f"{row['cases_change']:.0%}" if row['cases_change'] else ''
    print(f"{row['date']};{row['deaths']};;{row['cases']};;;{row['cases']};{row['cases_change']};{row['deaths']};{row['deaths_change']}")
