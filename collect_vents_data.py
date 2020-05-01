import argparse
import datetime
import matplotlib.pyplot as plt
import pandas as pd

def get_todays_beds_and_vents_data():
  url = f"https://hub.mph.in.gov/dataset/5a905d51-eb50-4a83-8f79-005239bd108b/resource/882a7426-886f-48cc-bbe0-a8d14e3012e4/download/covid_report_bedvent.xlsx"
  new_data = pd.read_excel(url, index_col='STATUS_TYPE')
  new_row = new_data['TOTAL']
  row_df = pd.DataFrame([new_row]).rename(index={'TOTAL':datetime.datetime.today().strftime('%Y-%m-%d')})
  row_df.index = pd.to_datetime(row_df.index)
  return row_df

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-w', '--write-file', help="append today's data to the file", action='store_true')
  parser.add_argument('-g', '--generate-graphs', help='generate graphs', action='store_true')
  args = parser.parse_args()

  file = f"covid_report_bedvent_compiled.csv"
  new_data = get_todays_beds_and_vents_data()
  old_data = pd.read_csv(file, index_col=0)
  old_data.index = pd.to_datetime(old_data.index)

  data = old_data.append(new_data)
  data = data[~data.index.duplicated(keep='last')]
  print(data)

  if args.write_file:
    print(f"updating {file}...")
    data.to_csv(file)

  if args.generate_graphs:
    icu_data = data[['beds_icu_occupied_beds_covid_19', 'bed_occupied_icu_non_covid', 'beds_available_icu_beds_total']]
    icu_data = icu_data.rename(columns={
      'beds_icu_occupied_beds_covid_19': 'COVID-19',
      'bed_occupied_icu_non_covid': 'Non-COVID-19',
      'beds_available_icu_beds_total': 'Available'
      })
    icu_plot = icu_data.plot.area(title='ICU Bed Availability in Indiana')
    plt.legend(loc='upper left', bbox_to_anchor=(0, 1.0))
    icu_plot.set_xlabel('Date')
    icu_plot.set_ylabel('#')

    vent_data = data[['vents_all_in_use_covid_19', 'vents_non_covid_pts_on_vents', 'vents_all_available_vents_not_in_use']]
    vent_data = vent_data.rename(columns={
      'vents_all_in_use_covid_19': 'COVID-19',
      'vents_non_covid_pts_on_vents': 'Non-COVID-19',
      'vents_all_available_vents_not_in_use': 'Available'
      })
    vent_plot = vent_data.plot.area(title='Ventilator Availability in Indiana')
    vent_plot.legend(bbox_to_anchor=(1,1))
    vent_plot.set_xlabel('Date')
    vent_plot.set_ylabel('#')
    plt.legend(loc='upper left', bbox_to_anchor=(0, 1.0))

    plt.show()