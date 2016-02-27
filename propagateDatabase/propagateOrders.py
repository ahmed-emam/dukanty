import requests
port = 80
url = 'http://104.236.115.239:'+str(port)+'/debug/createorder/'


def main():
    print("Propagating orders")
    with open("orders") as file:
        listOfProducts = file.readlines()[1:]
        # print (listOfProducts)
        for row in listOfProducts:

            row = row.strip().split()
            if len(row) < 13:
                shop_name, email, product_name, product_quantity, product_price, name, mobile, lat,\
                lon, street, building = row[0], row[1], row[2], row[3], row[4], row[5].replace(",", " "), row[6], row[7],\
                row[8], row[9], row[10]

                payload = {'shop_name': row[0], 'email': row[1], 'product_name': row[2], 'product_quantity': row[3],
                           'product_price': row[4], 'name': name, 'mobile': mobile, 'lat': lat, 'lon': lon,
                           'street': street, 'building': building}

            else:
                shop_name, email, product_name, product_quantity, product_price, name, mobile, lat,\
                lon, street, building, floor, apartment = row[0], row[1], row[2], row[3], row[4], row[5].replace(",", " ")\
                , row[6], row[7], row[8], row[9], row[10], row[11], row[12]

                payload = {'shop_name': row[0], 'email': row[1], 'product_name': row[2], 'product_quantity': row[3],
                           'product_price': row[4], 'name': name, 'mobile': mobile, 'lat': lat, 'lon': lon,
                           'street': street, 'building': building, 'floor': floor, 'apartment': apartment}

            request = requests.post(url, data=payload)
            print("Requested: "+request.url)
            print(request.status_code)
            print(request.json())

main()
