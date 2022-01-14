#Imports
import pandas as pd
import requests
import sqlalchemy as sql
from sqlalchemy.orm import Session
from api_keys import password, yelp_key, g_key

engine = sql.create_engine(f"postgresql://postgres:{password}@localhost/GeorgiaEatsDB")
session = Session(engine)
   
#with engine.connect() as cnxn:  # the connection will automatically close after executing the with block
 #                   zip_df_2.to_sql(table_name, cnxn, if_exists="append", index=False)
  #                  print(f"{table_name} successfully inserted.")  

def  db_check(zip_dict):
    #test_target = '38118'
    #test_days = 7

    

    # Get Google developer API key from file: api_keys.py
    #from api_keys import g_key

    # Test Target (this will be passed in from calling routine)
    delete_list = []
    lat_list = []
    lng_list = []
    zip_coord = []

    for zip in zip_dict:
        try:
            # Build the endpoint URL
            #print(zip)
            target_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={zip}&key={g_key}"

            # Run a request to the endpoint and convert result to a json
            response = requests.get(target_url)
            geo_data = response.json()

            # Extract latitude and longitude and create key variable
            lat = round(geo_data["results"][0]["geometry"]["location"]["lat"],2)
            lng = round(geo_data["results"][0]["geometry"]["location"]["lng"],2)

            zip_coord.append(zip)
            lat_list.append(lat)
            lng_list.append(lng)

            #print(zip_dict)
            #print[zip['zip_code']]
            #print(geo_data)
            #Yelp_Pull_Enter(lat, lng)
        except:
            print(geo_data)
            delete_list.append(zip)
    
    print(delete_list)
    zip_dict_2 = zip_dict.copy()

    for deletes in delete_list:
        del zip_dict_2[deletes]
    
    for y in range(len(zip_coord)):
        zip_dict_2[zip_coord[y]]['lat'] = lat_list[y]
        zip_dict_2[zip_coord[y]]['lng'] = lng_list[y]
    
    zip_df_2 = pd.DataFrame.from_dict(zip_dict_2,orient='index')

    Yelp_Pull_Enter(lat_list,lng_list,zip_coord,zip_df_2)
    #print(zip_df_2.head())

    #for zip in zip_dict_2:
    #   print(zip_dict_2[zip])



def Yelp_Pull_Enter(lat_list, lng_list, zip_coord, zip_df_2):

    categories = ['restaurants']

    # Test parameters (these will be passed in from calling routine)
    #input_lat = lat
    #input_lon = lng

    #category = 'restaurants'

    # Construct the search parameters
    headers = {'Authorization': 'Bearer {}'.format(yelp_key)}
    url = 'https://api.yelp.com/v3/businesses/search'

    #Insert Search Table Row

    table_name = 'zip_codes'
    
    #for zip in zip_list:
        #db_check(zip)
    for y in range(len(zip_coord)):

        for category in categories:

            table_name = category

            params = {
                'categories': category, 
                'latitude': lat_list[y],
                'longitude': lng_list[y],
                'limit': 50}

            # Run a request to the endpoint and convert to a json
            try:
                response = requests.get(url, headers=headers, params=params, timeout=5)
                yelp_data = response.json()
            except:
                print(f"A Yelp error has occured: {response.status_code} {response.reason}")    
                #return ("N/A")

            num_places = len(yelp_data["businesses"])

            # Define empty lists to place data into
            zip_code = []
            bus_id = []
            name = []
            category1 =[]
            category2 =[]
            category3 =[]
            price = []
            rating = []
            address = []
            city = []
            zip_code = []
            phone = []
            img = []
            latitude = []
            longitude = []

            # Populate the lists
            for place in yelp_data["businesses"]:
                price_available =  "price" in place
                zip_code.append(zip)
                bus_id.append(place['id'])
                name.append(place['name'])
                for y in range(len(place['categories'])):
                    if y == 0:
                        print(f'y = {y}')
                        category1.append(place['categories'][y]['title'])
                        print(f'Category1 = {category1}')
                    elif y == 1:
                        print(f'y = {y}')
                        category2.append(place['categories'][y]['title'])
                        print(f'Category2 = {category2}')
                    elif y == 2:
                        print(f'y = {y}')
                        category3.append(place['categories'][y]['title'])
                        print(f'Category3 = {category3}')
                if price_available:
                    price.append(place['price'])
                else:
                    price.append('N/A')  # in case the price rating is missing
                rating.append(place['rating'])
                address.append(place['location']['address1'])
                city.append(place['location']['city'])
                latitude.append(place['coordinates']['latitude'])
                longitude.append(place['coordinates']['longitude'])
                phone.append(place['phone'])
                img.append(place['image_url'])

            # Put lists into dictionary
            yelp_dict = {
                'zip_code': zip_code,
                'bus_id': bus_id,
                'bus_name':name,
                'category1':name,
                'category2':name,
                'category3':name,
                'price':price,
                'rating':rating,
                'address':address,
                'city':city,
                'zip_code':zip_code,
                'phone':phone,
                'image':img,
                'latitude':latitude,
                'longitude':longitude 
            }

            # Convert dictionary to dataframe
            yelp_DF = pd.DataFrame(yelp_dict)

            #try:
            with engine.connect() as cnxn:  # the connection will automatically close after executing the with block
                        zip_df_2.to_sql(table_name, cnxn, if_exists="append", index=False)
            with engine.connect() as cnxn:  # the connection will automatically close after executing the with block           
                        yelp_DF.to_sql(table_name, cnxn, if_exists="append", index=False)
                        print(f"{table_name} successfully inserted.")  
            #except: 
                #print('There was an error connecting with the database.')
            # Return the dataframe
            #print(yelp_DF.head())