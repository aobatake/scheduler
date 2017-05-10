from lxml import html
import requests

# --- Input: Request Link
# --- Output: HTML Tree Element
def getHtmlTree(link):
  page = requests.get(link)
  return html.fromstring(page.content)

# --- Input: HTML Tree
# --- Output: Dictionary of Class Data
def createClassDictionary(tree):
  class_dict = {}
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
      # --- There can be multiple meeting times
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
  return class_dict

