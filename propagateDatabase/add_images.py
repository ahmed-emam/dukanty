import requests
import os, sys
import json
#import Image
port = 80
url = 'http://104.236.115.239:'+str(port)+'/addimage/'


def main():
    print("Building Image archive")

    url = 'http://104.236.115.239:'+str(port)+'/getproducts/'
    headers = {'Authorization':'Token 4037c3f17e127f12e9be55592aa07e3765c08442'}
    response = requests.get(url, headers=headers)
    for obj in response.json():
        url = 'http://104.236.115.239:'+str(port)+'/addimage/'
        payload = {'product_id': obj['id']}
        files = {'file': open('Product Images/'+obj['name']+'.png', 'rb')}

        response = requests.post(url, data=payload, files=files)
        print("Requested: "+response.url)
        print(response.status_code)
        print(str(obj['id'])+"\t"+obj['name'])


    # for f in os.listdir('files'):
    #
    #     print response.status_code
    '''
    with open("list_images") as file:
        listOfProducts = file.readlines()
        # print (listOfProducts)
        for row in listOfProducts:
            row = row.strip().split()
            # print(row)
            payload = {'product_id': row[0] }
            #files = {'file': Image.open('files/'+row[1]+'.jpg')}
            files = {'file': open('files/'+row[1]+'.jpg', 'rb')}
            #response = requests.post(url, )
            response = requests.post(url, data=payload, files=files)
            print("Requested: "+response.url)
    #         print(request.status_code)
    #         print(request)
    '''
main()
