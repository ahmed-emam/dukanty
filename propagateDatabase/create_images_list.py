import requests
import os, sys

# port = 80
# url = 'http://104.236.115.239:'+str(port)+'/addimage/'
#
start = 99
end = 145
def main():
    # print("Building Image archive")
    # for f in os.listdir('files'):
    #
    #     print response.status_code
    list=os.system("ls files")


    with open("list_images","w") as file:
        index=0
        for i in range(start, end+1):
            print list[index]
            file.write("%d\t%s\n" % (i, list[i%int(start)]))
            index=index+1

        # listOfProducts = file.readlines()
        # # print (listOfProducts)
        # for row in listOfProducts:
        #     row = row.strip().split()
        #     # print(row)
        #     payload = {'product_id': row[0]}
        #     files = {'file': Image.open('files/'+row[1]+'.jpg')}
        #     #response = requests.post(url, )
        #     response = requests.post(url, data=payload, files=files)
        #     print("Requested: "+response.url)
    #         print(request.status_code)
    #         print(request)

main()
