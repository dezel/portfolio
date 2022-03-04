from asyncore import write
from datetime import date, datetime
from distutils.file_util import write_file
from pydoc import writedoc
from numpy import datetime64, dtype, float16
from pandas.core.tools import datetimes
import py_pdf_parser as pdf
from py_pdf_parser.loaders import load_file
import pandas as pd
import os
import re
from pymongo import MongoClient


def get_pdfs(folder):
    file_list = os.listdir(folder)
    pdfs = []
    for item in file_list:
        parts = item.split('.')
        extension = (parts[-1])
        if extension == 'pdf':
            pdfs.append(folder + item)
    #print(pdfs)
    return pdfs
#get_pdfs('w:\\')
def get_transactions(folder):
    #print(pdfs)
    pdfs = get_pdfs(folder=folder) 
    
    all_trans = []

    for pdf in pdfs:
        document = load_file(pdf)
        all_text = ''
        #reg_ex = '[\d]{2}:[\d]{2}:[\d]{2}[\s]{1,}[\d]{10}[\s]{2,}[\d]{8,}[\s]{1,}[\d]{1,}[\s]{1,} Cash (?:Withdrawal|Deposit) [\s]{15,}[\w]{7}[\s]{4,}[\d]{1,}[,]*[\d]*.*[\d]{2}'
        reg_ex = '[\d]{2}:[\d]{2}:[\d]{2}[\s]{1,}[\d]{10}[\s]{2,}[\d]{8,}[\s]{1,}[\d]{1,}[\s]{1,} (?:Sale|(?:Cash (?:Withdrawal|Deposit))) [\s]{15,}[\w]{7}[\s]{4,}[\d]{1,}[,]*[\d]*.*[\d]{2}'
        reg_ex2 = '[\d]{3,}'
        period = ''
        for element in document.elements:
            all_text += element.text()

        #all_text.write('alltext.txt')
        
        #txt_out = open('name.txt', 'w')
        

        all_text = all_text.replace('(cid:10)', '')
        # txt_out.write(all_text)
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
            
            #adjust for deposit transactions
            if len(x) == 9:
                x.insert(8, 0)
                #print(x)

            #print(x)

            #adjust for sale transactions
            if x[4] == 'Sale':
                x.insert(5,'')
                x.insert(8,0)
            
            trans_array.append(x)
            
        column_list = ['trans_time', 'merchant_usn', 'client_usn', 'period', 'transaction', 'type', 'wallet', 'amount','fee', 'trans_date']
        dtype={'merchant_usn': str, 'client_usn':str, 'period':str, 'wallet':str, 'amount':float,'fee':float, 'trans_date': datetime64}
        
        df = pd.DataFrame(trans_array, columns=column_list)
        #df['trans_type'] = [] 
        df['trans_type'] = df.transaction + ' ' + df.type
        #print(df.trans_type)
        df['trans_date'] = df.trans_date + ' ' + df.trans_time
        df = df.drop(columns=['trans_time', 'transaction', 'type'])
        print(df)
        df = df.astype(dtype)

        all_trans.append(df)

    all_trans_df = pd.concat(all_trans)
    return all_trans_df
#

#print(get_transactions(r'w:\\'))
def insert_transactions(transactions):
    client = MongoClient()
    ebanking_db = client['ebanking']
    ezwich_transactions = ebanking_db['ezwich_transactions']
    transactions = transactions.fillna(0)
    transactions_dict = transactions.to_dict("records")
    ezwich_transactions.insert_many(transactions_dict)
    print('data inserted successfully')
    return 
    


#trans_df = get_transactions(r'w:\\')
#insert_transactions(trans_df)
#print(trans_df.dtypes)
#print(trans_df)
#trans_df.to_csv('all_trans.csv')
