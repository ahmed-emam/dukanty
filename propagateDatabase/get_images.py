import requests
import os, sys

port = 8001
url = 'http://104.236.115.239:'+str(port)+'/getimages/'
#
start = 1
end = 40
def main():
    # print("Building Image archive")
    # for f in os.listdir('files'):
    #
    #     print response.status_code
    payload = {'product_list': range(start, end)}
    response = requests.post(url, data=payload)
    print(response)
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
