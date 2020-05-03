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

  list = []
  for index, row in data.iterrows():
    county_name = row['COUNTY_NAME'].title().replace("Dekalb", "DeKalb").replace("Laporte", "LaPorte").replace("Lagrange", "LaGrange").replace("St Joseph", "St. Joseph")
    list.append("|-")
    list.append(f"! style=\"padding:0px 2px;\" |[[{county_name} County, Indiana|{county_name}]]")
    # print(f"|- \n|style=\"text-align:left;\"|[[{county_name} County, Indiana|{county_name}]]||{row['COVID_COUNT']:,}||{row['COVID_DEATHS']:,}")
    list.append(f"| style=\"padding:0px 2px;\" |{row['COVID_COUNT']:,}")
    list.append(f"| style=\"padding:0px 2px;\" |{row['COVID_DEATHS']:,}")
    list.append(f"| style=\"padding:0px 2px;\" |{{{{–}}}}")
    list.append(f"| style=\"padding:0px 2px;\" |{row['population']:,}")
    list.append(f"| style=\"padding:0px 2px;\" |{(row['COVID_COUNT']/(row.population/float(100000))):,.01f}")
    list.append(f"| style=\"padding:0px 2px;\" |")

  separator = '\n'


  table_template = f"""<div class="tp-container" style="float:left;max-width:100%;overflow-y:auto;padding-right:0em;margin: 0 0 0.5em 1em">
{{| class="wikitable plainrowheaders sortable" style="text-align:right; font-size:85%; margin:0"
|+ {{{{Navbar-collapsible|{{{{resize|98%|[[2020 coronavirus pandemic in Indiana|COVID-19 cases in Indiana]] by [[List of counties in Indiana|county]]}}}}|2020 coronavirus pandemic data/Indiana medical cases by county}}}}
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

[[Category:2020 coronavirus pandemic data/United States medical cases by administrative subdivisions|Indiana]]
[[Category:Indiana templates]]
</noinclude>
"""

  print(table_template)

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
| map1 = COVID-19 Prevalence in Indiana by county.svg
| legend1 = {{2020 coronavirus pandemic in the United States prevalence legend|state=Indiana}}
| website = {{{{URL|https://www.in.gov/coronavirus/}}}}
}}}}"""

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

|togglesbar=
<div class="nomobile" style="text-align:center">
{{{{Medical cases chart/Month toggle button|jan}}}}
{{{{Medical cases chart/Month toggle button|feb}}}}
{{{{Medical cases chart/Month toggle button|mar}}}}
{{{{Medical cases chart/Month toggle button|apr}}}}
{{{{Medical cases chart/Month toggle button|may}}}}
<span class="mw-collapsible mw-customtoggle-l15 mw-customtoggle-mar-l15 mw-customtoggle-apr-l15 mw-customtoggle-may-l15 mw-collapsed" id="mw-customcollapsible-l15" style="padding:0 8px">Last 15 days</span>
<span class="mw-collapsible mw-customtoggle-l15 mw-customtoggle-mar-l15 mw-customtoggle-apr-l15 mw-customtoggle-may-l15" id="mw-customcollapsible-l15" style="border:2px solid lightblue; padding:0 8px">Last 15 days</span>
</div>

|collapsible=y

|data=
{separator.join(list)}
|caption='''Cases:''' The number of cases confirmed in Indiana. <br>
'''Source:''' <ref>{{{{Cite web|url=https://hub.mph.in.gov/dataset/covid-19-case-trend|title=ISDH - Novel Coronavirus|website=ISDH|language=en-US|access-date={datetime.datetime.today().strftime('%Y-%m-%d')}}}}}</ref>
}}}}</onlyinclude>
{{{{template reference list}}}}
{{{{U.S. COVID-19 case charts}}}}
{{{{2019–20 coronavirus pandemic|data|state=expanded}}}}
[[Category:2019–20 coronavirus pandemic in the United States medical cases charts|Indiana]]
[[Category:Indiana templates]]"""

  print(template)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--county_table', help='generate county-by-county infection table in wikimedia format', action='store_true')
  parser.add_argument('-i', '--info_box', help='generate infobox in wikimedia format', action='store_true')
  args = parser.parse_args()

  if args.county_table:
    trend = get_county_data()
    trend = trend.assign(population=[35777,
      379299,
      83779,
      8748,
      11758,
      67843,
      15092,
      20257,
      37689,
      118302,
      26225,
      32399,
      10577,
      33351,
      49458,
      26559,
      43475,
      114135,
      42736,
      206341,
      23102,
      78522,
      16346,
      22758,
      19974,
      33659,
      65769,
      31922,
      338011,
      78168,
      40515,
      170311,
      47972,
      82544,
      36520,
      44231,
      33562,
      20436,
      32308,
      27735,
      158167,
      36594,
      79456,
      39614,
      485493,
      109888,
      45370,
      129569,
      964582,
      46258,
      10255,
      35516,
      148431,
      38338,
      70489,
      13984,
      47744,
      5875,
      19646,
      20799,
      16937,
      19169,
      12389,
      170389,
      25427,
      12353,
      37576,
      24665,
      28324,
      16581,
      271826,
      23873,
      44729,
      20277,
      22995,
      34594,
      20669,
      10751,
      195732,
      15148,
      7054,
      181451,
      15498,
      107038,
      30996,
      8265,
      62998,
      28036,
      65884,
      28296,
      24102,
      33964])
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