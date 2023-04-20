import sqlite3

from models.models import *


class ConnectDB:
    def __init__(self, datasource):
        self._datasource = datasource
        self._conn = sqlite3.connect(self._datasource)
        self.cursor = self._conn.cursor()

    def getdata(self, colum, tablename, whereclause):
        if whereclause:
            query = 'SELECT '+colum+' from '+tablename+' WHERE '+whereclause+';'
        else:
            query = 'SELECT ' + colum + ' from ' + tablename +';'
        try:
            #print(query)
            self.cursor.execute(query)
        except sqlite3.OperationalError as err:
            return "SQL ERROR: "+str(err), None

        data = self.cursor.fetchall()
        list_data = []
        for i in data:
            list_data.append(list(i))
        #print (len(data))
        header = [description[0] for description in self.cursor.description]
        if data:
            return list_data, header


    def getDataFromQuery(self, q):
        query = q
        conn = sqlite3.connect(self._datasource)
        self.cursor = conn.cursor()
        try:
            self.cursor.execute(query)
        except sqlite3.OperationalError as err:
            return ("SQL ERROR: "+str(err), None)
        data = self.cursor.fetchall()

        header = [description[0] for description in self.cursor.description]

        if data:
            return data, header


    def getnodes(self, parent, child=None):
        rootnode = Node(parent, 'a')
        conn = sqlite3.connect(self._datasource)
        cursor = conn.cursor()
        # if parent == 'MRBTS':
        q = 'SELECT DISTINCT ' + parent + ',name FROM ' + parent + ' WHERE name IS NOT NULL;'
        #     print(q)
        # else:
        #     q = 'SELECT DISTINCT ' + parent + ',"" FROM ' + child + ';'
        try:
            cursor.execute(q)
        except sqlite3.OperationalError as err:
            #return "SQL ERROR: "+str(err), None
            return rootnode
        data = cursor.fetchall()
        header = [description[0] for description in cursor.description]
        d = {}
        
        for bsc in data:

            key = str(bsc[0])
            d[key] = Node(bsc[1], "PLMN-PLMN/"+parent+'-'+bsc[0].upper(), rootnode)
            q = 'SELECT plmn, ' + child + ',name from ' + child + ' where ' + parent + '="' + key + '";'
            if parent != "MRBTS":
                try:
                    cursor.execute(q)

                except sqlite3.OperationalError as err:
                    return ("SQL ERROR: " + str(err), None)

                data_bcf = cursor.fetchall()
                for bcf in data_bcf:
                    bcf_key = str(bcf[0])
                    d[bcf_key] = Node(
                        bcf[2].upper() + ' ' + child.upper() + '-' + bcf[1] if bcf[2] else child.upper() + '-' + bcf[1],bcf_key.upper(),
                        d[key])
        return rootnode


    def getnodesAll(self, clue):
        # clue = 'plmn-plmn/' + clue


        self.profile = []

        GSM_HIERARCHY = ['BSC', 'BCF', 'BTS', 'TRX']
        WCDMA_HIERARCHY = ['RNC', 'WBTS', 'WCEL', None]
        LTE_HIERARCHY = ['MRBTS', 'LNBTS', 'LNCEL', None]
        #print(clue)
        for i in GSM_HIERARCHY,WCDMA_HIERARCHY,LTE_HIERARCHY:
            for j in i:
                if j:
                    if clue.find(j)>=0:
                        self.profile = i
                        break
        # if self.profile == LTE_HIERARCHY:
        #     q = 'select distinct(substr(plmn,1,instr(plmn,\'' + self.profile[0] + '\')-2)),' + self.profile[0] + ' from ' + \
        #     self.profile[0] + ' where plmn ="' + clue.lower() + '";'
        # else:

        if self.profile == LTE_HIERARCHY:
            mrbts_id = clue.split('-')[-1]
            clue = clue+'/LNBTS-'+mrbts_id

        if len(clue.split('/'))<3:
            return None

        q = 'SELECT DISTINCT(SUBSTR(plmn,1,instr(plmn,\''+self.profile[1]+'\')-2)),'+self.profile[0]+' FROM '+\
            self.profile[1]+' WHERE plmn="'+clue+'";'

        #print (clue, q)

        self.cursor.execute(q)

        bsc_data = self.cursor.fetchall()
        if bsc_data:
            node_name = bsc_data[0][0]
            node_plmn = bsc_data[0][1]
        else:
            return None
        root = DetailNode('NODE', node_plmn, {}, 'XXX')

        bcf_node = self.nodeMaker(clue, self.profile[1], root)
        for bcf in bcf_node:
            if self.profile[2]:
                bts_nodes = self.nodeMaker(bcf[0], self.profile[2], bcf[1])
                if self.profile[3]:
                    for bts in bts_nodes:
                        trx_nodes = self.nodeMaker(bts[0], self.profile[3], bts[1])

        return root

    def nodeMaker(self, parent_plmn, current_object, parent_node):
        #print('-'*80)
        nodeinfo = []
        #print(current_object)

        if (current_object == 'bcf') or (current_object == 'bts') or (current_object == 'trx'):
            q1 = 'select plmn, name,'+current_object+',adminstate from '+current_object+' where plmn'

        elif(current_object == 'lncel'):
            q1 = 'select plmn, name,'+current_object+',administrativestate from '+current_object+' where plmn'

        else:
            q1 = 'select plmn, name,'+current_object+',"XXX" from '+current_object+' where plmn'


        if current_object == self.profile[1]:
            q = q1 + '="'+parent_plmn+'";'
        else:
            q = q1 + ' like "%'+parent_plmn+'/%";'
        #print(q)
        self.cursor.execute(q)
        data = self.cursor.fetchall()
        for result in data:
            q2 = 'select * from '+current_object+' where plmn="'+result[0]+'";'
            self.cursor.execute(q2)
            property_data = self.cursor.fetchall()
            header = [description[0] for description in self.cursor.description]
            for info in property_data:
                properties = dict(zip(header, info))

            p = DetailNode((current_object+'-'+result[2]).upper()+'    '+result[1].upper(),
                           result[0].upper(),
                           properties,
                           result[3],
                           parent_node)
            
            #print(properties)
            nodeinfo.append((result[0], p))
        return nodeinfo

    def getproperties(self, clue):
        table = clue.split('/')[-1].split('-')[0]
        q2 = 'select * from '+table+' where plmn="'+clue+'";'
        print(q2)
        print(self._datasource)
        self.cursor.execute(q2)
        property_data = self.cursor.fetchall()
        header = [description[0] for description in self.cursor.description]
        for info in property_data:
            properties = dict(zip(header, info))
        return properties

