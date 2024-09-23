import requests

url = "http://example.com"
response = requests.get(url)

print("Status Code:", response.status_code)
print("Content:", response.text[:500])  # Print first 500 characters of the response
