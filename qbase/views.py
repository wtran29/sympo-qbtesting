from django.shortcuts import render
import requests
import xml.etree.ElementTree as ET
from django.conf import settings
from bs4 import BeautifulSoup as bs


# Create your views here.
def qbase_request(request):
    target_domain = settings.TARGET_DOMAIN
    username = settings.QB_USERNAME
    password = settings.QB_PASSWORD
    auth_req = requests.get('http://' + target_domain + '.quickbase.com/db/main?a=api_authenticate&username='
                            + username + '&password=' + password)
    auth_req.raise_for_status()
    root = ET.fromstring(auth_req.content)
    ticket = [child.text for child in root.iter('ticket')]
    table_name = settings.QB_TABLE_NAME
    app_token = settings.QB_APP_TOKEN
    getdb = requests.get('https://williamtran.quickbase.com/db/' + table_name + '?a=API_GetDBInfo&ticket=' + str(ticket[0])
                         + '&apptoken=' + app_token)
    getdb_data = ET.fromstring(getdb.content)

    db_data = [item.text for item in getdb_data.iter()]

    doquery = requests.get(
        'https://williamtran.quickbase.com/db/' + table_name + '?a=API_DoQuery&ticket=' + str(ticket[0])
        + '&apptoken=' + app_token)
    context = {
        'database': db_data
    }
    return render(request, 'qbase/index.html', context)

