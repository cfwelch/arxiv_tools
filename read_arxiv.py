
from dateutil.parser import parse

FILENAME = 'test'

def main():
    lines = []
    with open(FILENAME) as handle:
        lines = handle.readlines()

    entry_set = []
    abstract = False
    title = False
    authors = False
    entry = {}
    for line in lines:
        if line.startswith('-----------'):
            if len(entry) > 0:
                entry_set.append(entry)
                print(entry)
                entry = {}
                abstract = False

        if line.startswith('Date: '):
            ds = line[6:line.index('   ')]
            dt = parse(ds)
            # print(dt)
            entry['month'] = dt.month
            entry['year'] = dt.year

        if line.startswith('Title: '):
            entry['title'] = line.strip()[7:]
            title = True

        if line.startswith('Authors: '):
            entry['authors'] = line.strip()[9:]
            title = False
            authors = True

        if line.startswith('Categories:'):
            authors = False

        if line.startswith('\\\\ ( https:'):
            entry['url'] = line[5:line.index(' , ')]
            abstract = False
        
        if line.startswith('  '):
            if title:
                entry['title'] += ' ' + line.strip()
            elif authors:
                entry['authors'] += ' ' + line.strip()
            else:
                abstract = True

        if abstract:
            if 'abstract' not in entry:
                entry['abstract'] = line.strip()
            else:
                entry['abstract'] += ' ' + line.strip()

            # If there is \\, then we were actually in the comments section, so clear it and record from that point
            if line.startswith('\\\\'):
                del entry['abstract']

    for entry in entry_set:
        entry['title'] = entry['title'].replace('"', '\'')
        entry['authors'] = entry['authors'].replace('"', '\'')
        entry['abstract'] = entry['abstract'].replace('"', '\'')

    with open('output_arxiv.csv', 'w') as handle:
        handle.write('Title,Authors,Month,Year,URL,Abstract,First Pass\n')
        for entry in entry_set:
            handle.write('"' + entry['title'] + '","' + entry['authors'] + '",' + str(entry['month']) + ',' + str(entry['year']) + ',"' + entry['url'] + '","' + entry['abstract'] + '","No"\n')

if __name__ == '__main__':
    main()
