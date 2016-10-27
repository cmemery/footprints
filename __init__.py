"""
Used to connect to BMC (Numara) Footprints SOAP API.

Usage:
    import footprints
    con = footprints.Connection('username', 'host.example.com', password='mypassword')
    issue = con.getIssue('8001', '536354') # where 8001 is the item definition id, and 536354 is the itemnumber
    print issue
"""
import getpass
from zeep import Client
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
import datetime

class Connection(object):
    """
    Create a connection to a Footprints server's SOAP API.
    Expects a webhost, username, password, and fqdn to setup the connection.

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

    def getIssue(self, definition_id, item_num, terse=True):
        """
        Retrieve information about an issue from Footprints via a SOAP API call.
        Filters fields to basic info by default. To get all fields in response, pass 
        terse=False.
        """
        if 'SR-' in item_num: #Not sure if SR prefix is custom to our env, but it appears to be required
            pass
        else:
            item_num = 'SR-' + item_num
        def_id = definition_id
        #First call gets the issue id by  the issue number, which don't match for some reason
        id_res = self.client.service.getItemId({'_itemDefinitionId':def_id,'_itemNumber':item_num})
        res = self.client.service.getItemDetails({'_itemDefinitionId':def_id,'_itemId':id_res})
        if terse:
            return self.extract_info(res, id_res)
        else:
            return (res, id_res)

    def extract_info(self, results, item_id):
        """
        Limits fields included in output of FP call
        Use terse = False in getIssue to avoid this filter
        """
        pretty_result = {}
        fields = ['Title', 'Updated On', 'Created On', 'Status','Email Address']
        for item in results['_itemFields']['itemFields']:
            try:
                label = item['fieldName']
                value = item['fieldValue']['value']
                if label in fields:
                    if (type(value) is list and len(value) == 1):
                        value = value[0]
                    if label in ['Created On','Updated On']:
                        dateobject = datetime.datetime.strptime(value,'%Y-%m-%dT%H:%M:%S')
                        adjusteddate = dateobject+datetime.timedelta(hours=-4)
                        datestring = adjusteddate.strftime('%m/%d/%Y %I:%M%p')
                        pretty_result[label] = datestring
                    else:
                        pretty_result[label] = value
                else:
                    pass
            except TypeError:
                pass
        pretty_result['item_id'] = item_id
        return pretty_result
