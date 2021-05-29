import datetime
from random import randint
from pandas import read_csv, ExcelWriter

def get_date():
    x = datetime.datetime.now()
    return x.strftime('%d-%b-%Y')

def generate_report(leaf_rate, filepath):
    leaf_rate = float(leaf_rate)
    date_postfix = get_date()
    output_file = 'LeafPaymentReport_' + date_postfix + '.xlsx'

    df = read_csv(filepath, sep='|', names=['Serial No', 'Agent', 'Date', 'Weight', 'Grade'])
    # drop columns
    df = df.drop(columns=['Serial No', 'Date', 'Grade'])
    # group
    df = df.groupby(['Agent']).sum()
    print(df)
    compute_rate = lambda x: x * leaf_rate

    df['Payment Amt'] = df.apply(compute_rate)
    df.loc["Total"] = df.sum()

    sheetname='Sheet1'
    writer = ExcelWriter(output_file, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheetname)  # send df to writer
    workbook  = writer.book
    worksheet = writer.sheets[sheetname]  # pull worksheet object
    worksheet.set_column('A:D', 40)  # set column width
    border_fmt = workbook.add_format({'bottom':1, 'top':1, 'left':1, 'right':1})
    writer.save()
    return output_file