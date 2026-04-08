# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import get_top_cities
from dbCode import country_by_language
from dbCode import add_country_to_favorites
from dbCode import delete_favorited_country

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-favorite-country', methods=['GET', 'POST'])
def add_favorite_country():
    if request.method == 'POST':
        # Extract form data
        country_name = request.form['country_name']
        city_name = request.form['city_name']
        notes = request.form['notes']
        
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("Country Name:", country_name, "City name: ", city_name, "Notes: ", notes)
        
        add_country_to_favorites(country_name, city_name, notes)

        flash('Country added to favorites! Huzzah!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_favorite_country.html')

@app.route('/delete-favorite-country',methods=['GET', 'POST'])
def delete_favorite_country():
    if request.method == 'POST':
        # Extract form data
        country_name = request.form['country_name']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("Country to delete:", country_name)
        
        delete_favorited_country(country_name)
        flash('Country deleted successfully! Hoorah!', 'warning') 
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('delete_favorite_country.html')


@app.route('/display-users')
def display_users():
    # hard code a value to the users_list;
    # note that this could have been a result from an SQL query :) 
    users_list = (('John','Doe','Comedy'),('Jane', 'Doe','Drama'))
    return render_template('display_users.html', users = users_list)


@app.route('/top-pop-city')
def top_cities():
    cities = get_top_cities()
    return render_template("top_cities.html", results=cities)
    


@app.route('/countries-by-language', methods=['GET', 'POST'])
def countries_by_language():
    country_list = []
    if request.method == 'POST':
        # Extract form data
        language = request.form['language']
        print("Enter a lanuage:", language)
        country_list = country_by_language(language)
        
    return render_template('countries_by_language.html',results=country_list)




# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
