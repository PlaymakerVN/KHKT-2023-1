import requests
server="http://localhost:8080/post.php"
r = requests.post(url=server,data={'text':'TESTING SERVER'})
r = requests.post(url=server,data={'text':'ip'})
a=r.text.split('\n')

print(a[0])
print(a[1])