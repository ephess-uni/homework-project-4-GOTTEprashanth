# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new_list=[]
    for d in old_dates:
        new_list.append(datetime.strptime(d, "%Y-%m-%d").strftime("%d %b %Y"))
    return new_list


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError
    elif not isinstance(start, str):
        raise TypeError
    else:
        lis=[]
        for i in range(0,n):
            lis.append(datetime.strptime(start,"%Y-%m-%d")  + timedelta(days=i))
        return lis


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    lis=[]
    z=0
    for i in values:
        telp_list=[]
        telp_list.append(datetime.strptime(start_date,"%Y-%m-%d")  + timedelta(days=z))
        telp_list.append(i) 
        lis.append(tuple(telp_list))
        z+=1
    return lis

            
def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    with open(infile) as f:
        li = []
        DictReader_obj = DictReader(f)
        for item in DictReader_obj:
            di = {}
            day1=datetime.strptime(item['date_returned'],'%m/%d/%Y')- datetime.strptime(item['date_due'],'%m/%d/%Y')
            if(day1.days>0):
                di["patron_id"]=item['patron_id']
                di["late_fees"]=round(day1.days*0.25, 2)
                li.append(di)
            else:
                di["patron_id"]=item['patron_id']
                di["late_fees"]=float(0)
                li.append(di)   
        aggregated_data = {}
        for dictionary in li:
            key = (dictionary['patron_id']) 
            aggregated_data[key] = aggregated_data.get(key, 0) + dictionary['late_fees']
        tax = [{'patron_id': key, 'late_fees': value} for key, value in aggregated_data.items()]
        for dict in tax:
            for k,v in dict.items():
                if k == "late_fees":
                    if len(str(v).split('.')[-1]) != 2:
                        dict[k] = str(v)+'0'
    with open(outfile,"w", newline="") as file:
        col = ['patron_id', 'late_fees']
        writer = DictWriter(file, fieldnames=col)
        writer.writeheader()
        writer.writerows(tax)
                


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
