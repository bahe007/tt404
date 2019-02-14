# tt404
## Abstract
tt404 is supposed to find broken links on a website by crawling through it. It's able to write the results into a csv-file, to make the findings easy to use and analyse. 
## Project Motivation
Most websites don't have a strict hierarchical navigation, instead there are links to other pages or even other websites within the article texts. This is especially critical, because it makes updating a website so difficult: If pages are moved to different urls, it can be quite hard to keep up with all the 404 errors. 

Links to websites maintained by other companies are even worse: These websites can be deleted, altered or whatsoever, without letting the websites that link to them know. 

## How It Works
Like stated at the beginning, tt404 is a simple web crawler crawling through a given website. To start it, you give a base URL where it should begin. It searches for all links on that page and visits the referred pages. If the status code is not 200, it saves the link as broken. If the referred website isn't the same top level domain as of the base URL, it just checks the directly linked site. If the referred website is the same top level domain, it visits all links on that page, too. 

If it has visited all sites it could find, it saves the results into a csv file. 

### Usage
You can run the script directly from the terminal via Python 3.

Valid arguments are: 
- ```base_url``` required, URL at which the crawler should start
- ```--output_csv``` optional, path for the output file, default: "tt404_analysis.csv"
- ```--politeness``` optional, time between two requests in seconds, default: 0.0s
- ```--ignore_urls``` optional, list of urls that should not be visited
- ```--ignore_html_classes``` optional, list of class names for HTML tags whose content shall be ignored (except on the base url)
- ```--ignore_html_ids``` optional, list of id names for HTML tags whose content shall be ignored (except on the base url)

Example: 
``` 
python tt404.py https://example.com --output_csv path_to_file.csv --politeness 5.0
```

### CSV Format
All csv files have the exact same format: The first line consists only of the given base URL. The second line shows what data is in each column and the following lines include the data. This should be a good trade-off between a human readable and a machine readable format. 

Example: 
```
https://example.com 
Origin, Label, Link, Status
https://example.com/origin, Button-Label, Referred URL, Returned Status Code
```

If there are child HTML tags in the ```<a>```-Tag, the "Label"-field for the specific link will be empty, otherwise it will display what the button says to help identify the error more easily. 

### Features
tt404 can ignore certain parts (e. g. footer or navigation) of all pages visited except on the base URL in order to prevent recognizing the same mistake on every page. To allow this, provide the ```class``` or ```id``` tag. 

It's also smart enough to recognize if a certain page has already been visited in order to be faster while crawling the website and prevent loops. 

A small neat features it the ability to choose politeness. You can set a minimum time that tt404 should wait between every url request. 

Last but not least, you can provide certain URLs that shouldn't be visited at all, for example if you have a calendar implementation that has a single web page for every month which would result in many unnecessary url calls. 

### Requirements 
- Python 3
- Beautiful Soup
- requests
- argparse
- time
- csv (which I may remove and use an own csv-implementation based on the basic ```open()``` command)

# License
[Fair Source License, version 0.9](https://fair.io/v0.9.txt)

Copyright © 2019 Bastian Heinlein (two things)

Licensor: Bastian Heinlein

Software: tt404 v1.0 

Use Limitation: 5 users

License Grant. Licensor hereby grants to each recipient of the Software (“you”) a non-exclusive, non-transferable, royalty-free and fully-paid-up license, under all of the Licensor’s copyright and patent rights, to use, copy, distribute, prepare derivative works of, publicly perform and display the Software, subject to the Use Limitation and the conditions set forth below.

Use Limitation. The license granted above allows use by up to the number of users per entity set forth above (the “Use Limitation”). For determining the number of users, “you” includes all affiliates, meaning legal entities controlling, controlled by, or under common control with you. If you exceed the Use Limitation, your use is subject to payment of Licensor’s then-current list price for licenses.

Conditions. Redistribution in source code or other forms must include a copy of this license document to be provided in a reasonable manner. Any redistribution of the Software is only allowed subject to this license.

Trademarks. This license does not grant you any right in the trademarks, service marks, brand names or logos of Licensor.

DISCLAIMER. THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OR CONDITION, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. LICENSORS HEREBY DISCLAIM ALL LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE.

Termination. If you violate the terms of this license, your rights will terminate automatically and will not be reinstated without the prior written consent of Licensor. Any such termination will not affect the right of others who may have received copies of the Software from you.