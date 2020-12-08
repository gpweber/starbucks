from scrapy import Spider, Request
from starbucks.items import StarbucksItem
import pandas as pd
import sys
import os 
import csv
import re
                
class StarbucksSpider(Spider):
    name = 'starbucks_spider'
    allowed_domains = ['www.city-data.com'] #MAIN WEBSITE
    start_urls = ['https://www.city-data.com/city/Anchorage-Alaska.html'] #INITIAL WEBPAGE FOR SEARCH

    def parse(self, response):

        directory = pd.read_csv('/Users/datscigreg/Desktop/M0projects/WebScraping/starbucks/starbucks/spiders/starbucksdirectory.csv')

        states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
        }
        
        us_starbucks = directory[directory['Country']=='US']
        us_starbucks = us_starbucks.sort_values(by = "State/Province")
        us_starbucks.reset_index(inplace = True, drop = True) 
        
        city_state_urls = list(set([(city, states[state_initials], f"https://www.city-data.com/city/{city}-{states[state_initials]}.html".replace(' ', '-').lower()) for city,state_initials in zip(us_starbucks['City'], us_starbucks['State/Province'])]))

        for city, state, url in city_state_urls[1546::-1]:
            yield Request(url=url, callback=self.parse_city_page, meta={'state': state, 'city': city})
        
    
    def parse_city_page(self, response):
        pop_section = re.sub('[,|.|(|)|%]',"", response.xpath('//*[(@id = "city-population")]/text()').extract_first().strip())
        try:
            population, percent_urban, percent_rural =map(lambda x: int(x),re.findall('\d+',pop_section))
        except:
            population = int(re.findall('\d+',pop_section)[0])
            percent_urban = None 
            percent_rural = None     
        
        age_city, age_state = response.xpath('//*[(@id = "median-age")]//text()').extract()[1:4:2]
        age_city = float(age_city[0:4])
        age_state = float(age_state[0:4])

        median_income, state_median_income = response.xpath('//*[(@id = "median-income")]//text()').extract()[8:11:2]
        median_income = float(median_income.strip('$').replace(',',''))
        state_median_income = float(state_median_income.strip('$').replace(',',''))

        cost_of_living_index = float(response.xpath('//*[(@id = "cost-of-living-index")]//text()').extract()[1])

        nearest_city_over_1E6pop, distance_to_nearest_city  = response.xpath('//*[(@id = "nearest-cities")]//text()').extract()[2:5:2]
        nearest_city_over_1E6pop = nearest_city_over_1E6pop.split(',')[0] 
        distance_to_nearest_city = float(re.findall('\d+\.?\d*',distance_to_nearest_city)[0])
    
        lesbian_couples_percent_self_reported, gay_couples_percent_self_reported = response.xpath('//*[(@id = "households-stats")]//text()').extract()[-8:-3:4] 
        lesbian_couples_percent_self_reported =  float(re.findall('\d+\.?\d*',lesbian_couples_percent_self_reported)[0])
        gay_couples_percent_self_reported = float(re.findall('\d+\.?\d*',gay_couples_percent_self_reported)[0])

        num_grocery_stores, num_grocery_per_1E5_state = response.css('h3+ .hgraph tr+ tr td , h3+ .hgraph > b , h3+ .hgraph b b').extract()[0:4:3]
        num_grocery_stores =  float(re.findall('\d+',num_grocery_stores)[0])
        num_grocery_per_1E5_state = float(re.findall('\d+\.?\d*',num_grocery_per_1E5_state)[1])

        item = StarbucksItem()
        item['city'] = response.meta['city']
        item['state'] = response.meta['state']
        item['population'] = population
        item['percent_urban'] = percent_urban 
        item['percent_rural'] = percent_rural
        item['age_city'] = age_city
        item['age_state'] = age_state
        item['median_income'] = median_income
        item['state_median_income'] = state_median_income
        item['cost_of_living_index'] = cost_of_living_index
        item['nearest_city_over_1E6pop'] = nearest_city_over_1E6pop
        item['distance_to_nearest_city'] = distance_to_nearest_city
        item['lesbian_couples_percent_self_reported'] = lesbian_couples_percent_self_reported
        item['gay_couples_percent_self_reported'] = gay_couples_percent_self_reported
        item['num_grocery_stores'] = num_grocery_stores
        item['num_grocery_per_1E5_state'] = num_grocery_per_1E5_state

        yield item



