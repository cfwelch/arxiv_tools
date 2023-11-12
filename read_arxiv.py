
import os
from dateutil.parser import parse

EMAIL_FOLDER = 'emls'
DATE_DELIMITER = '   '

def main():
    file_list = [t for t in os.listdir(EMAIL_FOLDER) if t.endswith('.eml')]
    entry_set = []
    print(file_list)

    for file in file_list:
        entry_set.extend(parse_email(file))

    for entry in entry_set:
        entry['title'] = entry['title'].replace('"', '\'')
        entry['authors'] = entry['authors'].replace('"', '\'')
        entry['abstract'] = entry['abstract'].replace('"', '\'')

    with open('output_arxiv.csv', 'w') as handle:
        handle.write('Title,Author,Month,Year,URL,Abstract,First Pass\n')
        for entry in entry_set:
            handle.write('"' + entry['title'] + '","' + entry['authors'] + '",' + str(entry['month']) + ',' + str(entry['year']) + ',"' + entry['url'] + '","' + entry['abstract'] + '","No"\n')

def parse_email(filename):
    lines = []
    with open(EMAIL_FOLDER + '/' + filename) as handle:
        lines = handle.readlines()

    entry_set = []
    abstract = False
    title = False
    authors = False
    skip_entry = False
    entry = {}
    for line in lines:
        if line.startswith('-----------'):
            if len(entry) > 0 and not skip_entry:
                entry_set.append(entry)
                print(entry)
                entry = {}
                abstract = False

        if line.startswith('replaced with revised'):
            skip_entry = True

        if line.startswith('Date: '):
            if DATE_DELIMITER in line:
                ds = line[6:line.index(DATE_DELIMITER)]
                dt = parse(ds)
                # print(dt)
                entry['month'] = dt.month
                entry['year'] = dt.year
            else:
                print('Date is part of external data -- Skipping...')

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
            elif 'title' in entry: ### skips lines with spaces that are outside of an entry
                abstract = True

        if abstract:
            if 'abstract' not in entry:
                entry['abstract'] = line.strip()
            else:
                entry['abstract'] += ' ' + line.strip()

            # If there is \\, then we were actually in the comments section, so clear it and record from that point
            if line.startswith('\\\\'):
                del entry['abstract']

    return entry_set

if __name__ == '__main__':
    main()
