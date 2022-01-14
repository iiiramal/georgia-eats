import sqlalchemy as sql
from sqlalchemy_utils import database_exists, create_database
from api_keys import password, yelp_key
import yelp
import georgiaeats
from sqlalchemy.orm import Session

def create_db(): 
    try:
        engine = sql.create_engine(f"postgresql://postgres:{password}@localhost/GeorgiaEatsDB")
        print("Connection to PostgreSQL successful.")
        if not database_exists(engine.url):
            create_database(engine.url)
            print("New database created: GeorgiaEatsDB")
            #create_tables(engine)
        
        else:
            print("GeorgiaEatsDB found.")
    except:
        print("Failed to connect.")

def create_tables(engine):

     with engine.connect():
                engine.execute( 'create table zip_codes\
                    (zip_code varchar PRIMARY KEY,\
                    city text,\
                    state text,\
                    lat varchar,\
                    lng varchar);\
                    \
                    create table restaurants\
                    (zip_code varchar,\
                    bus_id text,\
                    name varchar,\
                    category1 text,\
                    category2 text,\
                    category3 text,\
                    price text,\
                    rating text,\
                    address text,\
                    city text,\
                    phone varchar,\
                    image varchar,\
                    latitude decimal,\
                    longitude decimal,\
                    primary key (Bus_ID, zip_code),\
                    foreign key (zip_code) references zip_codes(zip_code) ON DELETE CASCADE);\
                    \
                    create table restaurants_all_categories\
                    (zip_code varchar,\
                    bus_id text,\
                    name varchar,\
                    categories text,\
                    price text,\
                    rating text,\
                    address text,\
                    city text,\
                    phone varchar,\
                    image varchar,\
                    latitude decimal,\
                    longitude decimal,\
                    primary key (Bus_ID, zip_code),\
                    foreign key (zip_code) references zip_codes(zip_code) ON DELETE CASCADE)')
                    
create_db()