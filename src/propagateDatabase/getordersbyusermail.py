import requests
url = 'http://104.236.115.239:8001/debug/getordersbyemail/'


def main():
    print("Getting list of orders for")
    with open("users_mail") as file:
        listOfProducts = file.readlines()
     # print (listOfProducts)
        for row in listOfProducts:
            row = row.strip().split()
            print("User: "+row[0])
            payload = {'email': row[0]}
            request = requests.post(url, data=payload)
            print("Requested: "+request.url)
            print(request.status_code)
            print(request.json())

main()