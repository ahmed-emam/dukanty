import requests
import os, sys, time

port = 8001


start = 1
end = 48
def main():
    # print("Building Image archive")
    # for f in os.listdir('files'):
    #
    #     print response.status_code
    url = 'http://104.236.115.239:'+str(port)+'/getimages/'
    listp = list(range(start, end))
    print(listp)
    payload = {'product_list': listp}
    print(payload)
    starttime = time.time()
    response = requests.post(url, data=payload)

   # print(response.text)
    fp = open("zippedFile.zip", "wb")
    fp.write(response.content) #r.text is the binary data for the PNG returned by that php script
    fp.close()
    endtime = time.time()

    print("Time taken %f" % (endtime-starttime))

    url = 'http://104.236.115.239:'+str(port)+'/getimage/'

    starttime = time.time()
    for i in range(start, end):
        response = requests.get(url+str(i)+"/")
        fp = open("downloadedFiles/"+str(i)+".png", "wb")
        fp.write(response.content) #r.text is the binary data for the PNG returned by that php script
        fp.close()

        # print(response.content)
        print("Requested: "+response.url)
      #  print(request.status_code)
        # print(request)
    endtime = time.time()
    print("Time taken %f" % (endtime-starttime))

main()
