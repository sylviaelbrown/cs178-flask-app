# World Travel Planning System

**CS178: Cloud and Database Systems — Project #1**
**Author:** Sylvia E. Brown
**GitHub:** sylviaelbrown

---

## Overview

For this project I have created a world travel planning system. The website allows users to explore information regarding countries around the world, in which it references the 'worlds' database stored in RDS. Users may then choose to favorite countries for potential travel. This list of favorited countries is a non-relational database where users can store a country's name, a specific city, and any other additional notes they desire. Users may add to this list, as well as delete, update, and view items in this list. 

---

## Technologies Used

- **Flask** — Python web framework
- **AWS EC2** — hosts the running Flask application
- **AWS RDS (MySQL)** — relational database for querying and retrieving information from the 'worlds' database. 
- **AWS DynamoDB** — non-relational database for adding, deleting, updating, and reading information to/from a favorite countries list, including country name, city, and additional notes. 
- **GitHub Actions** — auto-deploys code from GitHub to EC2 on push
- **ChatGPT** - used to finalize website with fancy looking HTML -> makes it look pretty!

---

## Project Structure

```
cs178-flask-app/
├── flaskapp.py                        # Main Flask application — routes and app logic
├── dbCode.py                          # Database helper functions (MySQL connection + queries)
├── creds.py                           # Private credentials file (excluded from GitHub with .gitignore)
├── README.md                          # Project documentation and setup instructions
├── .gitignore                         # Excludes creds.py, __pycache__, and other unnecessary files
├── .github/
│   ├── workflows/
│       ├── deploy.yml                 # GitHub Actions workflow for deployment
├── templates/
│   ├── home.html                       # Landing page
│   ├── add_favorite_country.html       # Form to add a country to favorites
│   ├── update_favorite_country.html    # Form to update a favorited country
│   ├── delete_favorite_country.html    # Form to delete a favorited country
│   ├── display_favorite_countries.html # Displays the favorite countries list
│   ├── countries_by_government.html    # Displays countries filtered by government type
│   ├──countries_by_language.html       # Displays countries filtered by language
└── __pycache__/                        # Python bytecode cache files

```




---

## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/sylviaelbrown/cs178-flask-app.git
   cd cs178-flask-app
   ```

2. Install dependencies:

   ```bash
   pip3 install flask pymysql boto3
   ```

3. Set up your credentials (see Credential Setup below)

4. Run the app:

   ```bash
   python3 flaskapp.py
   ```

5. Open your browser and go to `http://127.0.0.1:8080`

---

## How to Access in the Cloud

The app is deployed on an AWS EC2 instance. To view the live version:

```
http://44.222.227.131:8080/
```

_(Note: the EC2 instance may not be running after project submission.)_

---

## Credential Setup

This project requires a `creds.py` file that is **not included in this repository** for security reasons.

Create a file called `creds.py` in the project root with the following format (see `creds_sample.py` for reference):

```python
# creds.py — do not commit this file
host = "your-rds-endpoint"
user = "admin"
password = "your-password"
db = "your-database-name"
```

---

## Database Design

### SQL (MySQL on RDS)

**Worlds Database:**

- `country` — stores country name, government type, population, region, and other important country data; primary key is `Code`
- `countrylanguage` — stores whether a language is official and speaking percentage; foreign key links to `country` with CountryCode

The JOIN query used in this project combines the country and countrylanguage tables through country.Code and countrylanguage.CountryCode. This way, a user can explore and display information regarding countries that speak specific languages, which is a great tool when planning your travels.

### DynamoDB

- **Table name:** `FavoriteCountries`
- **Partition key:** `country_name`
-**Attributes:** country_name, city_name, notes
- **Used for:** After exploring information regarding different countries using the provided filters, users may store their favorites, which allows them to save the country name, a specific city, and any additional notes.

---

## CRUD Operations

| Operation | Route      | Description    |
| --------- | ---------- | -------------- |
| Create    | `/add-favorite-country` | User may add a country to their favorites list |
| Read      | `/display-favorite-countries` | User may view their list of favorited countries |
| Update    | `/update-favorite-country` | User may update information regarding a country in their favorites list (given it exists) |
| Delete    | `/delete-favorite-country` | User may delete a country from their favorites list (given it exists) |

---

## Challenges and Insights

<!-- What was the hardest part? What did you learn? Any interesting design decisions? -->
For me, the hardest aspect of this project was separating my helper tools and Flask routes. In previous labs, we had kept everything pretty much in one file, so it took a bit of practice to figure out what needed to exist where. I also faced a bit of a challenge with error handling. With this, I eventually added .strip() and .lower() functions to normalize spaces and capitalization, and also utilized try/except in the update and delete helper tools to ensure that the information being altered or deleted actually exists. With this, I again faced the challenge of separating the helper tools and Flask routes, which I thought was more challenging when it came to the try/except.
---

## AI Assistance

<!-- List any AI tools you used (e.g., ChatGPT) and briefly describe what you used them for. Per course policy, AI use is allowed but must be cited in code comments and noted here. -->
ChatGPT was used for the very fancy (and very pink) HTML. The AI generated HTML was not utilized until much futher on, after all the routes and helper fucntions were created and working. 



