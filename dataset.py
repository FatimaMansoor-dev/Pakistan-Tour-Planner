import json
# prompt: get request statement to get json from url

import pandas as pd
import requests

def hotel_data():

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }

    # Make requests for each number in the range and store the JSON responses in a list
    json_responses = [requests.get(f'https://www.agoda.com/api/cronos/geo/accommodations?pageTypeId=8&objectId={x}&accommodationFeaturesType=1', headers=headers).json() for x in range(275, 283)]

    my_df=pd.concat([pd.DataFrame(x) for x in json_responses],axis=0).reset_index(drop=True)

    my_df=(my_df.join(my_df['hotelcards'].apply(pd.Series)).drop('hotelcards', axis=1))

    my_df['hotelcity'] = my_df['hotelUrl'].str.split('-pk.html').str[0].str.split('/').str.get(-1)

    my_df['hotelprovince'] = my_df['title'].str.split(' hotels & accommodations').str[0]

    my_df.rename({'name':'hotelname','imgUrl':'hotelimg','starRating':'hotelrating','reviewSnippet':'hotelreview'},inplace=True,axis=1)

    my_df_filtered = my_df[['hotelname','hotelcity','hotelprovince','hotelimg','hotelUrl','hotelrating','hotelreview']]
    
    # my_df_filtered_dict = {category: [row.drop('hotelcity').to_dict() for index, row in my_df_filtered[my_df_filtered['hotelcity'] == category].iterrows()] for category in my_df_filtered['hotelcity'].unique()}
    return my_df_filtered
