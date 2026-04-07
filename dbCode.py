# dbCode.py
# Author: Sylvia Brown
# Helper functions for database connection and queries

import pymysql
import creds

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
