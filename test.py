import requests

# Server host for app
BASE = 'http://127.0.0.1:5000/'

# HelloWorld Tests
'''
# GET requests
res = requests.get(BASE + "helloworld/mike")
res2 = requests.get(BASE + "helloworld/steve")
res3 = requests.post(BASE + "helloworld/dumb")

# Print HTTP response status codes
print(res)
print(res2)
print(res3)

# Print data response in JSON format
print(res.json())
print(res2.json())
print(res3.json())
'''
# Video Tests

# Data list to insert IF database.db is empty
data = [{"likes": 78, "name": "Joe", "views": 100000},
        {"likes": 1000, "name": "How to make a Video Database", "views": 800000},
        {"likes": 35, "name": "Michael", "views": 2000}
        ]
# PUT request tests
for i in range(len(data)):
    vres = requests.put(BASE + "video/" + str(i), data[i])
    print(vres.json())

input()
# GET request tests
vres = requests.get(BASE + "video/2")
print(vres.json())
vres = requests.get(BASE + "video/7")
print(vres.json())

# UPDATE request tests
response = requests.patch(BASE + "video/7", {"views": 99})
print(response.json())
response = requests.patch(BASE + "video/2", {"name": "Brand New Video!"})
print(response)
print(response.json())
response = requests.patch(BASE + "video/2", {"name": "Change it Back!", "likes": 9000})
print(response)
print(response.json())

# DELETE request tests
# for i in range(len(data)):
#   vres = requests.delete(BASE + "video/" + str(i))
#   print(response) 
