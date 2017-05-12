"""
Connector to the AMIV SugarCRM
==============================

SugarCRM provides a SOAP and a REST api. At the time this tool was written
the REST api was unfortunately not available. Therefore SOAP is used.

The python library suds is used, more exactly the fork by
`jurko <https://bitbucket.org/jurko/suds>`.

Usage
-----

You will need a soap username and password. You can find them in the
`AMIV wiki <intern.amiv.ethz.ch/wiki/SugarCRM#SOAP>`.

.. code:: python
	CRM = AMIVCRMConnector(username, password)

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
"""
from contextlib import contextmanager
import html
from suds.client import Client as SOAPClient

URL = "https://people.ee.ethz.ch/~amivkt/crm/service/v2/soap.php?wsdl"
APPNAME = "AMIV Kontakt: Internal: Customer Relationship Management"

class AMIVCRM(object):
    """Connector providing easy access to entries and entry lists.

    Args:
        username (str): the soap username
        password (str): the soap password
        url (str): CRM url
        appname (str): the soap appname
    """
    def __init__(self, username, password, url=URL, appname=APPNAME):
        self.client = SOAPClient(url)
        self.appname = appname
        self.username = username
        self.password = password

    def get(self, module_name, query="", order_by="", select_fields=None):
        """Get list of module entries matching the query.

        Args:
            module_name (str): CRM module
            query (str): SQL query string
            order_by (str): SQL order by string
            select_fields (list): Fields the CRM should return

        Yields:
            dict: Parsed entry
        """
        with self._session() as session_id:
            response = self.client.service.get_entry_list(
                session=session_id,
                module_name=module_name,
                query=query,
                order_by=order_by,
                select_fields=select_fields,
                offset=0)

            for entry in response.entry_list:
                yield self._parse(entry)


    def getentry(self, module_name, entry_id, select_fields=None):
        """Get list of module entries matching the query.

        Args:
            id: Entry id
            module_name (str): crm module
            elect_fields (list): fields the crm should return

        Yields:
            dict: One entry after another
        """
        with self._session() as session_id:
            response = self.client.service.get_entry(
                id=entry_id,
                session=session_id,
                module_name=module_name,
                select_fields=select_fields)
        parsed = self._parse(response.entry_list[0])

        # If the entry doesn't exist, the response
        # contains the field 'deleted' set to '1'
        # regardless of selected fields in query
        if parsed.get('deleted') == '1':
            return None
        return parsed

    @contextmanager
    def _session(self):
        """Session context, yields the session id for requests."""
        # Login
        auth = {'user_name': self.username, 'password': self.password}
        session_id = self.client.service.login(auth, self.appname).id

        yield session_id

        # Logout
        self.client.service.logout(session_id)

    @staticmethod
    def _safe_str(item):
        """Escape strings from CRM.

        First of all if its a string it is actually a suds Text class.
        In some environments this seems not to play along well with unicode.
        (Although it is a subclass of str)
        Therefore explicitly cast it to a str and unescape html chars.

        Possible improvement: Check if soap returns anything else but strings.
        If not, the if statement might be removed.
        """
        if isinstance(item, str):
            return html.unescape(str(item))
        else:
            return item

    @staticmethod
    def _parse(entry):
        """Turn result object into dict."""
        return {item.name: AMIVCRM._safe_str(item.value)
                for item in entry.name_value_list}
