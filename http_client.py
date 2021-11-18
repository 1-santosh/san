import requests


q = """
{"query":"{\n  TweetByUser(name:\"elonmusk\")\n  {\n    name\n    tweets{\n      id \n      name\n      text\n      createdAT\n    }  \n  }\n}\n\n"}"
"""


resp = requests.post("http://localhost:8080/graphql", data=q,headers = { 'Content-type': 'application/json' 'Accept: application/json' 'Connection: keep-alive' 'DNT: 1' 'Origin: file://' 'Accept-Encoding: gzip, deflate, br'})
print(resp.text)
