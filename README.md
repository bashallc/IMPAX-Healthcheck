# IMPAX-Healthcheck
 Automated Tool to check and store healthcheck results for AGFA IMPAX 6.7

History:

Agfa Impax provides a healthcheck service to show to show the status and performance of the webservices. This is helpful but difficult to use as it requires users to manually check the url or login to the application. it also does not log this data no provide information about historical trends or baseline performance

Installation:

1. This was built in python 3.7
2. It requires a headless client to be installed to navigate to the page and extract the data (webdriver)
3. It stores the information to an SQL database (I use Postgres)

Running:

1. Enter your application server urls
2. Enter your IMPAX username and password to be passed to the healthcheck authentication page
3. Enter your SQL db, table, username and password to store the data.


Bugs:

1. We recently upgraded from 6.5.3 su4 to 6.7.su8 and found that some healthcheck webservices had been removed which changed the columns that were stored. This is writtern for version 6.7x