import xml.etree.ElementTree as et
import json
import gc

class AllEntities:
    def __getitem__(self, key):
        return ''

class Entry:
    data = {}
    def __init__(self):
        self.title = ''
        self.total_authors = 0
        self.author_names = []
        # self.data['journal'] = ''
        # self.data['url'] = ''
        # self.data['ee'] = ''
    def __repr__(self):
        data = {
                'title': self.title,
                'total_authors': self.total_authors,
                'author_names': self.author_names
            }
        return json.dumps(data)

    def __str__(self):
        data = {
                'title': self.title,
                'total_authors': self.total_authors,
                'author_names': self.author_names
            }
        return json.dumps(data, indent=4)

def garbageCollect():
    gc.collect()
    root.clear()

parser = et.XMLParser()
parser.parser.UseForeignDTD(True)
parser.entity = AllEntities()

isJournal = False
# journals = []
currentEntry = Entry()

context = et.iterparse('dblp.xml', parser=parser, events=("start", "end"))
context = iter(context)
event, root = context.next() #to clear root element

f = open('dblp_clean.txt', 'ab+')
f.write('[')
count = 0

# Reading dblp data and writing file on the fly along with
# garbage collecting so that I don't run out of memory
for event, elem in context:
    if elem.tag == 'article': # only parse lines that follow if it's a journal
        if event == 'start':
            currentEntry = Entry()
            isJournal = True
        else: # write to file when one journal entry is parsed
            currentEntry.total_authors = len(currentEntry.author_names)
            # journals.append(currentEntry)
            isJournal = False
            json.dump(json.loads(str(currentEntry)), f)
            f.write(',\n')

    if not isJournal: # skip all following lines if it's not a journal
        if count % 100 == 0:
            garbageCollect()
            print(count)

        count += 1
        continue

    if event == 'start': # parsing journals
        if elem.tag == 'author':
            currentEntry.author_names.append(elem.text)
        if elem.tag == 'title':
            currentEntry.title = elem.text

    if count % 100 == 0:
        garbageCollect()
        print(count)

    elem.clear()
    count += 1

f.write('{}]')
f.close()
