import requests
port = 80
url = 'http://104.236.115.239:'+str(port)+'/debug/inventory/'


def main():
    print("Propagating Inventory")
    with open("inventory") as file:
        listOfProducts = file.readlines()
        # print (listOfProducts)
        for row in listOfProducts:
            row = row.strip().split()
            # print(row)
            payload = {'shop_name': row[0], 'product_name': row[1], 'price': row[2], 'stock': row[3]}
            request = requests.post(url, data=payload)
            print("Requested: "+request.url)
            print(request.status_code)
            print(request)

main()