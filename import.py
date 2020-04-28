import argparse
import datetime
import pandas as pd

def get_county_data():
  url = f"https://hub.mph.in.gov/dataset/89cfa2e3-3319-4d31-a60d-710f76856588/resource/8b8e6cd7-ede2-4c41-a9bd-4266df783145/download/covid_report_county.xlsx"
  return pd.read_excel(url)[['COUNTY_NAME','COVID_COUNT','COVID_DEATHS','COVID_TEST']]

def get_beds_and_vents_data():
  url = f"https://hub.mph.in.gov/dataset/5a905d51-eb50-4a83-8f79-005239bd108b/resource/882a7426-886f-48cc-bbe0-a8d14e3012e4/download/covid_report_bedvent.xlsx"
  return pd.read_excel(url, index_col='STATUS_TYPE')

def get_trend_data():
  url = f"https://hub.mph.in.gov/dataset/ab9d97ab-84e3-4c19-97f8-af045ee51882/resource/182b6742-edac-442d-8eeb-62f96b17773e/download/covid-19_statewidetestcasedeathtrends_428.xlsx"
  return pd.read_excel(url, index_col='DATE')

def generate_county_table(data):
  totals = data.sum()
  print("==Statistics==")
  print(f"{{| class=\"wikitable sortable\" style=\"text-align:right\"\n|+Coronavirus disease 2019 (COVID-19) cases in Indiana Counties<ref>{{{{Cite web|url=https://hub.mph.in.gov/dataset/covid-19-county-statistics|title=ISDH - Novel Coronavirus: Novel Coronavirus (COVID-19)|access-date={datetime.datetime.today().strftime('%Y-%m-%d')}}}}}</ref>\n! County || Confirmed Cases || Deaths")
  for index, row in data.iterrows():
    county_name = row['COUNTY_NAME'].title().replace("Dekalb", "DeKalb").replace("Laporte", "LaPorte").replace("Lagrange", "LaGrange").replace("St Joseph", "St. Joseph")
    print(f"|- \n|style=\"text-align:left;\"|[[{county_name} County, Indiana|{county_name}]]||{row['COVID_COUNT']:,}||{row['COVID_DEATHS']:,}")
  print(f"|- \n! style=\"text-align:right;\" |Total\n! style=\"text-align:right;\" |{totals.COVID_COUNT:,}\n! style=\"text-align:right;\" |{totals.COVID_DEATHS:,}\n|}}")

def generate_infobox(confirmed_cases, all_beds, icu_beds, vents, deaths):
  infobox_template = f"""{{{{Infobox outbreak
| name = 2020 coronavirus pandemic in Indiana
| disease = [[COVID-19]]
| virus_strain = [[SARS-CoV-2]]
| location = [[Indiana]], US
| first_case = [[Indianapolis]]
| arrival_date = March 6, 2020
| confirmed_cases = {confirmed_cases:,}
| hospitalized_cases = {all_beds:,}(current)<ref name=beds-vents>{{{{cite web|url=https://hub.mph.in.gov/dataset/covid-19-beds-and-vents|title=COVID-19 Beds and Vents|publisher=Indiana State Department of Health|access-date={datetime.datetime.today().strftime('%Y-%m-%d')}}}}}</ref>
| critical_cases = {icu_beds:,}<ref name=beds-vents/>
| ventilator_cases = {vents:,}<ref name=beds-vents/>
| deaths = {deaths:,}
| website = {{URL|https://www.in.gov/coronavirus/}}
}}}}
  """
  print(infobox_template)

def generate_template_data(trend):
  list = []
  for index, row in trend.iterrows():
    row['deaths_change'] = f"{row['deaths_change']:.0%}" if row['deaths_change'] else ''
    row['cases_change'] = f"{row['cases_change']:.0%}" if row['cases_change'] else ''
    list.append(f"{index};{row['deaths']:,.0f};;{row['cases']:,.0f};;;{row['cases']:,.0f};{row['cases_change']};{row['deaths']:,.0f};{row['deaths_change']}")

  separator = '\n'

  template = f"""{{{{main|2020 coronavirus pandemic in Indiana}}}}<onlyinclude>
{{{{Medical cases chart
|barwidth=medium

|disease=COVID-19
|location=Indiana|location2=United States
|outbreak=2019–20 coronavirus pandemic

|recoveries=n
|right2=# of deaths
|numwidth=dddd
|data=
{separator.join(list)}
|caption='''Cases:''' The number of cases confirmed in Indiana. <br>
'''Source:''' <ref>{{{{Cite web|url=https://hub.mph.in.gov/dataset/covid-19-case-trend|title=ISDH - Novel Coronavirus|website=ISDH|language=en-US|access-date={datetime.datetime.today().strftime('%Y-%m-%d')}}}}}</ref>
}}}}</onlyinclude>
{{{{template reference list}}}}
{{{{U.S. COVID-19 case charts}}}}
{{{{2019–20 coronavirus pandemic|data|state=expanded}}}}
[[Category:2019–20 coronavirus pandemic in the United States medical cases charts|Indiana]]
[[Category:Indiana templates]]
  """

  print(template)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--county_table', help='generate county-by-county infection table in wikimedia format', action='store_true')
  parser.add_argument('-i', '--info_box', help='generate infobox in wikimedia format', action='store_true')
  args = parser.parse_args()

  if args.county_table:
    trend = get_county_data()
    generate_county_table(trend)
  elif args.info_box:
    beds_and_vents = get_beds_and_vents_data()
    all_beds = beds_and_vents.loc['beds_all_occupied_beds_covid_19', 'TOTAL']
    icu_beds = beds_and_vents.loc['beds_icu_occupied_beds_covid_19', 'TOTAL']
    vents = beds_and_vents.loc['vents_all_in_use_covid_19', 'TOTAL']

    trend = get_trend_data()
    deaths = trend.loc[trend.index[-1], 'COVID_DEATHS_CUMSUM']
    confirmed_cases = trend.loc[trend.index[-1], 'COVID_COUNT_CUMSUM']

    generate_infobox(confirmed_cases, all_beds, icu_beds, vents, deaths)
  else:
    trend = get_trend_data()
    trend = trend.rename(columns={'COVID_COUNT_CUMSUM': 'cases', 'COVID_DEATHS_CUMSUM': 'deaths'})
    trend = trend[['cases', 'deaths']]
    trend = trend.loc['2020-03-06':]
    trend = trend.assign(cases_change=trend.cases.pct_change())
    trend = trend.assign(deaths_change=trend.deaths.pct_change())
    trend = trend.fillna(0)

    generate_template_data(trend)