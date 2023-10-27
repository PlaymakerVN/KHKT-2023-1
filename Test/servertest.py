import requests
server="http://localhost:8080/post.php"
hosts_path="/home/playmakervn/Documents/GitHub/KHKT-2023-1/Test/untitled.txt"
r = requests.post(url=server,data={'text':'TESTING SERVER'})
r = requests.post(url=server,data={'text':'ip'})
a=r.text.split('\n')
for i in range(len(a)):
	print(a[i])
print(a[0])
print(a[1])


with open(hosts_path, 'r+') as file:
	content = file.read()
	for i in range(len(a)):
		file.write("Testing " + a[i] + "\n")
a=0
def test():
	b=a+1
	print(a)
test()
print(a)