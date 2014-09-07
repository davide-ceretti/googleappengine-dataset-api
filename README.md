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
git clone git@github.com:davide-ceretti/googleappengine-dataset-api.git
./install.sh # It will download and extract Google App Engine Python SDK
```

Load data
---------

```
# In your Google App Engine console
from scripts import load_from_dataset; load_from_dataset()
```

Tests
-----

```
# In your activated virtualenv
pip install test_requirements.txt
run_tests.sh
coverage report
```

Run server
----------

```
./run.sh
# Open your browser at http://localhost:8080/
```
