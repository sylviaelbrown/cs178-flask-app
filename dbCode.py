# dbCode.py
# Author: Sylvia Brown
# Helper functions for database connection and queries

import pymysql
import creds
import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('FavoriteCountries')


def get_conn():
    """Returns a connection to the MySQL RDS instance."""
    conn = pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
    )
    return conn

def execute_query(query, args=()):
    """Executes a SELECT query and returns all rows as dictionaries."""
    cur = get_conn().cursor(pymysql.cursors.DictCursor)
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

def get_top_cities():
    query = '''
        SELECT Name, Population
        FROM city
        ORDER BY Population DESC
        LIMIT 10;
        '''
    return execute_query(query)

def country_by_language(language):
    query = '''
        SELECT country.Name AS country, country.Continent, country.Region, country.Population, countrylanguage.IsOfficial
        FROM country 
        JOIN countrylanguage 
        ON country.Code = countrylanguage.CountryCode 
        WHERE countrylanguage.Language= %s
        ORDER BY country.Name
    '''
    return execute_query(query, (language,))


def add_country_to_favorites(country_name, city_name, notes):
    table.put_item(
    Item={
        'country_name':country_name,
        'city_name':city_name,
        'notes':notes
    }
)
    
def delete_favorited_country(country_name):
    table.delete_item(
    Key={
        'country_name': country_name,
    }
)

def display_favorited_countries():
    response = table.scan()
    return response['Items']

def update_favorited_country(country_name, city_name, notes):
    try: 
        table.update_item(
            Key={
                'country_name':country_name
            },
            UpdateExpression="SET city_name = :c, notes = :n",
            ExpressionAttributeValues={":c": city_name, ":n": notes},
            ConditionExpression="attribute_exists(country_name)"
        )
    except: 
        return False
        







