Lookout
Backend Internship ­ Services / Security Homework

SETUP:

Prerequisites: 
•	virtualenv (sudo /usr/local/bin/pip install virtualenv)
•	pip (sudo easy_install pip)
•	Postgresql

In order to successfully run sitecheck.py, run following commands in command line:

		mkdir ~/temp
		cd ~/temp
		git clone https://github.com/alenakruchkova/Lookout.git
		cd Lookout

		virtualenv env
		source env/bin/activate
		pip install -r requirements.txt

INVOKING APP VIA COMMAND LINE: 

		ln -s sitecheck.py sitecheck
		chmod 755 sitecheck

Make sure that Postgresql is running

		createdb <your db name>

I am using argparse to create command line options. 
If either url or database link are missing it will print "error: too few arguments" and exit. 
Interval could be omitted in which case it will default to 60.	
	
		./sitecheck -u <your url> -d postgresql:///<your db name> -i [your interval in seconds, defaults to 60] &

Note: one can use any structure for the input url above(e.g. http://google.com, www.google.com, google.com)

The app will then create a table in your database, then using requests library retrieve the status code of your website, 
and finally record url, timestamp and http status code to specified database.
I am using status codes below in addition to the standard http status codes:

- 1000 - ConnectionError - site does not exist
- 1001 - url could result in a very large download
- 1002 – ReadTimeout – site is hanging
- 1111 – unexpected error – all other errors

You can run multiple jobs simultaneously and record results to multiple databases.

TO CHECK THAT THINGS WORKED:

		psql <your db name>
		SELECT * FROM records;

TROUBLESHOOTING:

1. psql not found on MacOS, make sure it's in path as so

		export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/Latest/bin
		
2. spaces in directories cause problems

SITES I USED TO TEST EDGE CASES:

Sites I used to test edge cases:

- http://jhkjhkhkj.com/    does not exist 
- http://www.tkoofn.com/   hangs
- http://my.xfinity.com/   results in large download

RESOURCES I USED:

- argparse docs
https://docs.python.org/3/library/argparse.html

- requests lib docs
http://docs.python-requests.org/en/master/

- best library to use for http requests with timeout, maximum size
http://stackoverflow.com/questions/23514256/http-request-with-timeout-maximum-size-and-connection-pooling

- reference Errors and Exceptions
https://docs.python.org/2/tutorial/errors.html
