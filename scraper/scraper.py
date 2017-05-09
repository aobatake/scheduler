from lxml import html
import requests
import time
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
semester += time.strftime('-%m-%d-%H-%M', time.localtime())
db = client[semester]

# --- Get links of all department pages
semester_page = requests.get(root_url + semester_link[0].replace("./", ""))
tree = html.fromstring(semester_page.content)
department_links = tree.xpath("//div[@class='columns']/div/ul/li/a/@href")

department = tree.xpath("//div[@class='columns']/div/ul/li/a/text()")
department = map(lambda x: x[x.index('(') + 1: x.index(')')], department)

# -- Get CRN link inside the department page
i = 0
for department_page in department_links:
  collection = db[department[i]]
  
  classes_page = requests.get(root_url +  department_page.replace("./", ""))
  tree = html.fromstring(classes_page.content)
  crn_links = tree.xpath("//tr/td/a/@href")
  
  # --- Getting data from CRN pages
  for link in crn_links:
    class_dict = {}
    crn_page = requests.get(root_url + link.replace("./", ""))
    tree = html.fromstring(crn_page.content)
    j = 2
    while (j != 16):
      root = "//table[4]/tr[" + str(j) +"]/td"
      tds = tree.xpath(root + "/child::node()")
      tds_filter = filter(lambda x: x != '\n', tds)
      title = tds_filter[0]
      if 'CRN' in title:
        class_dict['CRN'] =  tree.xpath(root + '/b/text()')[0]
      elif 'Subject' in title:
        class_dict['Subject'] = tree.xpath(root + '/b/text()')[0]
      elif 'Course Number' in title:
        class_dict['Course_Number'] = tree.xpath(root + '/b/text()')[0]
      elif 'Course Title' in title:
        class_dict['Course_Title'] = tree.xpath(root + '/b/text()')[0]
      elif 'Credits' in title:
        class_dict['Credits'] = tree.xpath(root + '/b/text()')[0]
      elif 'Section' in title:
        class_dict['Section'] = tree.xpath(root + '/b/text()')[0]
      elif 'Gen. Ed/Focus' in title:
        abbr = tree.xpath(root + '/b/node()')
        if not abbr:
          class_dict['Focus'] = ''
        else:
          class_dict['Focus'] = tree.xpath(root + '/b/abbr/text()')[0]
      elif 'Instructor' in title:
        b = tree.xpath(root + '/b/node()')
        b_filter = filter(lambda x: x != '\n', b)
        if 'TBA' in b_filter[0]:
          class_dict['Instructor'] = b_filter[0]
        else:
          a = tree.xpath(root + '/b/a/child::node()')
          a = filter(lambda x: x != '\n', a)
          if not a:
            class_dict['Instructor'] = tree.xpath(root + '/b/text()')[0]
          else:
            class_dict['Instructor'] = tree.xpath(root + '/b/a/text()')[0]
      elif 'Meeting Times' in title:
        table = tree.xpath(root + '/table/tr/td/b/text()')
        table = filter(lambda x: x!= '\n', table)
        table = map(lambda x: x.strip("\n"), table)
        table = map(lambda x: x.strip(u'\xa0\n'), table)
        k = 0
        info_array = []
        info_dict = {}
        for data in table:
          if k == 0:
            info_dict['Days'] = data
          elif k == 1:
            info_dict['Time'] = data
          elif k == 3:
            info_dict['Room'] = data
            info_array.append(info_dict)
            info_dict = {}
            k = 0
          k += 1
        class_dict['info'] = info_array
      j += 1
    collection.insert_one(class_dict)
    print class_dict
  i += 1

