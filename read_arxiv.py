
from dateutil.parser import parse

FILENAME = 'arxiv_july_trip'

def main():
    lines = []
    with open(FILENAME) as handle:
        lines = handle.readlines()

    entry_set = []
    abstract = False
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

        if line.startswith('Authors: '):
            entry['authors'] = line.strip()[9:]

        if line.startswith('\\\\ ( https:'):
            entry['url'] = line[5:line.index(' , ')]
            abstract = False
        
        if line.startswith('  '):
            abstract = True

        if abstract:
            if 'abstract' not in entry:
                entry['abstract'] = line.strip()
            else:
                entry['abstract'] += ' ' + line.strip()

    for entry in entry_set:
        entry['title'] = entry['title'].replace('"', '\'')
        entry['authors'] = entry['authors'].replace('"', '\'')
        entry['abstract'] = entry['abstract'].replace('"', '\'')

    with open('output_arxiv.csv', 'w') as handle:
        handle.write('Title,Authors,Month,Year,URL,Abstract\n')
        for entry in entry_set:
            handle.write('"' + entry['title'] + '","' + entry['authors'] + '",' + str(entry['month']) + ',' + str(entry['year']) + ',"' + entry['url'] + '","' + entry['abstract'] + '"\n')

if __name__ == '__main__':
    main()
