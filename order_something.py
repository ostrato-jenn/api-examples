import json
import urllib
import httplib2
import getpass
import pdb

def prettyPrint(sampleJson):
	jsonFormatted = json.loads(sampleJson)
	print json.dumps(jsonFormatted, indent=4, sort_keys=True)


# Login
user = raw_input("Username: ")
passwd = getpass.getpass("Password: ")


# Get Token
h = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
headers = {'Content-Type': 'application/json'}
body=''.join(['{"user":"',user,'","pass":"',passwd,'"}'])
resp, content = h.request("https://localhost/dashboard/auth", "POST", headers=headers, body=body)
jsonFormatted = json.loads(content)

token = jsonFormatted['token']
print "Got Token : ", token
headers['X-Auth-Token'] = token

# Set Group - the Demo group in our system is id 1001
# Notice I also change tokens after changing groups
resp, content = h.request("https://localhost/dashboard/auth?group=1001", "PUT", headers=headers)
jsonFormatted = json.loads(content)

token = jsonFormatted['token']
print "Changing to the Demo Group, switching Token To: ", token
headers['X-Auth-Token'] = token

# Get All Catalog Items for the Demo group
resp, content = h.request("https://localhost/dashboard/catalogs/products", "GET", headers=headers)
jsonFormatted = json.loads(content)

# Create our menu for selection
products = jsonFormatted['products']

# Create our menu for selection
productList = list()
i = 0

for key in products:
	productList.append( [ i,  key['id'], key['title'], key['price_lowest'] ] )
	i = i + 1

for i in productList:
	print i[0],")\t",i[2],"\t\t",i[3]

print
userSelection = raw_input("Please select the Composite You Wish To Order: ")
userSelection = int(userSelection)

# Add Product To Cart

selectedProduct = productList[userSelection]
print "Adding ",selectedProduct[2]," of id ",selectedProduct[1]," to cart...."
nameOfProduct = raw_input("Name Your Product: ")
uniqueKey = raw_input("Specify 1 unique key: ")
uniqueValue = raw_input("Specify key value: ")

body=''.join([ '{ "', str(selectedProduct[1]), '": [ { "quantity": 1, "name": "', nameOfProduct, '", "ssh_username": null, "tags": [{ "key": "', uniqueKey, '", "value":"', uniqueValue, '" }],"network_id":null,"firewall_id":null,"private_cloud_id":null,"subnet_id":null } ] }' ]) 

resp, content = h.request("https://localhost/dashboard/carts/products", "POST", headers=headers, body=body)
jsonFormatted = json.loads(content)

# Order All Products In Cart
resp, content = h.request("https://localhost/dashboard/orders", "POST", headers=headers)



