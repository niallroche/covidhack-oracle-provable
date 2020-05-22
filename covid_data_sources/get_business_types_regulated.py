import requests as requests
import xmltodict
import json

def get_content(*args, **kwargs):

   response = requests.get('http://www.legislation.gov.uk/uksi/2020/350/schedule/2/data.xml')
   xml_dict = xmltodict.parse(response.text)

   parts = xml_dict['Legislation']['Secondary']['Schedules']['Schedule']['ScheduleBody']['Part']

   def get_business_type(list_values, name):

      if 'Text' in name['P1para'].keys() and 'P3' not in name['P1para'].keys():

         if 'Addition' in name['P1para']['Text']:
            try:
               list_values.append(name['P1para']['Text']['#text'])

            except:
               list_values.append(name['P1para']['Text']['Addition']['#text'])

         else:
            list_values.append(name['P1para']['Text'])

      elif 'P2' in name['P1para'].keys():
         for sub_list in name['P1para']['P2']:
            list_values.append(sub_list['P2para']['Text'])

      elif 'P3' in name['P1para'].keys():
         for sub_list in name['P1para']['P3']:
            list_values.append(sub_list['P3para']['Text']['Substitution']['#text'])

      return list_values

   business_closures = []
   business_exceptions = []

   for i, part in enumerate(parts):
      for name in part['P1']:

         # From part 1 to part 2 are the business subject to closure
         if i < 2:
            business_closures = get_business_type(business_closures, name)

         # Part 3 of the listings corresponds to the exceptions
         if i == 2:
            business_exceptions = get_business_type(business_exceptions, name)


   def give_format(list_values):
      list_values = [b.split("except")[0] for b in list_values]
      list_values = [b.split("subject")[0] for b in list_values]
      list_values = [b.rstrip(".") for b in list_values]
      list_values = [b.replace("including", "") for b in list_values]

      return list_values

   def split_words(list_v, split_char):
      for i, v in enumerate(list_v):
         if split_char in v:
            list_v.extend([s.strip() for s in v.split(split_char)])
            del list_v[i]
      return list_v

   business_closures = give_format(business_closures)
   business_exceptions = give_format(business_exceptions)

   business_closures = split_words(business_closures, ',')
   business_closures = split_words(business_closures, ',')

   business_exceptions = split_words(business_exceptions, ',')
   business_exceptions = split_words(business_exceptions, ',')

   business_closures = [b.rstrip("(") for b in business_closures]
   business_closures = [b.rstrip(",") for b in business_closures]
   business_closures = [b.strip().capitalize() for b in business_closures]

   business_exceptions = [b.rstrip("(") for b in business_exceptions]
   business_exceptions = [b.rstrip(",") for b in business_exceptions]
   business_exceptions = split_words(business_exceptions, ' or ')
   business_exceptions = [b.strip().capitalize() for b in business_exceptions]

   # Remove empty strings
   business_closures = [b for b in business_closures if b != ""]
   business_exceptions = [b for b in business_exceptions if b != ""]

   # Remove not needed empty words strings
   business_closures = [b for b in business_closures if b != "And"]
   business_exceptions = [b for b in business_exceptions if b != "And"]

   result = {'business_closures': business_closures,
             'business_exceptions': business_exceptions}


   # with open('business_closures.json', 'w+') as json_file:
   #     json.dump(result, json_file, indent=4)
   #
   # json_data = json.dumps(result, indent=4)
   # print(json_data)

   return result