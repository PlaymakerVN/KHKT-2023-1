#Run in Root 
import os 
import time
import requests
import json
from datetime import datetime as dt
from browser_history import browsers, generic, utils 




# POST
def POST(type,content):
    r = requests.post(url=server,data={type:content})
    print("POST : "+content)
# GET HOST
def get_hosts_path():
    plat = utils.get_platform_name()
    #LOCATE HOSTS 
    if plat == "Windows":
        hosts_path = "C:\Windows\System32\drivers\etc\hosts"
    if plat == "Linux":
        hosts_path = "/etc/hosts"
    print("USING "+plat+" METHOD")
    return hosts_path
#GET IP
def get_ip():
    r = requests.post(url=server,data={'text':'blacklist'})
    getted_ip = r.text.split('\n')
    return getted_ip

#MAIN Function


def get_history():
    """This method is used to obtain browser histories of all available and
    supported browsers for the system platform.

    :return: Object of class :py:class:`browser_history.generic.Outputs` with
        the data member histories set to
        list(tuple(:py:class:`datetime.datetime`, str))

    :rtype: :py:class:`browser_history.generic.Outputs`
    """
    output_object = generic.Outputs(fetch_type="history")
    browser_classes = utils.get_browsers()
    for browser_class in browser_classes:
        try:
            browser_object = browser_class()
            browser_output_object = browser_object.fetch_history()
            output_object.histories.extend(browser_output_object.histories)
        except AssertionError:
            utils.logger.info("%s browser is not supported", browser_class.name)
    output_object.histories.sort()
    return output_object


def get_bookmarks():
    """This method is used to obtain browser bookmarks of all available and
    supported browsers for the system platform.

    :return: Object of class :py:class:`browser_history.generic.Outputs` with
        the data member bookmarks set to
        list(tuple(:py:class:`datetime.datetime`, str, str, str))

    :rtype: :py:class:`browser_history.generic.Outputs`
    """
    output_object = generic.Outputs(fetch_type="bookmarks")
    subclasses = utils.get_browsers()
    for browser_class in subclasses:
        try:
            browser_object = browser_class()
            assert (
                browser_object.bookmarks_file is not None
            ), f"Bookmarks are not supported on {browser_class.name}"
            browser_output_object = browser_object.fetch_bookmarks()
            output_object.bookmarks.extend(browser_output_object.bookmarks)
        except AssertionError as e:
            utils.logger.info("%s", e)
    output_object.bookmarks.sort()
    return output_object


#BLOCK

def block():
    r = requests.post(url=server,data={'text':'BLOCKED'})
    for i in range(len(website_list)):
        print("BLOCKED " + website_list[i])
        r = requests.post(url=server,data={'text':'IP BLOCKED: '+ website_list[i]})
    #READ FILE
    with open(hosts_path, 'r+') as file:
        content = file.read()
        for website in website_list:
            if website in content:
                pass
            else:
                # Apply to host
                file.write(redirect + " " + website + "\n")
                file.write(redirect + " " +"www."+ website + "\n")
    pass

#UNBLOCK
def unblock():
    r = requests.post(url=server,data={'text':'UNBLOCKED'})
    with open(hosts_path, "r+") as file:
        content = file.readlines()
        file.seek(0)
        for line in content:
            if not any(website in line for website in website_list):
                # Apply to host
                file.write(line)
                #POST
        file.truncate()
        print("Unblocked !!")
    pass
#SAVE URL HISTORY
def save_url_history():
    domain_connected = get_history()
    domain_connected.save("history_file", output_format="json")
    f = open('history_file')
    data = json.load(f)
    for i in data['history']:
        a = i['URL']
        print(a)


#MCORE PROGRAMME

# localhost's IP
redirect = "127.0.0.1"

#SERVER LOCATING
server_local="N"
if server_local == "y" or server_local == "Y":
    server="http://localhost/post.php"
if server_local == "n" or server_local == "N":
    server="https://khkt-lxt.000webhostapp.com/post.php"

# Websites block
website_ban = ["anonops.com"]
website_cloud = get_ip()
website_list = website_cloud+website_ban
for i in range(len(website_list)):
    print("LIST :" + website_list[i])


POST('text','BOT IS STARTED')
c = input("Y or N:")

hosts_path = get_hosts_path()
save_url_history()
while True:
    if(c == "y" or c == "Y"):
        block()
        break
    if (c == "n" or c =="N"):
        unblock()
        break

