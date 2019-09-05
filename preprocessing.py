import pandas as pd
import glob
import os.path
import re
import bs4

data_path = "../../data/job_board_data/"


def salary_from_string(s):
    subs = s.split('$')
    if len(subs) == 1:
        return None
    all_numbers = []
    for sub in subs[1:]:
        if(len(sub.strip())>0):
            sub = sub.replace('K', '000').strip()
            number = re.split('[ab /\-\+!]',sub)[0]
#             print(number)
            all_numbers.append(float(number.replace(',','')))
    return sum(all_numbers)/len(all_numbers)


def load_df():
    files = glob.glob(os.path.join(data_path, "*export*.jsl"))
    df = pd.read_json(files[0], lines=True)
    
    df['mean_salary'] = df['salary'].map(lambda x: salary_from_string(x['rangeText']) if not pd.isna(x) else None)
    ## some salaries are hourly
    df['mean_salary'] = df['mean_salary'].map(lambda x: x*40*50 if x<100 else x)
    
    df['industryName'] = df.companyInfo.map(lambda x: x['industryName'] if 'industryName' in x else "")
    
    return df



def clean_job_description(s):
    soup = bs4.BeautifulSoup(s, 'html.parser')
    return soup.text



def clean_all_job_descriptions(descriptions):
    pass

    
    
    
