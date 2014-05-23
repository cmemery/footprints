import urllib, urllib2
import getpass
from xml.etree import ElementTree as ET

settings = {}
settings['userid'] = ''
settings['projectid'] = 0
settings['number'] = 0

class Connection(object):
    def __init__(self, user = settings['userid']):
        self.pword = getpass.getpass()
        self.user = user

    def getIssue(self, issue_number, projectid):
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
                        """ % (self.user, self.pword, projectid, issue_number)

        data8 = data.encode('utf-8')
        print data8
        headers = {
           "SOAPAction" : "MRWebServices#MRWebServices__getIssueDetails",
           "Content-Type" : 'text/xml; charset=utf-8',
           "Content-Length" : "%d" % len(data8)
           }
        options = {
          "method" : "post",
        }
        url = "https://support.cpcc.edu/MRcgi/MRWebServices.pl"
        req = urllib2.Request(url, data=data8, headers=headers)
        try: 
            resp = urllib2.urlopen(req)
            resp_xml = ET.fromstring(resp.read())
            top = resp_xml[0][0][0]
            issue = {}
            for item in top.getchildren():
                if item.text: 
                    issue[item.tag] = item.text
            return issue
        except urllib2.HTTPError as e:
            return e.fp.readlines()
