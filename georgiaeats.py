from venv import create
import pandas as pd
import yelp

def create_df():

    filepath = 'zip_code_database.csv'
    zip_df = pd.read_csv(filepath, index_col=False)
    #print(zip_df.head())
    zip_df = zip_df.rename(columns={'zip': 'zip_code', 'primary_city': 'city'})
    zip_df = zip_df.loc[(zip_df['state'] == 'GA') & (zip_df['type'] == 'STANDARD') ]
    zip_df = zip_df[['zip_code','city','state']]
    zip_df = zip_df.set_index('zip_code')
    zip_dict = zip_df.to_dict('index')
    #print(len(zip_dict['city']), len(zip_dict['state']))
    #print(zip_dict)
    #print(zip_df_2.head())
    #print(zip_dict.head())
    #lat_list = [125,386,927,567]
    #zip_change_list =[30002, 30004, 30005, 30008]
    #for y in range(len(zip_change_list)):
    #   zip_dict[zip_change_list[y]]['lat'] = lat_list[y]
    #zip_dict[30002]['lat'] = 35
    #print (zip_dict)
    #for zip in zip_dict:
     #   print(zip_dict[zip])

    
    #zip_list = zip_df['zip_code'].to_list()
    #print(zip_list)

    #copied_zip_dict = zip_dict.copy()
    #deletelist = [30002, 30008]

    #print(len(copied_zip_dict))
    #print(copied_zip_dict)
    #for zip in copied_zip_dict:
     #   print(zip)

    #for deletes in deletelist:
     #   print(f'I will now attempt to delete {deletes}')
      #  del copied_zip_dict[deletes]

    #for zip in copied_zip_dict:
     #   print(zip)

    
    #for zip in zip_dict:
     #   print(zip)
    yelp.db_check(zip_dict)

#zip_dict2 = create_df()

create_df()