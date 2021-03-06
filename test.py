import requests 

BASE="http://127.0.0.1:5000/"

data=[{'name':'rk','likes':1000,'views':56},
{'name':'aru','likes':5000,'views':78},
{'name':'kar','likes':7000,'views':97}]

for i in range(len(data)):
	response=requests.put(BASE+f'video/{i}',data[i])
	print(response.json())

response=requests.get(BASE+'video/3')
print(response.json())