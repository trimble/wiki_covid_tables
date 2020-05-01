import datetime
import pandas as pd

def get_todays_beds_and_vents_data():
  url = f"https://hub.mph.in.gov/dataset/5a905d51-eb50-4a83-8f79-005239bd108b/resource/882a7426-886f-48cc-bbe0-a8d14e3012e4/download/covid_report_bedvent.xlsx"
  new_data = pd.read_excel(url, index_col='STATUS_TYPE')
  new_row = new_data['TOTAL']
  row_df = pd.DataFrame([new_row]).rename(index={'TOTAL':datetime.datetime.today().strftime('%Y-%m-%d')})
  row_df.index = pd.to_datetime(row_df.index)
  return row_df

if __name__ == "__main__":
  file = f"covid_report_bedvent_compiled.csv"
  new_data = get_todays_beds_and_vents_data()
  old_data = pd.read_csv(file, index_col=0)
  old_data.index = pd.to_datetime(old_data.index)
  old_data = old_data.append(new_data)
  index = old_data.index
  is_duplicate = index.duplicated(keep="last")
  not_duplicate = ~is_duplicate
  old_data = old_data[not_duplicate]
  print(old_data)
  old_data.to_csv(file)