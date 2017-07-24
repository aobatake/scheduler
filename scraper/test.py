from lxml import html
import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

root_url = "https://www.sis.hawaii.edu/uhdad/"

# --- Get link of most recent semester and 
main_page = requests.get('https://www.sis.hawaii.edu/uhdad/avail.classes?i=MAN')
tree = html.fromstring(main_page.content)
semester_link = tree.xpath('//div/ul/li/a/@href')

# --- Get semester text and prep database
semester = tree.xpath('//div/ul/li/a/text()')[0]
semester = semester.lower().replace(" ", "-")
db = client[semester]

# --- Get links of all department pages
semester_page = requests.get(root_url + semester_link[0].replace("./", ""))
tree = html.fromstring(semester_page.content)
department_links = tree.xpath("//div[@class='columns']/div/ul/li/a/@href")

department = tree.xpath("//div[@class='columns']/div/ul/li/a/text()")
department = map(lambda x: x[x.index('(') + 1: x.index(')')], department)

# -- Get CRN link inside the department page
i = 44
collection = db[department[i]]
classes_page = requests.get(root_url +  department_links[i].replace("./", ""))
tree = html.fromstring(classes_page.content)
crn_links = tree.xpath("//tr/td/a/@href")

  # --- Getting data from CRN pages
for link in crn_links:
  crn_page = requests.get(root_url + link.replace("./", ""))
  tree = html.fromstring(crn_page.content)
  j = 2
  while (j != 16):
    root = "//table[4]/tr[" + str(j) +"]/td"
    tds = tree.xpath(root + "/child::node()")
    tds_filter = filter(lambda x: x != '\n', tds)
    title = tds_filter[0]
    if 'CRN' in title:
      print tree.xpath(root + '/b/text()')[0]
    elif 'Subject' in title:
      print tree.xpath(root + '/b/text()')[0]
    elif 'Course Number' in title:
      print tree.xpath(root + '/b/text()')[0]
    elif 'Course Title' in title:
      print tree.xpath(root + '/b/text()')[0]
    elif 'Credits' in title:
      print tree.xpath(root + '/b/text()')[0]
    elif 'Section' in title:
      print tree.xpath(root + '/b/text()')[0]
    elif 'Gen. Ed/Focus' in title:
      abbr = tree.xpath(root + '/b/node()')
      if not abbr:
        print ''
      else:
        print tree.xpath(root + '/b/abbr/text()')[0]
    elif 'Instructor' in title:
      b = tree.xpath(root + '/b/node()')
      b_filter = filter(lambda x: x != '\n', b)
      if 'TBA' in b_filter[0]:
        print b_filter[0]
      else:
        a = tree.xpath(root + '/b/a/child::node()')
        a = filter(lambda x: x != '\n', a)
        if not a:
          print tree.xpath(root + '/b/text()')[0]
        else:
          print tree.xpath(root + '/b/a/text()')[0]
    elif 'Meeting Times' in title:
      table = tree.xpath(root + '/table/tr/td/b/text()')
      table = filter(lambda x: x!= '\n', table)
      table = map(lambda x: x.strip("\n"), table)
      table = map(lambda x: x.strip(u'\xa0\n'), table)
      k = 0
      for data in table:
        k += 1
        if k == 1:
          print data
        elif k == 2:
          print data
        elif k == 4:
          print data
          k = 0
    j += 1
  print '\n'

