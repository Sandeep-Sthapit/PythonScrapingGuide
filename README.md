# Scraping Guide for Python

Simple notes on Python Scraper using Beautiful Soup and Selenium. This will help newcomers get familiarized with scrapers. This provides an overview of techniques used in scrapers.

# READING Robots.txt

Robots.txt is a file used by websites to let bots or crawlers know how to crawl a site or index it, or let know if it can be crawled. It should be respected to avoid legal consequences. Be sure to check the robots.txt file and respect it if it exists. It is usually found in domain_name/robots.txt like [https://angel.co/robots.txt](https://angel.co/robots.txt)

Some websites might block your IP if you put too much load on their servers. In this case, you can use proxies or use a different IP using a VPN.

* Full Access:

User-agent: *

Disallow:

* Block all access:

User-agent: *

Disallow: /

* Partial access

User-agent: *

Disallow: /folder/

User-agent: *

Disallow: /file.html

Disallowing some file or folders to be touched.

* Crawl rate limiting

Crawl-delay: 7

Limiting crawlers from overwhelming serves. In this example, crawler can hit in every 7 seconds.

* Visit time

Visit-time: 0400-0845      

This tells the crawlers about the time of day when crawling is allowed. In this example, the site can be crawled between 04:00 and 08:45 UTC. 

* Request rate

Request-rate: 1/10

It does not encourage bots trying to fetch multiple pages simultaneously. 1/10 as the value means the site can be crawled 1 page at a time every 10 seconds.

# CONNECTING TO SITES

from urllib.request import urlopen

try:

html = urlopen("http://pythonscraping.com/pages/page1.html")

print(html.read())

except HTTPError as e:

print(e)

This code outputs the HTML file *page1.html* in *pythonscraing.com*. This code doesn’t go back and request all the images or media in the *page1.html* like a browser. It will only read the specific file we requested. If the page is not existent like we get 404 error or 403 forbidden error and so on, our crawler with stop with error code. We need to handle these exceptions so that our crawler can run smoothly.

[urllib](https://docs.python.org/3/library/urllib.html) is a standard Python library (meaning you don’t have to install anything extra to run this example) and contains functions for requesting data across the web, handling cookies, and even changing metadata such as headers and your user agent.

# BEAUTIFUL SOUP

Beautiful soup is a python library that is used to interpret HTML webpage and extract information from it. It converts webpages to beautiful soup object with the following structure:

html → <html><head>...</head><body>...</body></html>

head → <head><title>A Useful Page<title></head>

title → <title>A Useful Page</title>

body → <body><p>An Int...</p><div>Lorem ip...</div></body>

span → <span>An Interesting Text</span>

div → <div>Lorem Ipsum dolor...</div>

To use beautiful soup, we proceed like follows:

html = urlopen("http://www.pythonscraping.com/exercise1.html") 

bsObj = BeautifulSoup(html.read());

Here a webpage is loaded and converted to beautiful soup object. Now we have capabilities to access individual contents inside the page. Suppose if we are to extract the span text information, we can achieve this by using following code:

text = bsObj.span

It is important to know how the website is constructed to extract the required information. We can use advanced functions like find, findall, select, select_one, children, parent and pass various arguments to it so that we can filter elements using html attributes like class, ids, style and so on. Select and select_one are easier to use if we are familiar with CSS selectors, and find and findall are better to use for advanced filtering.

Sometimes, the element we are trying to access might not exist and we get None objects. Beautiful soup will throw an attribute error when we try to access the attribute of None objects. We can either check if an object is None or not or use exception to catch attribute error like follows:

link = bsObj.a

if link is not None:

url = link[‘href’]

try:

print(bsObj.a[‘href’]

except AttributeError:

print("This page is missing something")

It is better to read the [documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to know about all the functionalities provided by beautiful soup. We can access attributes like (myTag.attrs) or use lambda functions or regular expression for advanced searching.

# SELENIUM

Selenium is a Web Browser Automation Tool. It is primarily used for automating web applications for testing purpose but it is not limited to it. It can perform tasks such as clicking buttons, entering information in forms, or searching for specific information on the web pages. Because of these features, it can be used to scrape webpages as well.

To use selenium first we need to install Selenium. The instructions for installing Selenium can be found [here](https://selenium-python.readthedocs.io/installation.html). Along with Selenium we will need drivers like chrome driver or gecko driver and install necessary browsers like chrome or firefox to use it. You will have to configure environment variables as well.

Import necessary libraries as shown below to start crawling the websites.

from selenium import webdriver

from selenium.webdriver import ActionChains

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException, NoSuchElementException

To perform any task using Selenium, first, we need to load the webdriver. This webdriver is used to open the browser and allows us to interact with websites. ActionChains allows us to perform tasks such as clicking elements, entering keywords, scrolling and so on. WebDriverWait allows the user to wait for the browser to load all the contents. Some elements are loaded using javascript and will take some time to load. If we do not use WebDriverWait with a delay and use expected condition to look for element, instead try to locate such elements using find_element_by_id or similar functions then we might get errors like NoSuchElementException. While using the WebDriverWait, if the element does not load in the specified delay then we will get TimeoutException. Below is the example of using webdriver:

driver = webdriver.Chrome()

driver.get(URL)

try:

submit =  WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.ID, "submit-btn")))

except TimeoutException:

    print("Loading took too much time!")

link = driver.find_elements(By.XPATH, '//a’)

linkdata = link.get_attribute('href')

print(linkdata)

driver.close()

We can also use expected conditions to look out for other conditions like some text to be in an element, visibility of some element and many more which are listed here.

send_keys(‘keyword’) and click() can be used to fill up forms and click items. Similarly, clear() can be used to clear fields and submit() can be used to submit a form. More details on locating element can be found [here](https://selenium-python.readthedocs.io/locating-elements.html).

Additionally, Selenium also provides xpath to locate elements. xpath is a powerful tool, that can be used to find elements using attributes such as class, or even by the presence of text. xpath is a language for finding any element on the web page using XML path expression. We can locate any element from HTML DOM structure. Its basic syntax is as follows:

Xpath = //tagname[@attribute=’value’]

**// :**	Select current node.

**Tagname:** Tagname of the particular node.

**@:**	Select attribute.

**Attribute:**	Attribute name of the node.

**Value:**	Value of the attribute.

Here is the [link](https://www.guru99.com/xpath-selenium.html) for more information on xpaths in Selenium.

It is better to read the [documentation](https://selenium-python.readthedocs.io/getting-started.html) for more information as well.

# COMBINING SELENIUM AND BEAUTIFUL SOUP

Selenium being an automation system is capable of doing almost everything that Beautiful Soup can do and some more functions as well. Selenium can help us to get emails or data from websites which are displayed using JavaScript which Beautiful Soup cannot render. But, this added functionality adds complexity as well. Beautiful Soup is simpler and easier to use. So, we can combine both to get the best of both libraries.

The way I prefer is to have Selenium fully render the webpage that we will be scraping and save the HTML that contains the information we desire into some variable or file. After that, we can use Beautiful Soup to convert the HTML to Beautiful Soup object and extract the required information easily.

However one may argue that the use of Beautiful Soup in this manner is pointless, but I think its the matter of preference. If people find it easier to use Selenium, they can use it.

# MULTIPROCESSING TO SCRAPE FASTER

We will be using Pool and Manger from multiprocessing python library. Pool allows parallelization of the execution of a function across multiple input values. It distributes the input data across processes which results in data parallelism. 

Some sites have thousands of pages and scraping pages one by one requires a tremendous amount of time. To utilize the full network bandwidth and power of the processor, we can use multiprocessing to run our code parallelly across multiple processes. This significantly reduces the time required to scrape a webpage.

Multiprocessing in simple words requires two steps: Map and Reduce. Map refers to dividing the task among the various processes and then after each process completes the task, they need to be combined together. This combining process is known as reduce.

Manager is required to store the parallelly scraped data into a single container which can later be saved into a file. When we try to store the parallelly scraped data into a normal container, it is not propagated to other processes running in parallel and thus, our scraped data is lost. Manager has methods which provide access to creating special lists like Manager.list() in which, changes made in the list are propagated to all the processes and the all the data scraped parallelly are consistently stored in this list.

Note: Users may face issue using multiprocessing in Jupyter Notebook. It is better to use Pycharm or other IDEs. If it is required to use it in Jupyter Notebook, writing the multiprocessing function in a different file might solve the issue.

Sample code is available in fast-scrape.py file.

# GETTING DATA FROM TWITTER API

To use the Twitter APIs, users require a developer account in Twitter which has to be approved by Twitter. This process could take some time even weeks, therefore it is better to get a developer account as soon as possible.

There are several libraries in python that can provide access to twitter APIs. Some of the popular ones are [Tweepy](https://www.tweepy.org/) and [python-twitter](https://python-twitter.readthedocs.io/en/latest/). Tweepy has better documentation but due to unavaialbily of some functions, python-twitter was used. In the future when required to make a bot for twitter, Tweepy might prove better suited for the purpose. But at the moment, we are only downloading followers and followings from the twitter which can be bulk downloaded using python-twitter.

If you need to get the Twitter ID of the user, this [site](http://gettwitterid.com/) can be of help. Just enter the twitter username and it will provide the id of the user.

After creating a twitter developer account you will get consumer_key, consumer_secret, access_token and access_token_secret which will help you access the APIs.

Various functions such as GetFollowers() will return the follower of a twitter user. If you want to get followers in bulk, we can use GetFollowersPaged() which will return 200 users in a group. These methods use a cursor to point which followers to return. It allows to navigate between pages of followers or get next follower or previous followers. To get the first list or first follower, the value of next_cursor will be -1 which will be passed as a default argument to the GetFollowers() or GetFollowersPaged()function. After the last follower has been returned, the value of the next cursor will be 0 and program can be terminated.

Twitter has specific rate limits. You can only make a certain number of call in a specified period of time. Thus, it is required to have a delay in the code to avoid being throttled. It is better to check more about rate-limiting [here](https://developer.twitter.com/en/docs/basics/rate-limiting.html).

Also, it is useful to read about the APIs provided by twitter in its official [API reference](https://developer.twitter.com/en/docs/api-reference-index).

Sample Code is provided here in the twitter_followers.ipynb file.

# MISCELLANEOUS TIPS

Sometimes it is faster to use text editors like SublimeText and use regular expression to get required information rather than writing a scraping script to get the information. Whole texts from small single paged websites can be copied and important information can be extracted using regular expression in the text editor. Therefore, it is handy to have some knowledge on this subject.

Also, for some single paged websites, if the contents are rendered using javascript, it is much faster to just download the whole HTML, save it as file and read the file then use beautiful soup to extract information rather than using selenium to get the information.


