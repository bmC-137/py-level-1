import requests
url = 'url'
data = {"name": filename}
files = {'file': open(full_file_path, 'rb')}
response = requests.post(url, data=data, files=files)
current_url = response.text
print(response.text)
