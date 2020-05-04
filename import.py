import argparse
import datetime
import pandas as pd

def get_county_data():
  url = f"https://hub.mph.in.gov/dataset/89cfa2e3-3319-4d31-a60d-710f76856588/resource/8b8e6cd7-ede2-4c41-a9bd-4266df783145/download/covid_report_county.xlsx"
  isdh_data = pd.read_excel(url)[['COUNTY_NAME','COVID_COUNT','COVID_DEATHS','COVID_TEST']]

  populations=pd.DataFrame([
    ("ADAMS", 35777),
    ("ALLEN", 379299),
    ("BARTHOLOMEW", 83779),
    ("BENTON", 8748),
    ("BLACKFORD", 11758),
    ("BOONE", 67843),
    ("BROWN", 15092),
    ("CARROLL", 20257),
    ("CASS", 37689),
    ("CLARK", 118302),
    ("CLAY", 26225),
    ("CLINTON", 32399),
    ("CRAWFORD", 10577),
    ("DAVIESS", 33351),
    ("DEARBORN", 49458),
    ("DECATUR", 26559),
    ("DEKALB", 43475),
    ("DELAWARE", 114135),
    ("DUBOIS", 42736),
    ("ELKHART", 206341),
    ("FAYETTE", 23102),
    ("FLOYD", 78522),
    ("FOUNTAIN", 16346),
    ("FRANKLIN", 22758),
    ("FULTON", 19974),
    ("GIBSON", 33659),
    ("GRANT", 65769),
    ("GREENE", 31922),
    ("HAMILTON", 338011),
    ("HANCOCK", 78168),
    ("HARRISON", 40515),
    ("HENDRICKS", 170311),
    ("HENRY", 47972),
    ("HOWARD", 82544),
    ("HUNTINGTON", 36520),
    ("JACKSON", 44231),
    ("JASPER", 33562),
    ("JAY", 20436),
    ("JEFFERSON", 32308),
    ("JENNINGS", 27735),
    ("JOHNSON", 158167),
    ("KNOX", 36594),
    ("KOSCIUSKO", 79456),
    ("LAGRANGE", 39614),
    ("LAKE", 485493),
    ("LAPORTE", 109888),
    ("LAWRENCE", 45370),
    ("MADISON", 129569),
    ("MARION", 964582),
    ("MARSHALL", 46258),
    ("MARTIN", 10255),
    ("MIAMI", 35516),
    ("MONROE", 148431),
    ("MONTGOMERY", 38338),
    ("MORGAN", 70489),
    ("NEWTON", 13984),
    ("NOBLE", 47744),
    ("OHIO", 5875),
    ("ORANGE", 19646),
    ("OWEN", 20799),
    ("PARKE", 16937),
    ("PERRY", 19169),
    ("PIKE", 12389),
    ("PORTER", 170389),
    ("POSEY", 25427),
    ("PULASKI", 12353),
    ("PUTNAM", 37576),
    ("RANDOLPH", 24665),
    ("RIPLEY", 28324),
    ("RUSH", 16581),
    ("ST JOSEPH", 271826),
    ("SCOTT", 23873),
    ("SHELBY", 44729),
    ("SPENCER", 20277),
    ("STARKE", 22995),
    ("STEUBEN", 34594),
    ("SULLIVAN", 20669),
    ("SWITZERLAND", 10751),
    ("TIPPECANOE", 195732),
    ("TIPTON", 15148),
    ("UNION", 7054),
    ("VANDERBURGH", 181451),
    ("VERMILLION", 15498),
    ("VIGO", 107038),
    ("WABASH", 30996),
    ("WARREN", 8265),
    ("WARRICK", 62998),
    ("WASHINGTON", 28036),
    ("WAYNE", 65884),
    ("WELLS", 28296),
    ("WHITE", 24102),
    ("WHITLEY", 33964)], columns=['COUNTY_NAME', 'population'])
  populations.set_index('COUNTY_NAME', inplace=True)
  isdh_data.set_index('COUNTY_NAME', inplace=True)
  isdh_data = pd.concat([isdh_data,populations], axis=1)
  return(isdh_data)

def get_beds_and_vents_data():
  url = f"https://hub.mph.in.gov/dataset/5a905d51-eb50-4a83-8f79-005239bd108b/resource/882a7426-886f-48cc-bbe0-a8d14e3012e4/download/covid_report_bedvent.xlsx"
  return(pd.read_excel(url, index_col='STATUS_TYPE'))

def get_trend_data():
  url = f"https://hub.mph.in.gov/dataset/ab9d97ab-84e3-4c19-97f8-af045ee51882/resource/182b6742-edac-442d-8eeb-62f96b17773e/download/covid-19_statewidetestcasedeathtrends_428.xlsx"
  return pd.read_excel(url, index_col='DATE')

def generate_county_table(data):
  totals = data.sum()

  list = []
  for index, row in data.iterrows():
    county_name = index.title().replace("Dekalb", "DeKalb").replace("Laporte", "LaPorte").replace("Lagrange", "LaGrange").replace("St Joseph", "St. Joseph")
    list.append("|-")
    list.append(f"! style=\"padding:0px 2px;\" |[[{county_name} County, Indiana|{county_name}]]")
    list.append(f"| style=\"padding:0px 2px;\" |{row['COVID_COUNT']:,}")
    list.append(f"| style=\"padding:0px 2px;\" |{row['COVID_DEATHS']:,}")
    list.append(f"| style=\"padding:0px 2px;\" |{{{{–}}}}")
    list.append(f"| style=\"padding:0px 2px;\" |{row['population']:,}")
    list.append(f"| style=\"padding:0px 2px;\" |{(row['COVID_COUNT']/(row.population/float(100000))):,.01f}")
    list.append(f"| style=\"padding:0px 2px;\" |")

  separator = '\n'

  table_template = f"""<div class="tp-container" style="float:left;max-width:100%;overflow-y:auto;padding-right:0em;margin: 0 0 0.5em 1em">
{{| class="wikitable plainrowheaders sortable" style="text-align:right; font-size:85%; margin:0"
|+ {{{{Navbar-collapsible|{{{{resize|98%|[[COVID-19 pandemic in Indiana|COVID-19 cases in Indiana]] by [[List of counties in Indiana|county]]}}}}|COVID-19 pandemic data/Indiana medical cases by county}}}}
|-
! style="text-align:right; padding-right:3px;" scope="col" |County{{{{efn|County of residence for individual with a positive test.}}}}
! style="text-align:right; padding-right:3px;" scope="col" |Cases
! style="text-align:right; padding-right:3px;" scope="col" |Deaths
! style="text-align:right; padding-right:3px;" scope="col" |{{{{abbr|Recov.|Recovered cases}}}}{{{{efn|name=na|"–" denotes that no data is currently available for listed county, not that the value is zero. ISDH is not currently providing recovered case numbers.}}}}
! style="text-align:right; padding-right:3px;" scope="col" data-sort-type="number" |Population<ref>{{{{cite web |title=County Population Totals: 2010-2019|url=https://www.census.gov/data/tables/time-series/demo/popest/2010s-counties-total.html|accessdate=2020-05-02}}}}</ref>
! style="text-align:right; padding-right:3px;" scope="col" data-sort-type="number" |{{{{abbr|Cases / 100k|Cases per 100,000 in population}}}}
! style="text-align:right; padding-right:4px;" scope="col" rowspan="2" class="unsortable" |{{{{abbr|Ref.|References & Notes}}}}
|-
! style="text-align:right; padding-right:17px; padding-left:3px;" scope="row" |'''92 / 92'''
! style="text-align:right; padding-right:17px; padding-left:3px;" scope="row" |'''{totals.COVID_COUNT:,}'''
! style="text-align:right; padding-right:17px; padding-left:3px;" scope="row" |'''{totals.COVID_DEATHS:,}'''
! style="text-align:right; padding-right:17px; padding-left:3px;" scope="row" |'''{{{{–}}}}'''
! style="text-align:right; padding-right:17px; padding-left:3px;" scope="row" |'''{totals.population:,}'''
! style="text-align:right; padding-right:17px; padding-left:3px;" scope="row" |'''{(totals.COVID_COUNT/(totals.population/float(100000))):,.01f}'''
{separator.join(list)}
|- style="text-align:center;" class="sortbottom"
| colspan="7" | {{{{resize|Updated {datetime.datetime.today().strftime('%Y-%m-%d')}}}}}<br/>{{{{resize|Data is publicly reported by Indiana State Department of Health}}}}<ref>{{{{cite web |title=Indiana COVID-19 Data Report |url=https://www.coronavirus.in.gov/2393.htm |website=Indiana State Department of Health |accessdate={datetime.datetime.today().strftime('%Y-%m-%d')}}}}}</ref><ref>{{{{cite web |title=COVID-19 County Statistics |url=https://hub.mph.in.gov/dataset/covid-19-county-statistics |website=Indiana State Department of Health |accessdate={datetime.datetime.today().strftime('%Y-%m-%d')}}}}}</ref>
|- style="text-align:center;" class="sortbottom"
| colspan="7" style="width:1px;"| {{{{notelist}}}}
|}}
</div>
<noinclude>
{{{{documentation}}}}

[[Category:COVID-19 pandemic data/United States medical cases by administrative subdivisions|Indiana]]
[[Category:Indiana templates]]
</noinclude>
"""

  print(table_template)

def generate_infobox(confirmed_cases, all_beds, icu_beds, vents, deaths):
  infobox_template = f"""{{{{Infobox outbreak
| name = COVID-19 pandemic in Indiana
| disease = [[COVID-19]]
| virus_strain = [[SARS-CoV-2]]
| location = [[Indiana]], US
| first_case = [[Indianapolis]]
| arrival_date = March 6, 2020
| confirmed_cases = {confirmed_cases:,}
| hospitalized_cases = {all_beds:,} (current)<ref name=beds-vents>{{{{cite web|url=https://hub.mph.in.gov/dataset/covid-19-beds-and-vents|title=COVID-19 Beds and Vents|publisher=Indiana State Department of Health|access-date={datetime.datetime.today().strftime('%Y-%m-%d')}}}}}</ref>
| critical_cases = {icu_beds:,}<ref name=beds-vents/>
| ventilator_cases = {vents:,}<ref name=beds-vents/>
| deaths = {deaths:,}
| map1 = COVID-19 Prevalence in Indiana by county.svg
| legend1 = {{{{COVID-19 pandemic in the United States prevalence legend|state=Indiana}}}}
| website = {{{{URL|https://www.in.gov/coronavirus/}}}}<br>{{{{URL|https://backontrack.in.gov/}}}}
}}}}"""

  print(infobox_template)

def generate_template_data(trend):
  list = []
  for index, row in trend.iterrows():
    row['deaths_change'] = f"{row['deaths_change']:.0%}" if row['deaths_change'] else ''
    row['cases_change'] = f"{row['cases_change']:.0%}" if row['cases_change'] else ''
    list.append(f"{index};{row['deaths']:,.0f};;{row['cases']:,.0f};;;{row['cases']:,.0f};{row['cases_change']};{row['deaths']:,.0f};{row['deaths_change']}")

  separator = '\n'

  template = f"""{{{{main|COVID-19 pandemic in Indiana}}}}<onlyinclude>
{{{{Medical cases chart
|barwidth=medium

|disease=COVID-19
|location=Indiana|location2=United States
|outbreak=COVID-19 pandemic

|recoveries=n
|right2=# of deaths
|numwidth=dddd

|togglesbar=
<div class="nomobile" style="text-align:center">
{{{{Medical cases chart/Month toggle button|mar}}}}
{{{{Medical cases chart/Month toggle button|apr}}}}
{{{{Medical cases chart/Month toggle button|may}}}}
{{{{Medical cases chart/Month toggle button|l15}}}}
</div>

|collapsible=y

|data=
{separator.join(list)}
|caption='''Cases:''' The number of cases confirmed in Indiana. <br>
'''Source:''' <ref>{{{{Cite web|url=https://hub.mph.in.gov/dataset/covid-19-case-trend|title=ISDH - Novel Coronavirus|website=ISDH|language=en-US|access-date={datetime.datetime.today().strftime('%Y-%m-%d')}}}}}</ref>
}}}}</onlyinclude>
{{{{template reference list}}}}
{{{{U.S. COVID-19 case charts}}}}
{{{{COVID-19 pandemic|data|state=expanded}}}}
[[Category:COVID-19 pandemic in the United States medical cases charts|Indiana]]
[[Category:Indiana templates]]"""

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