from scholarly import scholarly
import glob
import pandas as pd

for path in glob.glob('scholar_links' +  "/*.csv"):
    df = pd.read_csv(path)
    for title in df['title']:
        print(title)
        search_query = scholarly.search_pubs(title)
        scholarly.pprint(next(search_query))
        break
    break