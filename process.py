from pandas import read_csv, ExcelWriter
import numpy, os
from random import randint
# leaf_rate = input('Enter Leaf Rate: ')
def generate_report(leaf_rate, folder ,filepath):
    leaf_rate = int(leaf_rate)
    # folder = os.path.join(app.config['UPLOAD_FOLDER'])
    output_file = os.path.join(folder, 'LeafPaymentReport' + str(randint(1,99)) + '.xlsx')

    df = read_csv(filepath, sep='|', names=['Serial No', 'Agent', 'Date', 'Weight', 'Grade'])
    # drop columns
    df = df.drop(columns=['Serial No', 'Date', 'Grade'])
    # group
    df = df.groupby(['Agent']).sum()
    print(df)
    compute_rate = lambda x: x * leaf_rate

    df['Payment Amt'] = df.apply(compute_rate)
    df.loc["Total"] = df.sum()

    # print(df)
    sheetname='Sheet1'
    writer = ExcelWriter(output_file, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheetname)  # send df to writer
    workbook  = writer.book
    worksheet = writer.sheets[sheetname]  # pull worksheet object
    worksheet.set_column('A:D', 40)  # set column width
    border_fmt = workbook.add_format({'bottom':1, 'top':1, 'left':1, 'right':1})
    writer.save()
    return output_file