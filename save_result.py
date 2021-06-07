import os
import pandas as pd

def make_save_directory(start_page = 1):
    global result_directory, a_result_directory
    
    current_path = os.getcwd()

    result_directory = f'{current_path}/scholars_with_page_{start_page}'

    if not os.path.exists(result_directory):
        os.makedirs(result_directory)

    a_result_directory = f'{current_path}/authors_with_page_{start_page}'

    if not os.path.exists(a_result_directory):
        os.makedirs(a_result_directory)    

def save_result(gf, result):
    start = gf.start
    
    end = start + len(result) - 1
    
    df = pd.DataFrame(result)
    df.to_csv(f'{result_directory}/{start}_{end}.csv', index=False)
    print(f'save {result_directory}/{start}_{end}.csv')

    gf.start = end + 1


def save_author(gf, a_result):
    a_start = gf.a_start
    
    a_end = a_start + len(a_result) - 1
    
    df = pd.DataFrame(a_result)
    df.to_csv(f'{a_result_directory}/{a_start}_{a_end}.csv', index=False)
    print(f'save {a_result_directory}/{a_start}_{a_end}.csv')

    gf.a_start = a_end + 1