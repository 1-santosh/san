import requests


q = """
{ 
  website(url: "https://dzone.com/big-data-analytics-tutorials-tools-news") {
    title
    image
    description
  }
}
"""


resp = requests.post("http://localhost:5000/", params={'query': q})
print(resp.text)
