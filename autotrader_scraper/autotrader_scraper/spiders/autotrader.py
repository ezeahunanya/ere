import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
import re
import json
from autotrader_scraper.items import AutotraderCarsItem
from scrapy.loader import ItemLoader
import numpy as np
from datetime import datetime as dt 
from autotrader_scraper.functions_module import get_dictionary_value


class AutotraderSpider(CrawlSpider):
    '''
    Represent a spider object which will crawl autotrader webpages.

    Attributes
    ----------
    name: str
        name of the spider object
    allowed_domains: list, optional
        list of url strings which spider is allowed to crawl
    start_urls: list of str
        urls to make initial requests
    rules: list
        rule objects to define how spider crawls the web
    '''

    name = 'autotrader'
    allowed_domains = ['autotrader.co.uk']
    start_urls = ['''https://www.autotrader.co.uk/car-search?postcode=n14an&make=&include-delivery-option=on&advertising-location=at_cars&page=1''']

    rules = (
            Rule(LinkExtractor(allow = ('/car-details/'), 
            restrict_css = ('li.search-page__result')), 
            callback = 'parse_car', follow=True),
            )

    def parse_car(self, response):
        '''
        Yields a request for the api endpoint of an individual car 
        advertisement.
        '''
        
        parsed_url = urlparse(response.url)
        advert_id = parsed_url.path.split('/')[-1]

        for item in response.css('script::text').getall():
            if re.search('window.AT.correlationId', item) != None:
                string = item
                correlation_id = re.search('\w+-\w+-\w+-\w+-\w+', string)[0]
                break
        
        car_details_api_endpoint = '''https://www.autotrader.co.uk/json/fpa/initial/{advert_id}?advertising-location=at_cars&guid={correlation_id}&include-delivery-option=on&onesearchad=New&onesearchad=Nearly%20New&onesearchad=Used&page=1&postcode=n14an&radius=1501&sort=relevance'''\
                                    .format(advert_id=advert_id, correlation_id=correlation_id)
        
        yield scrapy.Request(car_details_api_endpoint, 
                             callback=self.parse_car_api)

    def parse_car_api(self, response):
        '''
        Returns a scrapy request for extra car specifications.
        '''

        car_raw_data = response.text
        car_data = json.loads(car_raw_data)

        il = ItemLoader(item=AutotraderCarsItem())
        il.add_value('advert_id', get_dictionary_value(car_data, ['pageData', 
                                                       'ods', 'advertId']))
                                                       
        il.add_value('time_scraped', dt.now().time())
        
        il.add_value('date_scraped', dt.now().date())
        
        il.add_value('make', get_dictionary_value(car_data, ['vehicle', 'make']))
        
        il.add_value('model', 
                    get_dictionary_value(car_data, ['vehicle', 'model']))
        
        il.add_value('trim', get_dictionary_value(car_data, ['vehicle', 'trim']))
        
        il.add_value('manufactured_year', 
                     get_dictionary_value(car_data, ['vehicle', 'keyFacts', 
                                         'manufactured-year']))
        
        il.add_value('manufactured_year_identifier', 
                     get_dictionary_value(car_data, ['vehicle', 'keyFacts', 
                                          'manufactured-year']))
        
        il.add_value('body_type', 
                     get_dictionary_value(car_data, ['vehicle', 'keyFacts', 
                                          'body-type']))
        
        il.add_value('mileage', 
                     get_dictionary_value(car_data, ['vehicle', 'keyFacts', 
                                          'mileage']))
        
        il.add_value('engine_size', 
                     get_dictionary_value(car_data, ['vehicle', 'keyFacts', 
                     'engine-size']))
        
        il.add_value('transmission', 
                     get_dictionary_value(car_data, ['vehicle', 'keyFacts', 
                                          'transmission']))
        
        il.add_value('fuel_type', 
                     get_dictionary_value(car_data, ['vehicle', 'keyFacts', 
                                          'fuel-type']))
        
        il.add_value('doors', 
                     get_dictionary_value(car_data, ['vehicle', 'keyFacts', 
                                          'doors']))
        
        il.add_value('seats', 
                     get_dictionary_value(car_data, ['vehicle', 'keyFacts', 
                                          'seats']))
        
        il.add_value('number_of_owners', 
                     get_dictionary_value(car_data, ['vehicle', 'keyFacts', 
                                          'owners']))
        
        il.add_value('emission_scheme', 
                     get_dictionary_value(car_data, ['vehicle', 'keyFacts', 
                                          'emission-scheme']))
        
        il.add_value('vehicle_location_postcode', 
                     get_dictionary_value(car_data, ['vehicle', 
                                          'vehicleLocation', 'postcode']))
        
        il.add_value('vehicle_location_latitude', 
                     get_dictionary_value(car_data, ['vehicle', 
                                          'vehicleLocation', 'latLong']))
        
        il.add_value('vehicle_location_longitude', 
                     get_dictionary_value(car_data, ['vehicle', 
                                          'vehicleLocation', 'latLong']))
        
        il.add_value('vehicle_registration_mark', 
                     get_dictionary_value(car_data, ['vehicle', 'vrm']))
        
        il.add_value('derivative_id', 
                     get_dictionary_value(car_data, ['vehicle', 'derivativeId']))
        
        il.add_value('condition', 
                     get_dictionary_value(car_data, ['vehicle', 'condition']))
        
        il.add_value('imported', 
                     get_dictionary_value(car_data, ['vehicle', 'imported']))
        
        il.add_value('average_mileage', 
                     get_dictionary_value(car_data, ['vehicle', 
                                          'mileageDeviation', 
                                          'predictedMileage']))
        
        il.add_value('mileage_deviation', 
                     get_dictionary_value(car_data, ['vehicle', 
                                          'mileageDeviation', 'deviation']))
        
        il.add_value('mileage_deviation_type', 
                     get_dictionary_value(car_data, ['vehicle', 
                                          'mileageDeviation', 'type']))
        
        il.add_value('ad_description', 
                     get_dictionary_value(car_data, ['advert', 'description']))
        
        il.add_value('price', 
                     get_dictionary_value(car_data, ['advert', 'price']))
        
        il.add_value('price_excluding_fees', 
                     get_dictionary_value(car_data, ['advert', 
                                          'priceExcludingFees']))
        
        il.add_value('no_admin_fees', 
                     get_dictionary_value(car_data, ['advert', 'noAdminFees']))
        
        il.add_value('price_deviation', 
                     get_dictionary_value(car_data, ['advert', 
                                          'marketAveragePriceDeviation', 
                                          'deviation']))
        
        il.add_value('price_deviation_type', 
                     get_dictionary_value(car_data, ['advert', 
                                          'marketAveragePriceDeviation', 
                                          'type']))
        
        il.add_value('price_rating', 
                     get_dictionary_value(car_data, ['advert', 
                                          'priceIndicator', 'rating']))
        
        il.add_value('price_rating_label', 
                     get_dictionary_value(car_data, ['advert', 
                                          'priceIndicator', 'ratingLabel']))
        
        il.add_value('seller_name', 
                     get_dictionary_value(car_data, ['seller', 'name']))
        
        il.add_value('seller_id', 
                     get_dictionary_value(car_data, ['seller', 'id']))
        
        il.add_value('is_dealer_trusted', 
                     get_dictionary_value(car_data, ['seller', 
                                          'isTrustedDealer']))
        
        il.add_value('seller_longlat', 
                     get_dictionary_value(car_data, ['seller', 'longitude']))
        
        il.add_value('seller_segment', 
                     get_dictionary_value(car_data, ['seller', 'segment']))
        
        il.add_value('seller_rating', 
                     get_dictionary_value(car_data, ['seller', 'ratingStars']))
        
        il.add_value('total_reviews', 
                     get_dictionary_value(car_data, ['seller', 
                                          'ratingTotalReviews']))
        
        il.add_value('seller_postcode', 
                     get_dictionary_value(car_data, ['seller', 
                                          'location', 'postcode']))
        
        il.add_value('seller_address_one', 
                     get_dictionary_value(car_data, ['seller', 
                                          'location', 'addressOne']))
        
        il.add_value('seller_address_two', 
                     get_dictionary_value(car_data, ['seller', 
                                          'location', 'addressTwo']))
        
        il.add_value('page_url', 
                     get_dictionary_value(car_data, ['pageData', 'canonical']))
        
        il.add_value('number_of_photos', 
                     get_dictionary_value(car_data, ['pageData', 
                                          'tracking', 'number_of_photos']))
        
        il.add_value('co2_emissions', 
                     get_dictionary_value(car_data, ['vehicle', 'co2Emissions']))
        
        il.add_value('tax', get_dictionary_value(car_data, ['vehicle', 'tax']))
        
        item = il.load_item()
        
        car_full_spec_api_endpoint = 'https://www.autotrader.co.uk/json/taxonomy/technical-specification?derivative={derivative_id}&channel=cars'\
                                     .format(derivative_id=item['derivative_id'])

        yield scrapy.Request(car_full_spec_api_endpoint, 
                                 callback=self.parse_car_spec_api, 
                                 meta={'item': item})


    def parse_car_spec_api(self, response):
        '''
        Returns a car item for each advertisment with all the features
        '''
        
        car_specs_raw_data = response.text
        car_specs_data = json.loads(car_specs_raw_data)

        il2 = ItemLoader(item=response.meta['item'])
        
        dic = {}
        
        if car_specs_data != {}:
            for item in car_specs_data['techSpecs']:
                if item['specName'] == 'Performance':
                    for i in item['specs']:
                        name = str(i['name']).replace('0 - 60 mph', 'zero_to_sixty').replace('0 - 62 mph', 'zero_to_sixty_two').lower().replace(' ', '_')
                        value = i['value']
                        dic[name] = value

                elif item['specName'] == 'Dimensions':
                    for i in item['specs']:
                        name = str(i['name']).lower().replace(' ', '_').replace('(', '').replace(')', '')
                        value = i['value']
                        dic[name] = value

        
        il2.add_value('zero_to_sixty', 
                      get_dictionary_value(dic, ['zero_to_sixty']))
        
        il2.add_value('zero_to_sixty_two', 
                      get_dictionary_value(dic, ['zero_to_sixty_two']))
        
        il2.add_value('top_speed', get_dictionary_value(dic, ['top_speed']))
        
        il2.add_value('cylinders', get_dictionary_value(dic, ['cylinders']))
        
        il2.add_value('valves', get_dictionary_value(dic, ['valves']))
        
        il2.add_value('engine_power', 
                      get_dictionary_value(dic, ['engine_power']))
        
        il2.add_value('engine_torque', 
                      get_dictionary_value(dic, ['engine_torque']))
        
        il2.add_value('height', get_dictionary_value(dic, ['height']))
        
        il2.add_value('length', get_dictionary_value(dic, ['length']))
        
        il2.add_value('wheelbase', get_dictionary_value(dic, ['wheelbase']))
        
        il2.add_value('width', get_dictionary_value(dic, ['width']))
        
        il2.add_value('fuel_tank_capacity', 
                      get_dictionary_value(dic, ['fuel_tank_capacity']))
        
        il2.add_value('gross_vehicle_weight', 
                      get_dictionary_value(dic, ['gross_vehicle_weight']))
        
        il2.add_value('boot_space_seats_up', 
                      get_dictionary_value(dic, ['boot_space_seats_up']))
        
        il2.add_value('boot_space_seats_down', 
                      get_dictionary_value(dic, ['boot_space_seats_down']))
        
        il2.add_value('max_loading_weight', 
                      get_dictionary_value(dic, ['max_loading_weight']))
        
        il2.add_value('minimum_kerb_weight', 
                      get_dictionary_value(dic, ['minimum_kerb_weight']))

        return il2.load_item()
