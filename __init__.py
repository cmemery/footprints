"""
Used to connect to BMC (Numara) Footprints SOAP API.

Usage:
    import footprints
    con = footprints.Connection('username', 'host.example.com', password='mypassword')
    issue = con.getIssue(1, 536354) # where 1 is the item definition id, and 536354 is the item id
    print issue
"""
import urllib, urllib2, getpass, requests
from xml.etree import ElementTree as ET
from zeep import Client
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth

class Connection(object):
    """
    Create a connection to a Footprints server's SOAP API.

    Expects a userid and fqdn to setup the connection.

    """
    def __init__(self, userid, webhost, password = None):
        if not password:
            self.pword = getpass.getpass()
        else:
            self.pword = password
        self.user = userid
        self.url = "https://{}/footprints/servicedesk/externalapisoap/ExternalApiServicePort?wsdl".format(webhost)
        self.client = Client(self.url,
                             transport=Transport(http_auth=HTTPBasicAuth(self.user, self.pword)))

    def getIssue(self, definition_id, issue_id):
        """
        Retrieve information about an issue from Footprints via a SOAP API call.

        """
        fields = ['Title', 'Updated On', 'Created On', 'Status','Email Address']
        def_id = definition_id
        item_id = issue_id
        res = self.client.service.getItemDetails({'_itemDefinitionId':def_id,'_itemId':item_id,'_fieldsToRetrieve':fields })
        #return res
        return self.extract_info(res)

    def extract_info(self, results):
        """
        """
        pretty_result = {}
        fields = ['Title', 'Updated On', 'Created On', 'Status','Email Address']
        for item in results['_itemFields']['itemFields']:
            print item
            try:
                label = item['fieldName']
                value = item['fieldValue']['value']
                if label in fields:
                    if (type(value) is list and len(value) == 1):
                        pretty_result[label] = value[0]
                    else:
                        pretty_result[label] = value
                else:
                    pass
            except TypeError:
                pass
        return pretty_result
