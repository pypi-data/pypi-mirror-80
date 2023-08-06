# Welcome to StackEdit!

Hi! I'm your first Markdown file in **StackEdit**. If you want to learn about StackEdit, you can read me. If you want to play with Markdown, you can edit me. Once you have finished with me, you can create new files by opening the **file explorer** on the left corner of the navigation bar.


```python
def  getAsyncRequests(urls,maxConnections,timeDelay,headers):
	startTime = time.time()
	pageCount = len(urls)
	print("Total web page count:", pageCount)
	responseSuccesCount = 0
	responseFailCount = 0
	responses = []

	for x in  range(0, pageCount+1, maxConnections):
	rs = (grequests.get(u, headers=headers, stream=False)

	for u in urls[x:x+maxConnections])
	time.sleep(timeDelay)

	responses.extend(grequests.map(rs))
	print(x, "Waiting")
	index = 0

	for response in responses:
	index += 1

	if  str(response) == "<Response [200]>":
	responseSuccesCount += 1
	else:
	responseFailCount += 1

	print("Succes: {} , Fail: {}".format(responseSuccesCount, responseFailCount))
	endTime = time.time()
	print("It took", endTime-startTime, "seconds to retrieve",pageCount,"webpages.")

return responses
```
