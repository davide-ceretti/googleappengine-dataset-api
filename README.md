googleappengine-dataset-api
===========================

> Provide a simple Python API to retrieve data from the provided data set. The users of this API need to be able to specify a range of timestamps and optionally name which columns they are interested in. The API should return the relevant data in a format you feel is appropriate.

The app is deployed on Google App Engine @ http://dataset-api.appspot.com

Some of the possible queries:
* http://dataset-api.appspot.com/
* http://dataset-api.appspot.com/?timestamp_lt=2013-07-22%2009:25:00.000072636
* http://dataset-api.appspot.com/?f=lowpx,closepx

Install
-------

```
# Install the Google App Engine Python SDK somewhere
wget https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.10.zip
unzip google_appengine_1.9.10.zip
rm google_appengine_1.9.10.zip
export PATH=$PATH:<path-to-google_appengine>

# Clone this repo
git clone git@github.com:davide-ceretti/googleappengine-dataset-api.git
```

Run server
----------

```
./run.sh
# Open your browser at http://localhost:8080/
```

Load data
---------

```
# In your Google App Engine console (http://localhost:8000/console)
from scripts import load_from_dataset; load_from_dataset()
```

Tests
-----

```
# In your activated virtualenv
pip install test_requirements.txt
coverage run test.py <path-to-google_appengine> tests
coverage report
```

