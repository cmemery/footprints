"""
Used to connect to BMC (Numara) Footprints SOAP API.

Usage:
    import footprints
    con = footprints.Connection('username', 'host.example.com', password='mypassword')
    issue = con.getIssue(1, 536354) # where 1 is the project id, and 536354 is the issue id
    print issue
"""
import urllib, urllib2, getpass
from xml.etree import ElementTree as ET

class Connection(object):
    """
    Create a connection to a Footprints server's SOAP API.

    Expects a userid and fqdn to setup the connection.

    """
    def __init__(self, userid, webhost, ssl=True, password = None):
        if not password:
            self.pword = getpass.getpass()
        else:
            self.pword = password
        self.user = userid
        if ssl:
            protocol = 'https'
        else:
            protocol = 'http'
        self.url = "%s://%s/MRcgi/MRWebServices.pl" % (protocol, webhost)

    def getIssue(self, project_id, issue_id):
        """
        Retrieve information about an issue from Footprints via a SOAP API call.

        Accepts two int arguments, projectid and issue_id.
        """
        #TODO: Move some of this boilerplate out of method for reuse in other API actions
        data = """
            <SOAP-ENV:Envelope 
              xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
              xmlns:namesp2="http://xml.apache.org/xml-soap" 
              xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
              xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/">
                <SOAP-ENV:Header/>
                <SOAP-ENV:Body> 
                    <namesp1:MRWebServices__getIssueDetails xmlns:namesp1="MRWebServices">
                        <user xsi:type="xsd:string">%s</user> 
                        <password xsi:type="xsd:string">%s</password> 
                        <extrainfo xsi:type="xsd:string"/> 
                        <projectnumber xsi:type="xsd:int">%d</projectnumber> 
                        <mrid xsi:type="xsd:int">%d</mrid> 
                    </namesp1:MRWebServices__getIssueDetails> 
                </SOAP-ENV:Body> 
            </SOAP-ENV:Envelope>
                        """ % (self.user, self.pword, project_id, issue_id)

        data8 = data.encode('utf-8')
        headers = {
           "SOAPAction" : "MRWebServices#MRWebServices__getIssueDetails",
           "Content-Type" : 'text/xml; charset=utf-8',
           "Content-Length" : "%d" % len(data8)
           }
        options = {
          "method" : "post",
        }
        req = urllib2.Request(self.url, data=data8, headers=headers)
        try: 
            resp = urllib2.urlopen(req)
            resp_xml = ET.fromstring(resp.read())
            top = resp_xml[0][0][0]
            issue = {}
            for item in top.getchildren():
                if item.text: 
                    issue[item.tag] = item.text
            issue['raw'] = top
            return issue
        except urllib2.HTTPError as e:
            return e.fp.readlines()

