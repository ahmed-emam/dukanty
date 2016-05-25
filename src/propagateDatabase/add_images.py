import requests
import os, sys, os
from os.path import expanduser
import json
#import Image
port = 80
hostname = 'dukanty.com'
url = 'http://'+hostname+':'+str(port)+'/addimage/'



home = expanduser("~")

products_list = dict()
categories = ['canned foods', 'chocolate', 'Health & Beauty', 'Spices']

def import_from_dropbox():
    root_path = home+'/Dropbox/Dukanty/'
    for dirname, dirnames, filenames in os.walk(root_path+'for_server/'):
        for subdirname in dirnames:
            #print(subdirname)
            #print(os.path.join(dirname, subdirname))
            for subdirpath ,subsubdirnames, subfilenames in os.walk(os.path.join(dirname, subdirname)):
                for filename in subfilenames:
                    #print(filename.split(".")[0])
                    #print os.path.join(subdirpath, filename)
                    open(os.path.join(subdirpath, filename), 'rb')
                    #products_list[filename.split(".")[0]] = subdirname
                    payload = {'product_id': filename.split(".")[0]}
                    files = {'file': open(os.path.join(subdirpath, filename), 'rb')}
                    headers = {'Authorization': 'Token 1445ff16e94bc86d037a4f9ad86fd89735be4a05'}
                    response = requests.post(url, data=payload, files=files, headers=headers)
                    print("Requested: " + response.url)
                    print(response.status_code)
                    print(response)
    # with open(root_path+"/focus_data/products_list.csv") as list:
    #     listOfProducts = list.readlines()
    #     for row in listOfProducts:
    #         row = row.strip().split(";")
    #         if row[0] in products_list:
    #             row.append(products_list[str(row[0])])
    #             category_id = categories.index(row[3])
    #             payload = {'barcode': row[0], 'name': row[1], 'company': row[1].split(' ')[0], 'category': category_id}
    #             print payload
    #             request = requests.post(url, data=payload)
    #             print("Requested: " + request.url)
    #             print(request.status_code)
    #             print(request.json())
                #print row



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


import_from_dropbox()
