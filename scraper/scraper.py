from lxml import html
import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

root_url = "https://www.sis.hawaii.edu/uhdad/"

main_page = requests.get('https://www.sis.hawaii.edu/uhdad/avail.classes?i=MAN')
tree = html.fromstring(main_page.content)
semester_link = tree.xpath('//div/ul/li/a/@href')
semester = tree.xpath('//div/ul/li/a/text()')[0]
semester = semester.lower().replace(" ", "-")
db = client[semester]

print semester
print(root_url + semester_link[0].replace("./", ""))

semester_page = requests.get(root_url + semester_link[0].replace("./", ""))
tree = html.fromstring(semester_page.content)
department_links = tree.xpath("//div[@class='columns']/div/ul/li/a/@href")

# TODO: Loop through all department links

classes_page = requests.get(root_url +  department_links[0].replace("./", ""))
tree = html.fromstring(classes_page.content)
crn_links = tree.xpath("//tr/td/a/@href")

for link in crn_links:
  crn_page = requests.get(root_url + link.replace("./", ""))
  tree = html.fromstring(crn_page.content)
  count = 2
  while (count != 16):
    root = "//table[4]/tr[" + str(count) +"]/td"
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
        print tree.xpath(root + '/b/a/text()')[0]
    elif 'Meeting Times' in title:
      table = tree.xpath(root + '/table/tr/td/b/text()')
      table = filter(lambda x: x!= '\n', table)
      table = map(lambda x: x.strip("\n"), table)
      table = map(lambda x: x.strip(u'\xa0\n'), table)
      for data in table:
        print data
    count += 1

