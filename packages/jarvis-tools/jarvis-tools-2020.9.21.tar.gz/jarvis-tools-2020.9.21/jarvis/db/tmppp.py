import os, requests, pprint

print("status: uploading data file...")
filename = "JVASP-1004.xml"
template_id = "5f6909278c6d9e011c8cc8c9"
template_id = "5f68d3cd18df58014367a55f"
base_url = "http://test-jarvis.nist.gov"
username = "kamal"
password = "kamal123"
xml_file = open(filename, "rb")
xml_content = xml_file.read()

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
print("output")
pprint.pprint(out)
response_code = response.status_code
print("code:", response_code, requests.codes.ok)
if response_code == requests.codes.created:
    print("status: uploaded.")
    upload_id = out["id"]
    print("upload_id", upload_id)
