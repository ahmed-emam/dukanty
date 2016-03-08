import requests
import os, sys
#import Image
port = 8001
url = 'http://104.236.115.239:'+str(port)+'/addimage/'


def main():
    print("Building Image archive")
    # for f in os.listdir('files'):
    #
    #     print response.status_code
    with open("list_images") as file:
        listOfProducts = file.readlines()
        # print (listOfProducts)
        for row in listOfProducts:
            row = row.strip().split()
            # print(row)
            payload = {'product_id': row[0]}
            #files = {'file': Image.open('files/'+row[1]+'.jpg')}
            files = {'file': open('files/'+row[1]+'.jpg', 'rb')}
            #response = requests.post(url, )
            response = requests.post(url, data=payload, files=files)
            print("Requested: "+response.url)
    #         print(request.status_code)
    #         print(request)

main()
