import requests, os
from os.path import expanduser
port = 80
url = 'http://104.236.115.239:'+str(port)+'/debug/inventory/'


home = expanduser("~")

products_list = dict()
categories = ['canned foods', 'chocolate', 'Health & Beauty', 'spices']

def import_from_dropbox():
    root_path = home+'/Dropbox/Dukanty/'
    for dirname, dirnames, filenames in os.walk(root_path+'for_server/'):
        for subdirname in dirnames:
            #print(subdirname)
            #print(os.path.join(dirname, subdirname))
            for subdirpath ,subsubdirnames, subfilenames in os.walk(os.path.join(dirname, subdirname)):
                for filename in subfilenames:
                    #print(filename.split(".")[0])
                    products_list[filename.split(".")[0]] = subdirname

    with open(root_path+"/focus_data/products_list.csv") as list:
        listOfProducts = list.readlines()
        for row in listOfProducts:
            row = row.strip().split(";")
            if row[0] in products_list:
                # row.append(products_list[str(row[0])])
                # category_id = categories.index(row[3])
                # payload = {'barcode': row[0], 'name': row[1], 'company': row[1].split(' ')[0]}

                payload = {'shop_id': 13, 'product_id': row[0], 'price': row[2], 'stock': 1}
                print payload
                request = requests.post(url, data=payload)
                print("Requested: " + request.url)
                print(request.status_code)
                print(request.json())


def main():
    print("Propagating Inventory")
    with open("Product List.csv") as file:
        listOfProducts = file.readlines()
        # print (listOfProducts)
        for row in listOfProducts:
            row = row.strip().split(',')
            # print(row)
            if row[3] == '1':
                inStock = 'True'
            else:
                inStock = 'False'
            payload = {'shop_id': 13, 'product_name': row[0], 'price': row[2], 'stock': inStock}
            request = requests.post(url, data=payload)
            print("Requested: "+request.url)
            print(request.status_code)
            print(request)

import_from_dropbox()
