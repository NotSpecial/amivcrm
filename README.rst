Connector to the AMIV SugarCRM
==============================

SugarCRM provides a SOAP and a REST api. At the time this tool was written
the REST api was unfortunately not available. Therefore SOAP is used.

The python library suds is used, more exactly the fork by
`jurko <https://bitbucket.org/jurko/suds>`_.

Installation
------------

TODO

Usage
-----

You will need a soap username and password. You can find them in the
`AMIV wiki <intern.amiv.ethz.ch/wiki/SugarCRM#SOAP>`_.

.. code-block:: python
	from amivcrm import AMIVCRM

	CRM = AMIVCRM(username, password)

	# Get Companies
	CRM.get('Accounts')

	# Select only certain fields
	# Filter and order with SQL statements
	CRM.get('Accounts',
	        # Only companies participating in job fair
	        query="accounts_cstm.messeteilnahme_c = 1",
	        # Order alphabetically
	        order_by="accounts.name",
	        # Return Name and ID only
	        select_fields=['name', 'id'])

	# Get a single company by id
	CRM.getentry('Accounts',
	             '505404b1-1851-1472-d63e-4d829377e30b',
	             # Optional: Limit the returned fields as well
	             select_fields=['name'])

	# Get a company only if  modified after given date
	id = '505404b1-1851-1472-d63e-4d829377e30b'
	date = '2016-03-20 08:05:39'
	# Be careful to use quotes in query
	query = ("accounts.id = '%s' and "
	         "accounts.date_modified >= '%s'" % (id, date))
	CRM.get('Accounts', query=query)