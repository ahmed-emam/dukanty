import requests, os
from os.path import expanduser
port = 8000
hostname = 'localhost'
url = 'http://'+hostname+':'+str(port)+'/debug/addproduct/'
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
                    products_list[filename.split(".")[0]] = subdirname

    with open(root_path+"/focus_data/products_list.csv") as list:
        listOfProducts = list.readlines()
        for row in listOfProducts:
            row = row.strip().split(";")
            if row[0] in products_list:
                row.append(products_list[str(row[0])])
                category_id = categories.index(row[3])
                payload = {'barcode': row[0], 'name': row[1], 'company': row[1].split(' ')[0], 'category': category_id}
                print payload
                request = requests.post(url, data=payload)
                print("Requested: " + request.url)
                print(request.status_code)
                print(request.json())
                #print row


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

import_from_dropbox()
