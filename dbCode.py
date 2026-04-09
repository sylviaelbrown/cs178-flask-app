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


def country_by_language(language):
    query = '''
        SELECT country.Name AS country, country.Continent, country.Region, country.Population, countrylanguage.IsOfficial
        FROM country 
        JOIN countrylanguage 
        ON country.Code = countrylanguage.CountryCode 
        WHERE countrylanguage.Language= %s 
        ORDER BY country.Name
    '''
    return execute_query(query, (language,)) #had to research and experiment with syntax here, and below

#had to google and experiment with syntax on the %s

def country_by_government(government):
    query = '''
        SELECT country.Name AS country, country.Continent, country.Region, country.Population, country.GovernmentForm
        FROM country 
        WHERE GovernmentForm = %s
        ORDER BY country.Name
    '''
    return execute_query(query, (government,))


def add_country_to_favorites(country_name, city_name, notes):
    table.put_item(
    Item={
        'country_name':country_name,
        'city_name':city_name,
        'notes':notes
    }
)
    
def delete_favorited_country(country_name):
    try: 
        table.delete_item(
        Key={
            'country_name': country_name,
        },
        ConditionExpression="attribute_exists(country_name)" #combined with route, if user tries to delete an item that does not exist, its going to to say 'you can't do that!'
        )
        return True
    except:
        return False
    
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
            ConditionExpression="attribute_exists(country_name)" #combined with route, if user tries to update an item that does not exist, its going to to say 'you can't do that!'
        )
        return True
    except: 
        return False
        







