import grequests
import time

def singleRequests(url):
    urls = [url]
    rs = (grequests.get(u, stream=False) for u in urls)
    response = grequests.map(rs)
    return response[0]

def getAsyncRequests(urls,maxConnections,timeDelay,headers):
    startTime = time.time()
    pageCount = len(urls)
    print("Total web page count:", pageCount)
    responseSuccesCount = 0
    responseFailCount = 0
    responses = []
    for x in range(0, pageCount+1, maxConnections):
        rs = (grequests.get(u, headers=headers, stream=False)
            for u in urls[x:x+maxConnections])
        time.sleep(timeDelay)
        responses.extend(grequests.map(rs))
        print(x, "Waiting")

    index = 0
    for response in responses:
        index += 1
        if str(response) == "<Response [200]>":
            responseSuccesCount += 1
        else:
            responseFailCount += 1
    print("Succes: {} , Fail: {}".format(responseSuccesCount, responseFailCount))
    endTime = time.time()
    print("It took", endTime-startTime, "seconds to retrieve",pageCount,"webpages.")
    return responses
