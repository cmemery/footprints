"""
Used to connect to BMC (Numara) Footprints SOAP API.

Usage:
    import footprints
    con = footprints.Connection('username', 'host.example.com', password='mypassword')
    issue = con.getIssue(1, 536354) # where 1 is the item definition id, and 536354 is the item id
    print issue
"""
import getpass
from zeep import Client
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth

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

    def getIssue(self, definition_id, item_num):
        """
        Retrieve information about an issue from Footprints via a SOAP API call.

        """
        if 'SR-' in item_num:
            pass
        else:
            item_num = 'SR-' + item_num
        def_id = definition_id
        id_res = self.client.service.getItemId({'_itemDefinitionId':def_id,'_itemNumber':item_num})
        res = self.client.service.getItemDetails({'_itemDefinitionId':def_id,'_itemId':id_res})
        return self.extract_info(res, id_res)

    def extract_info(self, results, item_id):
        """
        """
        pretty_result = {}
        fields = ['Title', 'Updated On', 'Created On', 'Status','Email Address']
        for item in results['_itemFields']['itemFields']:
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
        pretty_result['item_id'] = item_id
        return pretty_result
