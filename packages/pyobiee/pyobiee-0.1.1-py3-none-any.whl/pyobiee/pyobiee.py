import re
import time
from zeep import Client
from requests import Session
from zeep.transports import Transport
import xml.etree.ElementTree as ET
from zeep.wsse.username import UsernameToken
import pandas as pd

QUERY_TIMEOUT = 20
RETRIES = 30

def downloadReport(wsdl_url, username, password, reportpath, executionOptions):
    # Initializing SOAP client, start a session
    session = Session(verify=True)
    transport = Transport(session=session)
    client = Client(wsdl=wsdl_url, wsse=UsernameToken(username, password), transport=transport)

    # getting session id
    session_id = client.service.logon(username, password)
    # bind to the XmlViewService
    xmlservice = client.bind('XmlViewService')

    # Retrieveing data schema and column headings
    max_retries = RETRIES
    while max_retries > 0:
        schema = xmlservice.executeXMLQuery(report=reportpath, outputFormat="SAWRowsetSchema", executionOptions=executionOptions, sessionID=session_id)
        if schema.rowset == None:
            max_retries -= 1
            continue
        else:
            time.sleep(QUERY_TIMEOUT)
            break
    
    if schema.rowset == None:
        client.service.logoff(sessionID=session_id)
        raise SAWRowsetSchemaError("Schema is blank, your query is wrong or execution time is too long")
    
    # parsing column headers
    headers = re.findall(r'columnHeading="(.*?)"', schema.rowset)
    dataset_dict = {}
    for header in headers:
        dataset_dict[header] = []
    

    # Making a query and parsing first fetch of data rows
    query_result = xmlservice.executeXMLQuery(report=reportpath, outputFormat="SAWRowsetData", executionOptions=executionOptions, sessionID=session_id)
    query_id = query_result.queryID

    if query_result.rowset == None:
        client.service.logoff(sessionID=session_id)
        raise SAWRowsetDataError('Data is blank, your query is wrong or execution time is too long')
    
    ETobject = ET.fromstring(query_result.rowset)
    rows = ETobject.findall('{urn:schemas-microsoft-com:xml-analysis:rowset}Row')
    
    for row in rows:
        for key in dataset_dict.keys():
            dataset_dict[key].append(row.find("{urn:schemas-microsoft-com:xml-analysis:rowset}Column" + 
                                             str(list(dataset_dict.keys()).index(key))).text)
    
    
    # Determine if additional fetching is needed and if yes - parsing additional rows   
    is_finished = query_result.finished
    while (not is_finished):
        query_fetch = xmlservice.fetchNext(queryID=query_id, sessionID=session_id)
        ETobject = ET.fromstring(query_fetch.rowset)
        rows = ETobject.findall('{urn:schemas-microsoft-com:xml-analysis:rowset}Row')

        for row in rows:
            for key in dataset_dict.keys():
                dataset_dict[key].append(row.find('{urn:schemas-microsoft-com:xml-analysis:rowset}Column' +
                                                 str(list(dataset_dict.keys()).index(key))).text)
        
        is_finished = query_fetch.finished
        
    # By some reason OBIEE doesn't make the last fetching, it will fix it
    is_finished = False
    while (not is_finished):
        query_fetch = xmlservice.fetchNext(queryID=query_id, sessionID=session_id)
        ETobject = ET.fromstring(query_fetch.rowset)
        rows = ETobject.findall('{urn:schemas-microsoft-com:xml-analysis:rowset}Row')
    
        for row in rows:
            for key in dataset_dict.keys():
                dataset_dict[key].append(row.find('{urn:schemas-microsoft-com:xml-analysis:rowset}Column' + 
                                                  str(list(dataset_dict.keys()).index(key))).text)
        is_finished = True
    
    client.service.logoff(sessionID=session_id)
        
    return pd.DataFrame(dataset_dict)


def executeSQL(wsdl_url, username, password, query, executionOptions):
    
    """
    The function sends a SQL query to OBIEE for execution and then downloads data, returns Pandas DataFrame
    """


    # Initializing SOAP client, start a session
    session = Session(verify=True)
    transport = Transport(session=session)
    client = Client(wsdl=wsdl_url, wsse=UsernameToken(username, password), transport=transport)

    # getting session id
    session_id = client.service.logon(username, password)
    # bind to the XmlViewService
    xmlservice = client.bind('XmlViewService')
    
    
    # Retrieveing data schema and column headings
    max_retries = RETRIES
    while max_retries > 0:
        schema = xmlservice.executeSQLQuery(sql=query, outputFormat="SAWRowsetSchema", executionOptions=executionOptions, sessionID=session_id)
        if schema.rowset == None:
            max_retries -= 1
            continue
        else:
            time.sleep(QUERY_TIMEOUT)
            break
    
    if schema.rowset == None:
        client.service.logoff(sessionID=session_id)
        raise SAWRowsetSchemaError("Schema is blank, your query is wrong or execution time is too long")
    
    # parsing column headers
    headers = re.findall(r'columnHeading="(.*?)"', schema.rowset)
    dataset_dict = {}
    for header in headers:
        dataset_dict[header] = []
    
    # Making a query and parsing first datarows
    query_result = xmlservice.executeSQLQuery(sql=query, outputFormat="SAWRowsetData", executionOptions=executionOptions, sessionID=session_id)
    query_id = query_result.queryID

    if query_result.rowset == None:
        client.service.logoff(sessionID=session_id)
        raise SAWRowsetDataError('Data is blank, your query is wrong or execution time is too long')

    ETobject = ET.fromstring(query_result.rowset)
    rows = ETobject.findall('{urn:schemas-microsoft-com:xml-analysis:rowset}Row')
    
    for row in rows:
        for key in dataset_dict.keys():
            rowdata = row.find("{urn:schemas-microsoft-com:xml-analysis:rowset}Column" + str(list(dataset_dict.keys()).index(key)))
            if rowdata != None:
                dataset_dict[key].append(rowdata.text)
            else:
                dataset_dict[key].append("")
    
    # Determine if additional fetching is needed and if yes - parsing additional rows   
    is_finished = query_result.finished
    
    while (not is_finished):
        query_fetch = xmlservice.fetchNext(queryID=query_id, sessionID=session_id)
        ETobject = ET.fromstring(query_fetch.rowset)
        rows = ETobject.findall('{urn:schemas-microsoft-com:xml-analysis:rowset}Row')

        for row in rows:
            for key in dataset_dict.keys():
                rowdata = row.find("{urn:schemas-microsoft-com:xml-analysis:rowset}Column" + str(list(dataset_dict.keys()).index(key)))
                if rowdata != None:
                    dataset_dict[key].append(rowdata.text)
                else:
                    dataset_dict[key].append("")
        
        is_finished = query_fetch.finished
    
    client.service.logoff(sessionID=session_id)
        
    return pd.DataFrame(dataset_dict)


# PyOBIEE Exceptions
class PyObieeError(Exception):
    """PyObieeError class"""
    pass


class SAWRowsetSchemaError(PyObieeError):
    def __init__(self, message):
        self.message = message


class SAWRowsetDataError(PyObieeError):
    def __init__(self, message):
        self.message = message