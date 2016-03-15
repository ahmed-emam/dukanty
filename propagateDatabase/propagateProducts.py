import requests
port = 80
url = 'http://104.236.115.239:'+str(port)+'/debug/addproduct/'


def main():
    print("Propagating products")
    with open("Product List.csv") as file:
        listOfProducts = file.readlines()
        # print (listOfProducts)
        for row in listOfProducts:
            row = row.strip().split(',')
            print(row)
            category = 0
            if row[1] == 'Beverages':
                category = 1
            elif row[1] == 'Bakery':
                category = 2
            elif row[1] == 'Dairy':
                category = 3
            elif row[1] == 'Produce':
                category = 4

          #  print(row[0])
           # print(row[1])
            #print(row[2])
           # print(row[3])
           # print(row[4])
            payload = {'name': row[0], 'company': row[4], 'category': category, 'img': 'none'}
            request = requests.post(url, data=payload)
            print("Requested: "+request.url)
            print(request.status_code)
            print(request.json())

main()
