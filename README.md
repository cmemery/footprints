footprints
==========

Connect to Numara Footprints SOAP api using python

This is a pretty bare-bones module that should help you
at least get started if you're trying to work with the
BMC FootPrints service desk application API.

Version 2.0 works with FP v12.1. Use v1.0 for FP 11.

Version 2 adds a dependency on zeep, so I've added
a requirements file to install dependencies.

Quickstart
==============
Create a project directory, a virtualenv, and install deps

```
$mkdir fp_project
$cd fp_project
$virtualenv .
$source bin/activate
$git clone https://github.com/cmemery/footprints footprints
$pip install -r footprints/requirements.txt
$python

```

From python shell or your script, import footprints to use

```
>>>import footprints
>>>con = footprints.Connection('username','host_fqdn', password='12345')
# You will be prompted for password if omitted
>>>issue = con.getIssue('82001','154000')
>>>issue
{'Status': 'Resolved', 'Updated On': '2016-08-11T16:28:47', 'Email
Address': 'client@example.com', 'Title': 'Internet wont work',
'Created On': '2016-08-11T16:28:47', 'item_id': 154387L}
```
