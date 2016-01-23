import requests
url = 'http://104.236.115.239:8001/debug/createorder/'


def main():
    print("Propagating orders")
    with open("orders") as file:
        listOfProducts = file.readlines()
        # print (listOfProducts)
        for row in listOfProducts:
            row = row.strip().split()
            # print(row)
            payload = {'shop_name': row[0], 'email': row[1], 'product_name': row[2], 'product_quantity': row[3],
                       'product_price': row[4]}
            request = requests.post(url, data=payload)
            print("Requested: "+request.url)
            print(request.status_code)
            print(request.json())

main()