import requests
url = 'http://104.236.115.239:8001/auth/register/'


def main():
    print("Propagating users")
    with open("list_users") as file:
        listOfShops = file.readlines()
        # print (listOfShops)
        for row in listOfShops:
            row = row.strip().split()
            # print(row)
            payload = {'email': row[0], 'phone_number': row[1], 'password': row[2]}
            request = requests.post(url, data=payload)
            print("Requested: "+request.url)
            print(request.status_code)
            print(request.json())

main()