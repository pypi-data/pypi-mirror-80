import pandas as pd
from pprint import pprint
import boto3

class Search:
  ''' a search class to return search result'''
  def __init__(self, searchTerm:str, key, pw, region = 'ap-southeast-1',
               endpoint = '',
               requiredFields = [
                                 'villa_category_l1_en',
                                 'villa_category_l2_en',
                                 'villa_category_l3_en',
                                 'villa_category_l2_en'
               ] ):
    self.searchTerm = searchTerm
    self.cloudSearch = boto3.client('cloudsearchdomain' ,
                                    aws_access_key_id=key,
                                    aws_secret_access_key=pw,
                                    region_name=region,
                                    endpoint_url= endpoint)
    self.requiredFields = requiredFields

  def createCriticalColumns(self, df):
    ''' fill in required fields if not exist'''
    for col in self.requiredFields:
      if col not in df:
        df[col] = 'noData'
    return df.fillna('noData')

  def returnFullSearch(self):
    query = self.searchTerm
    searchResults = self.cloudSearch.search(query = query)['hits']
    results = []
    items = map(lambda x: x.get('fields'),searchResults.get('hit'))
    items =  map(lambda x: dict(zip(x.keys(),map(lambda y: y[0],x.values()))),items)
    return list(items)

  def sortedSearch(self):
    items = self.returnFullSearch()
    print(f'raw search result is {pd.DataFrame(items, columns= self.requiredFields)}')
    if not items: return []
    df =  self.sortResultsV2(items)
    # return df
    output_dict = list(
        df.drop(
            ['isNotFresh', 'cat2Count', 'finalCat'], axis = 1
            ).T.to_dict().values()
        )
    return output_dict

  def sortResultsV2(self, items):
    df = pd.DataFrame(items)
    df = self.createCriticalColumns(df)
    df['isNotFresh'] = df['villa_category_l1_en'] != 'Fresh'
    cat2Count = df.groupby('villa_category_l2_en').count()['pr_code']
    df['cat2Count'] = df['villa_category_l2_en'].apply(lambda x: -cat2Count[x])
    df['finalCat'] = df['villa_category_l4_en'].fillna(df['villa_category_l3_en'])
    return df.sort_values(by=['isNotFresh', 'cat2Count', 'finalCat', 'pr_engname'], ascending= True)

