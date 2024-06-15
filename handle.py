import pandas as pd
import json

def handle_person():
    df = pd.read_csv('person_list_210.csv')
    res = df.groupby(['person']).size().sort_values(ascending=False)
    res.to_csv('count.csv', encoding='utf_8_sig')



if __name__ == '__main__':
    handle_person()