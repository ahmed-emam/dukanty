import requests
url = 'http://104.236.115.239:8001/debug/addproduct/'


def main():
    print("Propagating products")
    with open("list_products") as file:
        listOfProducts = file.readlines()
        # print (listOfProducts)
        for row in listOfProducts:
            row = row.strip().split()
            # print(row)
            payload = {'name': row[0], 'company': row[1], 'category': row[2], 'img': row[3]}
            request = requests.post(url, data=payload)
            print("Requested: "+request.url)
            print(request.status_code)
            print(request.json())

main()