import requests
import os, sys
from zipfile import ZipFile
port = 8001
url = 'http://104.236.115.239:'+str(port)+'/getimages/'
#
start = 99
end = 146
def main():
    # print("Building Image archive")
    # for f in os.listdir('files'):
    #
    #     print response.status_code
    listp = list(range(start, end))
    print(listp)
    # payload = {'product_list': listp}
    # print(payload)
    # response = requests.post(url, data=payload)

    with ZipFile("file.zip", 'w') as zippedFile:
        for i in listp:
                zippedFile.write("propagateDatabase/downloadedFiles/"+str(i)+".jpg")

    # print(response.text)
    # fp = open("propagateDatabase/downloadedFiles/zippedFile.zip", "wb")
    # fp.write(response.content) #r.text is the binary data for the PNG returned by that php script
    # fp.close()

    # with open("list_images","w") as file:
    #     for i in range(start, end+1):
    #
    #         payload = {'image_id': i}
    #         response = requests.get(url+str(i)+"/")
    #         fp = open("downloadedFiles/"+str(i)+".jpg", "wb")
    #         fp.write(response.content) #r.text is the binary data for the PNG returned by that php script
    #         fp.close()

          #  print(response.content)
        #     print("Requested: "+response.url)
    #         print(request.status_code)
    #         print(request)

main()
