# --- PIP Modules
from pymongo import MongoClient

# --- Library and Custom Modules
import scraper
import time

print 'Conencting to Database'
client = MongoClient('localhost', 27017)

root_url = "https://www.sis.hawaii.edu/uhdad/"

# --- Get link of most recent semester and 
print 'Getting Most Recent Semester Link'
tree = scraper.getHtmlTree('https://www.sis.hawaii.edu/uhdad/avail.classes?i=MAN')
semester_link = tree.xpath('//div/ul/li/a/@href')

# --- Get semester text and prep database
semester = tree.xpath('//div/ul/li/a/text()')[0]
semester = semester.lower().replace(" ", "-")
print 'Creating Database Name'
# database name is the semester and current month, day, hour, minute
semester += time.strftime('-%m-%d-%H-%M', time.localtime())
print 'Database Name:', semester
db = client[semester]

# --- Get links of all department pages
print 'Getting Department Links'
tree = scraper.getHtmlTree(root_url + semester_link[0].replace("./", ""))
department_links = tree.xpath("//div[@class='columns']/div/ul/li/a/@href")

# --- Get Department Name
department = tree.xpath("//div[@class='columns']/div/ul/li/a/text()")
department = map(lambda x: x[x.index('(') + 1: x.index(')')], department)

# TODO: How can I make this more efficient?
# Takes 10 mins?
# -- Get CRN link inside the department page
i = 0
for department_page in department_links:
  print 'Scraping Department:', department[i]
  collection = db[department[i]]
  
  # --- Get each individual class page
  tree = scraper.getHtmlTree(root_url +  department_page.replace("./", ""))
  crn_links = tree.xpath("//tr/td/a/@href")
  
  # --- Getting data from CRN pages
  for link in crn_links:
    tree = scraper.getHtmlTree(root_url + link.replace("./", ""))
    class_dict = scraper.createClassDictionary(tree) 
    collection.insert_one(class_dict)
    #print class_dict
  i += 1

