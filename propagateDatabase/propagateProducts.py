import requests
port = 80
url = 'http://104.236.115.239:'+str(port)+'/debug/addproduct/'


def main():
    print("Propagating products")
    with open("list_products") as file:
        listOfProducts = file.readlines()
        # print (listOfProducts)
        for row in listOfProducts:
            row = row.strip().split()
            # print(row)
            category = 0
            if row[1] == 'Beverages':
                category = 1
            elif row[1] == 'Bakery':
                category = 2
            elif row[1] == 'Dairy':
                category = 3
            elif row[1] == 'Produce':
                category = 4

            payload = {'name': row[0], 'company': row[1], 'category': category, 'img': row[3]}
            request = requests.post(url, data=payload)
            print("Requested: "+request.url)
            print(request.status_code)
            print(request.json())

main()