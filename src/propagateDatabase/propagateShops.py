import requests
port = 8000
url = 'http://localhost:'+str(port)+'/debug/addshop/'


def main():
    print("Propagating shops")
    with open("list_shops") as file:
        listOfShops = file.readlines()
        # print (listOfShops)
        for row in listOfShops:
            row = row.strip().split()
            print(row)
            payload = {'name': row[0], 'rating': row[1], 'lat': row[2], 'lon': row[3], 'distance': row[4]}
            request = requests.post(url, data=payload)
            print("Requested: "+request.url)
            print(request.status_code)
            print(request.content)


main()
