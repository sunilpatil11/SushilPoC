import requests

endpoint = 'https://pag-translator.cognitiveservices.azure.com/'
key =  '7b40139d7cd84aac815f2f9c3545b8ed'
path = 'translator/text/batch/v1.1/batches'
constructed_url = endpoint + path

sourceSASUrl = 'https://rg4seedevelopmentinprogr.blob.core.windows.net/pagsourcecontainer?sp=racwl&st=2023-06-07T11:06:13Z&se=2024-06-07T19:06:13Z&spr=https&sv=2022-11-02&sr=c&sig=tD0pdchDAtVqxLmHZBYJZyxYFQmabHVS3FFqHKZp6TE%3D'

targetSASUrl = 'https://rg4seedevelopmentinprogr.blob.core.windows.net/pag/Pag/destination-language/japan?sp=racwl&st=2023-06-07T11:03:28Z&se=2024-06-07T19:03:28Z&spr=https&sv=2022-11-02&sr=c&sig=EOl9Oiqp3J3vRXrhDd5WCIpVbjOzOLJBmvAlSK3g3ac%3D'

body= {
    "inputs": [
        {
            "source": {
                "sourceUrl": sourceSASUrl,
                "storageSource": "AzureBlob",
                "language": "ja"
            },
            "targets": [
                {
                    "targetUrl": targetSASUrl,
                    "storageSource": "AzureBlob",
                    "category": "general",
                    "language": "en"
                }
            ]
        }
    ]
}
headers = {
  'Ocp-Apim-Subscription-Key': key,
  'Content-Type': 'application/json',
}

response = requests.post(constructed_url, headers=headers, json=body)
response_headers = response.headers

print(f'response status code: {response.status_code}\nresponse status: {response.reason}\n\nresponse headers:\n')

for key, value in response_headers.items():
    print(key, ":", value)