import requests
port = 80
url = 'http://104.236.115.239:'+str(port)+'/debug/inventory/'


def main():
    print("Propagating Inventory")
    with open("Product List.csv") as file:
        listOfProducts = file.readlines()
        # print (listOfProducts)
        for row in listOfProducts:
            row = row.strip().split(',')
            # print(row)
            if row[3] == '1':
                inStock = 'True'
            else:
                inStock = 'False'
            payload = {'shop_name': 'shopter', 'product_name': row[0], 'price': row[2], 'stock': inStock}
            request = requests.post(url, data=payload)
            print("Requested: "+request.url)
            print(request.status_code)
            print(request)

main()
