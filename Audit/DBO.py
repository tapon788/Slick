__author__ = 'Tapon'

from pymysql import *

import sqlite3


# select actDualRx1xCsfb,actCSFBRedir,if(actDualRx1xCsfb=0,'YES','NO') as col from lnbts having col = 'YES';
#
# select mrbts,case
# 					when mrbts>10000 and mrbts<20000 then 'DHK'
# 					when mrbts>20000 and mrbts<30000 then 'CTG'
# 					else 'SYL' end from lncel;
#

class DBCheck:
    def __init__(self, hostname, username, password, dbname):
        self.connection = connect(host=hostname,
                                  user=username,
                                  password=password,
                                  db=dbname,
                                  port=3306,
                                  cursorclass=cursors.DictCursor)
        self.cursor = self.connection.cursor()

    def get_result(self, tablename, profileDictionary):

        subquery = ''
        for key,val in profileDictionary.iteritems():
            val = '"'+val.replace('"', '\\"')+'"'
            subquery += key+',CASE '
            # Check in range
            if val.find('--') >= 0:
                subquery += 'WHEN '+key+'>='+val.split('--')[0]+' AND '+key+'<='+val.split('--')[-1]+' THEN "OK" ELSE "NOK" END AS '+key+'_comment, '

            # Check multiple OR
            elif val.find('|') >= 0:
                subquery+='WHEN '
                for v in val.split('|'):
                    subquery+= key+'='+v+' OR '
                subquery = subquery[:-4]+' THEN "OK" ELSE "NOK" END AS '+key+'_comment, '

            # Check 'NOT EQUAL TO'
            elif val.find('!')>=0:
                subquery += 'WHEN '+key+'!='+val.split('!')[-1]+' THEN "OK" ELSE "NOK" END AS '+key+'_comment, '

            # Check multiple 'NOT EQUAL TO'
            elif val.find('~')>=0:
                subquery+='WHEN '
                for v in val.split('~'):
                    subquery += key+'!='+v+' AND '
                subquery = subquery[:-5]+' THEN "OK" ELSE "NOK" END AS '+key+'_comment, '

            # Check 'EQUAL TO'
            else:
                subquery += 'WHEN '+key+'='+val+' THEN "OK" ELSE "NOK" END AS '+key+'_comment, '

        query = 'SELECT '+subquery[:-2]+' FROM '+tablename+';'
        print (query)
        self.cursor.execute(query)

        data = self.cursor.fetchall()
        return data


    def __del__(self):
        self.cursor.close()
        self.connection.close()


class DBCheckSqlite:
    def __init__(self, data_src):
        # self.connection = connect(host=hostname,
        #                           user=username,
        #                           password=password,
        #                           db=dbname,
        #                           port=3306,
        #                           cursorclass=cursors.DictCursor)
        self._datasource = data_src
        self.connection = sqlite3.connect(self._datasource)
        self.connection.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
        self.cursor = self.connection.cursor()

    def get_result(self, tablename, profileDictionary):

        subquery = ''
        for key,val in profileDictionary.items():
            val = val.replace('"', '\\"')
            subquery += key+',CASE '
            # Check in range
            if val.find('--') >= 0:
                subquery += 'WHEN CAST('+key+' AS INT) >='+val.split('--')[0]+' AND CAST('+key+' AS INT) <='+val.split('--')[-1]+' THEN "OK" ELSE "NOK" END AS '+key+'_comment, '

            # Check multiple OR
            elif val.find('|') >= 0:
                subquery+='WHEN '
                for v in val.split('|'):
                    subquery+= key+'="'+v+'" OR '
                subquery = subquery[:-4]+' THEN "OK" ELSE "NOK" END AS '+key+'_comment, '

            # Check 'NOT EQUAL TO'
            elif val.find('!')>=0:
                subquery += 'WHEN '+key+'!="'+val.split('!')[-1]+'" THEN "OK" ELSE "NOK" END AS '+key+'_comment, '

            # Check multiple 'NOT EQUAL TO'
            elif val.find('~')>=0:
                subquery+='WHEN '
                for v in val.split('~'):
                    subquery += key+'!='+v+' AND '
                subquery = subquery[:-5]+' THEN "OK" ELSE "NOK" END AS '+key+'_comment, '

            # Check 'EQUAL TO'
            else:
                subquery += 'WHEN '+key+'='+val+' THEN "OK" ELSE "NOK" END AS '+key+'_comment, '

        query = 'SELECT plmn,'+subquery[:-2]+' FROM '+tablename+';'
        print (query)
        print(self._datasource)
        self.cursor.execute(query)

        data = self.cursor.fetchall()
        #print(data)
        return data


    def __del__(self):
        self.cursor.close()
        self.connection.close()
