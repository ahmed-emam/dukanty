import requests
port = 80
hostname = 'dukanty.com'
url = 'http://'+hostname+':'+str(port)+'/debug/addshop/'


def main():
    print("Propagating shops")
    with open("list_shops") as file:
        listOfShops = file.readlines()
        # print (listOfShops)
        for row in listOfShops:
            row = row.strip().split()
            print(row)
            payload = {'name': row[0], 'rating': row[1], 'lat': row[2], 'lon': row[3], 'distance': row[4]}
            headers={'Authorization':'Token 1445ff16e94bc86d037a4f9ad86fd89735be4a05'}
            request = requests.post(url, data=payload, headers=headers)
            print("Requested: "+request.url)
            print(request.status_code)
            print(request.content)


main()
