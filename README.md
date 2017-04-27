# Vermont Public Radio Alexa Skill

This project is a [Flask-Ask](https://github.com/johnwheeler/flask-ask)-based web application, providing a Voice User Interface to [Vermont Public Radio](https://vpr.net) programming.

Using Alexa AudioDirectives, it allows users to:

* play episodic (podcast) VPR programming
* stream live VPR programming including:
  ** VPR Live Stream
  ** VPR Jazz
  ** VPR Classical
  
## Running the Alexa Skill

It's easiest to run the skill in [Heroku](https://heroku.com) using the provided [Procfile](./Procfile). Follow the [getting started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python) documentation online.

* **FLASK_SECRET_KEY**
  * Sets the `SECRET_KEY` value on the Flask app. See [http://flask.pocoo.org/docs/0.12/config/#builtin-configuration-values](http://flask.pocoo.org/docs/0.12/config/#builtin-configuration-values)
* **DISABLE_ASK_VERIFY_REQUESTS** (optional)
  * _True_ - Flask-Ask will not confirm the request originated from Amazon (allowing you to test from any system)
  * _False_ - [Default] all requests are checked to see if they originate from Amazon
* **REDIS_URL** (optional)
  * A Heroku-like URL to a Redis instance to use for Alexa session caching. 
  * *Note: Heroku-like means following the `redis://h:..` pattern. If you add a Redis add-on via Heroku, it should automatically set this environment variable on your dyno.*

## Application Design

The project is logically split out across a few modules:

* **webapp.py** - main web application logic, including Alexa Skills Kit intent handling
* **programs.py** - VPR programming data model, integration to VPR's podcast site for lookups
* **wsgi.py** - WSGI setup for running in something like [gunicorn](https://gunicorn.org)

## Contributing

The project is built to work with both **Python 2.7** and **Python 3.6**. If you'd like to hack on the source code, it's recommended to use a Python virtual environment.

### Building the Project

1. Clone the project: `git clone https://github.com/.../vpr-alexa-skill`
2. Install dependencies: `pip install -r requirements.txt`
3. Verify you project through tests:
   a. Using tox: `tox`
   b. Using pytest directly: `pytest`
   
### Tests!

The project uses the [pytest](https://docs.pytest.org/en/latest/) framework, keeping testing simple and straightforward.

* Tests are located in [./tests](./tests)
* Sample Alexa JSON requests are available in [./tests/fixtures](./tests/fixtures)

