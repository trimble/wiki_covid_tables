import datetime
import pandas as pd

def get_todays_beds_and_vents_data():
  url = f"https://hub.mph.in.gov/dataset/5a905d51-eb50-4a83-8f79-005239bd108b/resource/882a7426-886f-48cc-bbe0-a8d14e3012e4/download/covid_report_bedvent.xlsx"
  return pd.read_excel(url, index_col='STATUS_TYPE')

if __name__ == "__main__":
  file = f"covid_report_bedvent_compiled.csv"
  new_data = get_todays_beds_and_vents_data()
  new_row = new_data['TOTAL']
  old_data = pd.read_csv(file)
  old_data[f"{datetime.date.today()}"] = old_data['STATUS_TYPE'].map(new_row)
  old_data.set_index('STATUS_TYPE', inplace=True)
  print(old_data)
  old_data.to_csv(file)