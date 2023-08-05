import os
import requests
from xml.etree import ElementTree as et

username = "knc6"
password = ""

web_info = {
    "base_url": "https://jarvis.nist.gov",
    "template_id": "5f626925ece4b00035e5277f",
}


web_info = {
    "base_url": "https://test-jarvis.nist.gov",
    "template_id": "5f624bc547d1ac011a224672",
}




def update_xml_for_pid(
    xml_file="JVASP-1002.xml",
    element="basic_info/main_relax_info/id",
    prefix="https://jarvis.nist.gov/pid/rest/local/jarvis",
    output="temp.xml",
):
    tree = et.parse(xml_file)
    old_val = tree.getroot().find("main_relax_info/id").text
    new_val = str(prefix) + str("/") + old_val
    tree.getroot().find("main_relax_info/id").text = new_val
    print("old_val", tree.getroot().find("main_relax_info/id").text)
    # tree.find('idinfo/timeperd/timeinfo/rngda).text = '1/1/2011'
    tree.write(output)


def upload_xml_file(
    base_url="",
    filename="JVASP-1002.xml",
    template_id="",
    update_for_pid=True,
    temp_filename="temp.xml",
):
    """Upload file using path of the file and schema/template id."""
    print("status: uploading data file...")
    if update_for_pid:
        print("Updating for PID")
        update_xml_for_pid(xml_file=filename, output=temp_filename)
        filename = temp_filename
    xml_file = open(filename, "rb")
    xml_content = xml_file.read()
    xml_content1 = update_xml_for_pid(xml_file=filename)

    xml_upload_url = "/rest/data/"
    turl = base_url + xml_upload_url
    base = os.path.basename(filename)
    print("Filename:" + base)
    print("Template_id:" + template_id)
    data = {
        "title": base,
        "template": template_id,
        "xml_content": xml_content,
    }
    response = requests.post(
        turl, data=data, verify=False, auth=(username, password)
    )
    out = response.json()
    # pprint.pprint(out)
    response_code = response.status_code
    # print ('code:',response_code, requests.codes.ok)
    if response_code == requests.codes.created:
        print("status: uploaded.")
        upload_id = out["id"]
        print("upload_id", upload_id)
    else:
        response.raise_for_status()
        pprint.pprint(out)
        raise Exception(
            "A problem occurred when uploading the schema (Error ",
            response_code,
            ")",
        )

    return upload_id


# update_xml_for_pid()
upload_xml_file(
    base_url=web_info["base_url"], template_id=web_info["template_id"]
)
