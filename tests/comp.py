import sqlite3
import os



def compare(table, name1, name2):
    # table = 'lncel'
    # name1 = 'DHK_L0068_1'
    # name2 = 'DHK_L0065_2'
    conn = sqlite3.connect(os.getcwd()+'\\resources\\db\\parsed_sbts.sqlite')
    cursor = conn.cursor()
    cursor.execute('Select * from '+ table +' where plmn="'+name1+'";')
    header = list(map(lambda x: x[0], cursor.description))

    item1 = dict(zip(header,cursor.fetchone()))
    cursor.execute('Select * from ' + table + ' where plmn="'+name2+'";')

    item2 = dict(zip(header,cursor.fetchone()))
    cursor.close()
    conn.close()

    header  = (name1,'Parameter',name2,'Comparison')
    matched_list = []
    unmatched_list = []
    for key,val in item1.items():
        if item2[key] != val:
            unmatched_list.append((val,key,item2[key],'Not Aligned'))
            
        else:
            if val is None:
                continue
            matched_list.append((val,key,item2[key],'Aligned'))

    return (header,matched_list,unmatched_list)