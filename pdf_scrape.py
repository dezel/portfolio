from numpy import datetime64
from py_pdf_parser.loaders import load_file
import pandas as pd
import os
import re
from pymongo import MongoClient

#this method accepts a folder as an input parameter and scans through the folder to select only pdf files and return it as a list of files
def get_pdfs(folder):
    file_list = os.listdir(folder)
    pdfs = []
    for item in file_list:
        parts = item.split('.')
        extension = (parts[-1])
        if extension == 'pdf':
            pdfs.append(folder + item)
    return pdfs

#gets transactions from pdf based on the list of pdfs that was returned in get_pdfs
def get_transactions(folder):
    pdfs = get_pdfs(folder=folder) 
    all_trans = []
    for pdf in pdfs:
        document = load_file(pdf)
        all_text = ''
        #set a regular expression string for the transactions
        reg_ex = '[\d]{2}:[\d]{2}:[\d]{2}[\s]{1,}[\d]{10}[\s]{2,}[\d]{8,}[\s]{1,}[\d]{1,}[\s]{1,} (?:Withdrawal)))'
        for element in document.elements:
            all_text += element.text()

        all_text = all_text.replace('(cid:10)', '')
        date_match = re.findall('[\d]{4}-[\d]{1,}-[\d]{1,}', all_text)
        
        if date_match:
            trans_date = date_match[0]

        reg_result = re.findall( reg_ex, all_text)
        trans_array = []
        for x in reg_result:
            x = x.replace(',', '')
            x= x + ',' + trans_date
            x=re.sub('[\s]{1,}', ',',x)
            x=x.split(',')
                        
            trans_array.append(x)
            
        column_list = ['trans_time', 'merchant_usn', 'client_usn', 'period', 'transaction', 'type', 'wallet', 'amount','fee', 'trans_date']
        dtype={'merchant_usn': str, 'client_usn':str, 'period':str, 'wallet':str, 'amount':float,'fee':float, 'trans_date': datetime64}
        
        df = pd.DataFrame(trans_array, columns=column_list)
        df['trans_type'] = df.transaction + ' ' + df.type
        df['trans_date'] = df.trans_date + ' ' + df.trans_time
        df = df.drop(columns=['trans_time', 'transaction', 'type'])
        df = df.astype(dtype)

        all_trans.append(df)

    all_trans_df = pd.concat(all_trans)
    return all_trans_df


#save all the transactions into a mongo database
def insert_transactions(transactions):
    client = MongoClient()
    transactions_db = client['transactions']
    all_transactions = transactions_db['all_transactions']
    transactions = transactions.fillna(0)
    transactions_dict = transactions.to_dict("records")
    all_transactions.insert_many(transactions_dict)
    print('data inserted successfully')
    return 
    


