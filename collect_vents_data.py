# import argparse
import datetime
import pandas as pd

def get_todays_beds_and_vents_data():
  url = f"https://hub.mph.in.gov/dataset/5a905d51-eb50-4a83-8f79-005239bd108b/resource/882a7426-886f-48cc-bbe0-a8d14e3012e4/download/covid_report_bedvent.xlsx"
  return pd.read_excel(url)

def get_compiled_data():
  file = f"covid_report_bedvent_compiled.xlsx"
  return pd.read_excel(file, index_col='date')

if __name__ == "__main__":
  # parser = argparse.ArgumentParser()
  # parser.add_argument('-c', '--county_table', help='generate county-by-county infection table in wikimedia format', action='store_true')
  # args = parser.parse_args()

  new_data = get_todays_beds_and_vents_data().rename(columns={'TOTAL':f"{datetime.date.today()}", 'STATUS_TYPE':'date'}).set_index('date').transpose()
  old_data = get_compiled_data()
  data = pd.concat([old_data,new_data])
  print(data)
  data.to_excel('covid_report_bedvent_compiledxxx.xlsx')
