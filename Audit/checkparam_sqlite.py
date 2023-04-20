__author__ = 'Tapon'

from DBO import DBCheck, DBCheckSqlite
from nokia_parse.Audit.read_xl_input import Read_XL
from XL import MakeExcelFile

if __name__ == '__main__':
    objectname = 'Parameter'

    input = Read_XL('C:\\Python27\\omcproject\\nokia_parse\\Audit\\profile\\AuditProfile.xlsx', objectname)
    input_data = input.read_excel()[1]
    parametername = []
    plannedvalue = []
    objectname = []
    print (input_data)
    for i in input_data:
        objectname.append(i[0])
        parametername.append(i[1])
        if str(i[-1]):
            if len(str(i[-1]).split('.')) > 2:
                plannedvalue.append(str(i[-1]))
            else:
                plannedvalue.append(str(i[-1]).split('.')[0])
    print (objectname)
    print (parametername)
    print (plannedvalue)
    objectDictionary = {}

    for i in objectname:
        if i not in objectDictionary.keys():
            p = []
            v = []
            index = 0
            for j in objectname:
                if j==i:
                    p.append(parametername[index])
                    v.append(plannedvalue[index])
                index+=1
            objectDictionary[i] = dict(zip(p, v))



    #dbOpeartions = DBCheck('10.10.9.150','tapon','tapon12345','huawei')
    dbOpeartions = DBCheckSqlite(r'C:\Python36\Scripts\python3env\Scripts\MyQt5\Slick\resources\db\nokia.db')
    abc = MakeExcelFile('C:\\Python27\\audit.xlsx')

    for key,val in objectDictionary.iteritems():
        dbfeedback = dbOpeartions.get_result(key, val)
        abc.createsheet(key,dbfeedback)

    abc.close()