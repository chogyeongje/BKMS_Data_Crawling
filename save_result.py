import os
import pandas as pd

def make_save_directory():
    global scholars_dir, authors_dir, scholar_links_dir, author_links_dir
    
    current_path = os.getcwd()

    scholars_dir = f'{current_path}/scholars'

    if not os.path.exists(scholars_dir):
        os.makedirs(scholars_dir)

    authors_dir = f'{current_path}/authors'

    if not os.path.exists(authors_dir):
        os.makedirs(authors_dir)    

    scholar_links_dir = f'{current_path}/scholar_links'

    if not os.path.exists(scholar_links_dir):
        os.makedirs(scholar_links_dir)

    author_links_dir = f'{current_path}/author_links'

    if not os.path.exists(author_links_dir):
        os.makedirs(author_links_dir)

    return author_links_dir, scholar_links_dir, authors_dir, scholars_dir

def save_authors(gf, result):
    global authors_dir
    _save_result(gf, result, authors_dir)

def save_scholars(gf, result):
    global scholars_dir
    _save_result(gf, result, scholars_dir)

def save_author_links(gf, result):
    global author_links_dir
    _save_result(gf, result, author_links_dir)

def save_scholar_links(gf, result):
    global scholar_links_dir
    _save_result(gf, result, scholar_links_dir)

def _save_result(gf, result, path):
    start = gf.start
    
    end = start + len(result) - 1
    
    df = pd.DataFrame(result)
    df.to_csv(f'{path}/{start}_{end}.csv', index=False)
    print(f'save {path}/{start}_{end}.csv')

    gf.start = end + 1