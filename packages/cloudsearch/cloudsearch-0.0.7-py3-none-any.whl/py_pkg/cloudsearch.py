import pandas as pd
from pprint import pprint
import boto3

class Searcher:
  ''' a search class to return search result'''
  def __init__(self, searchTerm:str, key, pw, region = 'ap-southeast-1',
               endpoint = 'https://search-villa-cloudsearch-2-4izacsoytzqf6kztcyjhssy2ti.ap-southeast-1.cloudsearch.amazonaws.com'
               ):
    self.searchTerm = searchTerm
    self.cloudSearch = boto3.client('cloudsearchdomain' ,
                                    aws_access_key_id=key,
                                    aws_secret_access_key=pw,
                                    region_name=region,
                                    endpoint_url= endpoint)

  def returnFullSearch(self):
    query = self.searchTerm
    searchResults = self.cloudSearch.search(query = query)['hits']
    results = []
    items = map(lambda x: x.get('fields'),searchResults.get('hit'))
    items =  map(lambda x: dict(zip(x.keys(),map(lambda y: y[0],x.values()))),items)
    return items

def returnFullSearch(query):
  # query = self.searchTerm
  searchResults = cloudSearch.search(query = query)['hits']
  results = []
  items = map(lambda x: x.get('fields'),searchResults.get('hit'))
  items =  map(lambda x: dict(zip(x.keys(),map(lambda y: y[0],x.values()))),items)

def sortResultsV1(items):
  df = pd.DataFrame(items)
  df['isFresh'] = df['villa_category_l1_en'] == 'Fresh'
  cat2Count = df.groupby('villa_category_l2_en').count()['pr_code']
  df['cat2Count'] = df['villa_category_l2_en'].apply(lambda x: cat2Count[x])
  cat3Count = df.groupby('villa_category_l3_en').count()['pr_code']
  df['cat3Count'] = df['villa_category_l3_en'].apply(lambda x: -cat3Count[x])
  return df.sort_values(by=['isFresh', 'cat2Count', 'cat3Count'], ascending= False)

def sortResultsV2(items):
  df = pd.DataFrame(items)
  df['isNotFresh'] = df['villa_category_l1_en'] != 'Fresh'
  cat2Count = df.groupby('villa_category_l2_en').count()['pr_code']
  df['cat2Count'] = df['villa_category_l2_en'].apply(lambda x: -cat2Count[x])
  df['finalCat'] = df['villa_category_l4_en'].fillna(df['villa_category_l3_en'])
  return df.sort_values(by=['isNotFresh', 'cat2Count', 'finalCat', 'pr_online_name_en'], ascending= True)

def sortedSearch(query):
  items = returnFullSearch(query)
  df =  sortResultsV2(items)
  # return df
  output_dict = list(df.drop(['isNotFresh', 'cat2Count', 'finalCat'], axis = 1).T.to_dict().values())
  return output_dict
