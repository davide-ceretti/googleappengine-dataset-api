The app is deployed on Google App Engine @ http://dataset-api.appspot.com

Try on your browser
http://dataset-api.appspot.com/
http://dataset-api.appspot.com/?timestamp_lt=2013-07-22%2009:25:00.000072636
http://dataset-api.appspot.com/?f=lowpx,closepx


Install
-------

git clone
./install.sh

Load data
---------

In the Google App Engine console:
from scripts import load_from_dataset; load_from_dataset()

Delete data
-----------

In the Google App Engine console:
from utils import delete_all; delete_all()

Tests
-----

(In your activated virtualenv)
pip install test_requirements.txt
run_tests.sh
coverage report

Run server
----------

./run.sh

Make queries
------------

curl http://localhost:8080/
curl http://localhost:8080?f=date,symbol

# Encode 2013-07-22 09:50:00.000091493
curl http://localhost:8080?timestamp_gt=2013-07-22%2009%3A50%3A00.000091493%0A

# Encode 2013-07-19 08:48:00.000187704
curl http://localhost:8080?timestamp_lt=2013-07-19%2008%3A48%3A00.000187704%0A
