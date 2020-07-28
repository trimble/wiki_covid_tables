import argparse
import datetime
import pandas as pd

def get_county_data():
  url = f"https://hub.mph.in.gov/dataset/89cfa2e3-3319-4d31-a60d-710f76856588/resource/8b8e6cd7-ede2-4c41-a9bd-4266df783145/download/covid_report_county.xlsx"
  isdh_data = pd.read_excel(url)[['COUNTY_NAME','COVID_COUNT','COVID_DEATHS']]

  populations=pd.DataFrame([
    ("Adams", 35777),
    ("Allen", 379299),
    ("Bartholomew", 83779),
    ("Benton", 8748),
    ("Blackford", 11758),
    ("Boone", 67843),
    ("Brown", 15092),
    ("Carroll", 20257),
    ("Cass", 37689),
    ("Clark", 118302),
    ("Clay", 26225),
    ("Clinton", 32399),
    ("Crawford", 10577),
    ("Daviess", 33351),
    ("Dearborn", 49458),
    ("Decatur", 26559),
    ("De Kalb", 43475),
    ("Delaware", 114135),
    ("Dubois", 42736),
    ("Elkhart", 206341),
    ("Fayette", 23102),
    ("Floyd", 78522),
    ("Fountain", 16346),
    ("Franklin", 22758),
    ("Fulton", 19974),
    ("Gibson", 33659),
    ("Grant", 65769),
    ("Greene", 31922),
    ("Hamilton", 338011),
    ("Hancock", 78168),
    ("Harrison", 40515),
    ("Hendricks", 170311),
    ("Henry", 47972),
    ("Howard", 82544),
    ("Huntington", 36520),
    ("Jackson", 44231),
    ("Jasper", 33562),
    ("Jay", 20436),
    ("Jefferson", 32308),
    ("Jennings", 27735),
    ("Johnson", 158167),
    ("Knox", 36594),
    ("Kosciusko", 79456),
    ("Lagrange", 39614),
    ("Lake", 485493),
    ("La Porte", 109888),
    ("Lawrence", 45370),
    ("Madison", 129569),
    ("Marion", 964582),
    ("Marshall", 46258),
    ("Martin", 10255),
    ("Miami", 35516),
    ("Monroe", 148431),
    ("Montgomery", 38338),
    ("Morgan", 70489),
    ("Newton", 13984),
    ("Noble", 47744),
    ("Ohio", 5875),
    ("Orange", 19646),
    ("Owen", 20799),
    ("Parke", 16937),
    ("Perry", 19169),
    ("Pike", 12389),
    ("Porter", 170389),
    ("Posey", 25427),
    ("Pulaski", 12353),
    ("Putnam", 37576),
    ("Randolph", 24665),
    ("Ripley", 28324),
    ("Rush", 16581),
    ("St. Joseph", 271826),
    ("Scott", 23873),
    ("Shelby", 44729),
    ("Spencer", 20277),
    ("Starke", 22995),
    ("Steuben", 34594),
    ("Sullivan", 20669),
    ("Switzerland", 10751),
    ("Tippecanoe", 195732),
    ("Tipton", 15148),
    ("Union", 7054),
    ("Vanderburgh", 181451),
    ("Vermillion", 15498),
    ("Vigo", 107038),
    ("Wabash", 30996),
    ("Warren", 8265),
    ("Warrick", 62998),
    ("Washington", 28036),
    ("Wayne", 65884),
    ("Wells", 28296),
    ("White", 24102),
    ("Whitley", 33964)], columns=['COUNTY_NAME', 'population'])
  populations.set_index('COUNTY_NAME', inplace=True)
  isdh_data.set_index('COUNTY_NAME', inplace=True)
  isdh_data = pd.concat([isdh_data,populations], axis=1)

  return(isdh_data)

def get_beds_and_vents_data():
  url = f"https://hub.mph.in.gov/dataset/4d31808a-85da-4a48-9a76-a273e0beadb3/resource/0c00f7b6-05b0-4ebe-8722-ccf33e1a314f/download/covid_report_bedvent_date.xlsx"
  return(pd.read_excel(url, index_col='DATE'))

def get_trend_data():
  url = f"https://hub.mph.in.gov/dataset/ab9d97ab-84e3-4c19-97f8-af045ee51882/resource/182b6742-edac-442d-8eeb-62f96b17773e/download/covid_report_date.xlsx"
  return pd.read_excel(url, index_col='DATE')

def generate_county_table(data):
  totals = data.sum()

  list = []
  for index, row in data.iterrows():
    county_name = index.title().replace("De Kalb", "DeKalb").replace("La Porte", "LaPorte").replace("Lagrange", "LaGrange").replace("St Joseph", "St. Joseph")
    list.append("|-")
    list.append(f"! style=\"padding:0px 2px;\" |[[{county_name} County, Indiana|{county_name}]]")
    list.append(f"| style=\"padding:0px 2px;\" |{row['COVID_COUNT']:,}")
    list.append(f"| style=\"padding:0px 2px;\" |{row['COVID_DEATHS']:,}")
    list.append(f"| style=\"padding:0px 2px;\" |{row['population']:,}")
    list.append(f"| style=\"padding:0px 2px;\" |{(row['COVID_COUNT']/(row.population/float(100000))):,.01f}")

  separator = '\n'

  table_template = f"""<div class="tp-container" style="float:left;max-width:100%;overflow-y:auto;padding-right:0em;margin: 0 0 0.5em 1em">
{{| class="wikitable plainrowheaders sortable" style="text-align:right; font-size:85%; margin:0"
|+ {{{{Navbar-collapsible|{{{{resize|98%|[[COVID-19 pandemic in Indiana|COVID-19 cases in Indiana]] by [[List of counties in Indiana|county]]}}}}|COVID-19 pandemic data/Indiana medical cases by county}}}}
|-
! style="text-align:right; padding-right:3px;" scope="col" |County{{{{efn|County of residence for individual with a positive test}}}}
! style="text-align:right; padding-right:3px;" scope="col" |Cases
! style="text-align:right; padding-right:3px;" scope="col" |Deaths
! style="text-align:right; padding-right:3px;" scope="col" data-sort-type="number" |Population<ref>{{{{cite web |title=County Population Totals: 2010-2019|url=https://www.census.gov/data/tables/time-series/demo/popest/2010s-counties-total.html|accessdate=2020-05-02}}}}</ref>
! style="text-align:right; padding-right:3px;" scope="col" data-sort-type="number" |{{{{abbr|Cases / 100k|Cases per 100,000 in population}}}}
|-
! style="text-align:right; padding-right:17px; padding-left:3px;" scope="row" |'''92 / 92'''
! style="text-align:right; padding-right:17px; padding-left:3px;" scope="row" |'''{totals.COVID_COUNT:,}'''
! style="text-align:right; padding-right:17px; padding-left:3px;" scope="row" |'''{totals.COVID_DEATHS:,}'''
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
</noinclude>"""

  print(table_template)

def generate_infobox(confirmed_cases, all_beds, icu_beds, vents, deaths):
  infobox_template = f"""{{{{short description|Ongoing COVID-19 viral pandemic in Indiana, United States}}}}
{{{{Infobox outbreak
| name               = COVID-19 pandemic in Indiana
| disease            = [[COVID-19]]
| virus_strain       = [[SARS-CoV-2]]
| location           = [[Indiana]], US
| first_case         = [[Indianapolis]]
| arrival_date       = March 6, 2020
| confirmed_cases    = {confirmed_cases:,}
| hospitalized_cases =  (current)<ref>{{Cite web |title=ISDH - Novel Coronavirus: Novel Coronavirus (COVID-19) |author= |work=coronavirus.in.gov |date= |access-date=2020-07-28|url= https://www.coronavirus.in.gov/}}</ref>
|| critical_cases     = {icu_beds:,}<ref name=beds-vents>{{{{cite web|url=https://hub.mph.in.gov/dataset/4d31808a-85da-4a48-9a76-a273e0beadb3/resource/0c00f7b6-05b0-4ebe-8722-ccf33e1a314f/download/covid_report_bedvent_date.xlsx|title=COVID-19 Beds and Vents|publisher=Indiana State Department of Health|access-date={datetime.datetime.today().strftime('%Y-%m-%d')}}}}}</ref>
| ventilator_cases   = {vents:,}<ref name=beds-vents/>
| deaths             = {deaths:,}
| map1               = COVID-19 rolling 14day Prevalence in Indiana by county.svg
| legend1            = {{{{COVID-19 pandemic in the United States new cases prevalence legend|state=Indiana}}}}
| map2               = COVID-19 Prevalence in Indiana by county.svg
| legend2            = {{{{COVID-19 pandemic in the United States prevalence legend|state=Indiana}}}}
| website            = {{{{URL|https://www.in.gov/coronavirus/}}}}<br>{{{{URL|https://backontrack.in.gov/}}}}
}}}}
{{{{COVID-19 pandemic data/United States/Indiana medical cases chart}}}}
The [[COVID-19 pandemic]] was confirmed to have reached the U.S. state of [[Indiana]] on March 6, 2020. As of {datetime.datetime.today().strftime('%B %d, %Y')}, the Indiana State Department of Health (ISDH) had confirmed {confirmed_cases:,} cases in the state and {deaths:,} deaths. As of July 3, 2020, all 92 counties have reported at least 10 cases with [[Pike County, Indiana|Pike County]] being the last to surpass this threshold.<ref>{{{{Cite web|url=https://www.in.gov/coronavirus/|title=ISDH – Novel Coronavirus: Novel Coronavirus (COVID-19)|website=www.in.gov|access-date={datetime.datetime.today().strftime('%Y-%m-%d')}}}}}</ref>"""

  print(infobox_template)

def generate_template_data(trend):
  list = []
  for index, row in trend.iterrows():
    list.append(f"{index};{row['deaths']:.0f};;{row['cases']:.0f}")

  separator = '\n'

  template = f"""{{{{main|COVID-19 pandemic in Indiana}}}}<onlyinclude>
{{{{Medical cases chart
|disease    = COVID-19
|location   = Indiana
|location2  = United States
|outbreak   = COVID-19 pandemic
|recoveries = no <!-- ISDH is not reporting recoveries -->
|numwidth   = dddd
|rowheight  = 1.2
|duration   = 28
|altlbl1    = Total Confirmed Cases
|right2     = # of deaths
|collapsible=y
|data       =
{separator.join(list)}
|caption    = '''Source:''' {{{{Cite web|url=https://hub.mph.in.gov/dataset/covid-19-case-trend|title=ISDH - Novel Coronavirus|website=ISDH|language=en-US|access-date={datetime.datetime.today().strftime('%Y-%m-%d')}}}}}
}}}}
</onlyinclude>
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
    all_beds = '(presently not reported)'
    icu_beds = beds_and_vents.loc[beds_and_vents.index[-1], 'BEDS_ICU_OCCUPIED_COVID_19']
    vents = beds_and_vents.loc[beds_and_vents.index[-1], 'VENTS_ALL_USE_COVID_19']

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