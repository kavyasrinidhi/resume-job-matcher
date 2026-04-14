import requests

url = "http://127.0.0.1:5000/analyze"

data = {
    "resume_text": "Python Machine Learning Data Analysis",
    "jd_text": "Looking for Python ML skills"
}

response = requests.post(url, data=data)

print(response.status_code)
print(response.text)