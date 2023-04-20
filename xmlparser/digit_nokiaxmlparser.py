##!/usr/bin/python
# -*- coding:utf-8 -*-
"""
Nokia XML Parser
================
| script:           nokiaxmlparser.py
| Base class:       ContentHandler
| Inherited class:  ManagedObjectHandler
| custom methods:

* xml_mo_chunker    (To split big xml file into pieces)
* write_parsed      (To write parsed content into a sql like file)
* clean_db          (Clean database by delte/create)
* create_tables     (Create necessary table based on parsed content)
* insert_data       (To insert data from sql like file to sqlitedb)

Dependencies
--------------
os, time, xml.sax, gzip, platform, prettytable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

"""

__author__ = "Tapon Paul"

from xml.sax.handler import ContentHandler
from xml.sax import parse


def xml_mo_chunker(src, mobj, size, path):

    """
    This method splits one big xml file into smaller pieces of xml files. It accepts
    4 arguments, src, mobj, size and path. src = source file, mobj = managedObject,  
    size = how many managedObjects in source file  will be chunked together and 
    path = absulute directory name relative to current folder.
    """

    mo_chunk = list()
    file_cnt = 0
    is_mo = False
    

    with gzip.open(BASE_DIR+separator+src, 'rb') as src_file:
        for line in src_file:
            line = line.decode()
            if line.find('<'+mobj+' ') >= 0:
                is_mo = True

            if line.find('</'+mobj+'>') >= 0:
                file_cnt += 1
                mo_chunk.append(line)
                is_mo = False
                if (file_cnt % size) == 0:
                    print('Making ' + str(int(file_cnt / size)) + '.xml')
                    with open(BASE_DIR + separator + path + separator + str(int(file_cnt / size)) + '.xml', 'w+') as fp:
                        fp.write('<raml version="2.0">\n')
                        for xml in mo_chunk:
                            fp.write(xml)
                        fp.write('</raml>')
                        mo_chunk = list()
            if is_mo:
                mo_chunk.append(line)


class ManagedObjectHandler(ContentHandler):
    """
    XML parser 
    """
    in_headline = False

    def __init__(self):
        ContentHandler.__init__(self)
        self.is_list = False
        self.is_item = False
        self.isdata = str()
        self.class_name = str()
        self.class_address = str()
        self.mo_attrs = str()
        self.param_value = list()
        self.param_list = list()
        self.list_name = str()
        self.list_values = list()
        self.items = list()
        self.parameters = list()
        self.values = list()

    def startElement(self, name, Attributes):
        self.mo_attrs = Attributes.values()
        if name == 'list':
            self.is_list = True
            self.list_name = self.mo_attrs[0]
            self.list_values = list()

        if name == 'item':
            self.is_item = True
            self.items = []

        if name == 'managedObject':
            self.class_name = Attributes.values()[(Attributes.keys().index('class'))]
            self.in_headline = True
            if MO_LIST_FILTER:
                if self.class_name in MO_LIST_FILTER:
                    self.in_headline = True
                else:
                    self.in_headline = False

            self.parameters = list()
            self.values = list()
            self.class_address = str()
            self.isdata = ""
            self.class_name = Attributes.values()[(Attributes.keys().index('class'))]
            self.class_address = Attributes.values()[(Attributes.keys().index('distName'))]
            self.parameters.append('plmn')
            self.values.append(self.class_address)

            if len(self.values[0].split('/')) > 1:
                for p in self.values[0].split('/')[1:]:
                    self.parameters.append(p.split('-')[0])
                    self.values.append(p.split('-')[-1])

    def characters(self, string):
        if self.in_headline:
            string = string.rstrip()
            if(len(string)>0):
                self.isdata = self.isdata+string
            else:
                self.isdata = "";

    def endElement(self, name):
        if name == 'p':
            if self.is_item:
                self.items.append({self.mo_attrs[0]:self.isdata})
                return
            elif self.mo_attrs:
                self.parameters.append(self.mo_attrs[0])
                self.values.append(self.isdata)

            elif self.is_list:
                self.list_values.append(self.isdata)

        if name == 'list':
            if self.is_list:
                if self.items:
                    self.parameters.append(self.list_name)
                    self.values.append(str(self.items))
                else:
                    self.parameters.append(self.list_name)
                    self.values.append(str(self.list_values))
                self.is_list = False

        if name == 'item':
            if self.is_item:
                self.list_values.append(self.items)
                self.is_item = False

        if name == 'managedObject':
            if self.in_headline:
                self.in_headline = False
                self.write_parsed(self.parameters, self.values)

        if name == 'raml':
            pass

    def write_parsed(self,paramters,values):

        with open(BASE_DIR + separator + 'Parsed' + separator + self.class_name,'a+') as wr:
            #print(self.class_name,paramters,values)

            wr.write('INSERT INTO '+self.class_name+'('+','.join(paramters)+
                     ') VALUES('+str(values)[1:-1]+');\n')
            if self.class_name in dict_table_headers.keys():
                for p in self.parameters:
                    if p not in dict_table_headers[self.class_name]:
                        dict_table_headers[self.class_name].append(p)

            else:
                dict_table_headers[self.class_name] = paramters

def clean_db():
    """ Cleans sqllite database by deleting from the directory """
    if os.path.exists(BASE_DIR+separator+DB_NAME):
        os.remove(BASE_DIR+separator+DB_NAME)


def create_tables():
    """ This function creates table from the dictinary loaded during parsing. It stores 
    table name as key from the class attr of managedObject. This dictionary stores all 
    possible parameter names as a list throughout the parsing cycle. """

    conn = sqlite3.connect(BASE_DIR+separator+DB_NAME)
    cursor = conn.cursor()

    for key, val in dict_table_headers.items():
        if val:
            try:
                if len(val) == 1:
                    q_create_table_1 = 'CREATE TABLE ' + key
                    q_create_table_2 = str(tuple(val)).replace(',', '') + ';'
                    cursor.execute(q_create_table_1 + q_create_table_2)
                    with open(BASE_DIR + separator + 'Parsed'+separator + 'create_' + key, 'a+') \
                                as wr_table:
                        wr_table.write(q_create_table_1 + q_create_table_2 + '\n')
                else:
                    cursor.execute('CREATE TABLE ' + key + str(tuple(val)) + ';')
            except:
                print("********" + key + "********")
    conn.commit()
    conn.close()

def insert_data():
    conn = sqlite3.connect(BASE_DIR+separator+DB_NAME)
    cursor = conn.cursor()
    count_total_object = 0
    for f in os.listdir(BASE_DIR + separator + 'Parsed'):
        if not f.find('create_') >= 0:
            count_object = 0
            print("Working with " + f)
            with open(BASE_DIR + separator + 'Parsed'+ separator + f) as insert_q_file:
                for line in insert_q_file.readlines():
                    count_object += 1
                    cursor.execute(line)
            object_info[f] = count_object
            count_total_object += count_object
            conn.commit()
    cursor.close()
    object_info['Total'] = count_total_object


if __name__ == '__main__':
    
    """ Library Imports """
    from sys import platform
    from prettytable import PrettyTable
    import deputy.os_utility as myhelper
    import os
    import time
    import gzip
    import sqlite3
    import shutil
    
    """ Variable declarations """
    dict_table_headers = dict()
    object_info = dict()
    st = str()
    pt = str()
    et = str()
    separator = str()
    xml_file_path = str()
    csv_file_path = str()
    MO_LIST_FILTER = []
    MO_CHUNK_SIZE = 10000
    CRONPATH_WINDOWS = str()
    CRONPATH_LINUX = str()
    SOURCE_FILE = 'nokia.xml.gz'
    MO_NAME = 'managedObject'
    ABS_PATH = 'ToBeParsed'
    IS_ZIP_DB = False
    IS_WEEKLY_BAKUP = False
    
    # Keep process starting time
    st = time.ctime()

    separator = myhelper.get_path_seperator()
   
    """ Overwrites default configuration """
    from parse_conf import *
    
    """ Prepare xml path """
    xml_file_path = BASE_DIR + separator + ABS_PATH
    myhelper.clean_dir(xml_file_path)

    """ Chunks big xml into pieces """
    xml_mo_chunker(src=SOURCE_FILE, mobj=MO_NAME,
                   size=MO_CHUNK_SIZE, path=ABS_PATH)

    """ Prepare csv path """
    csv_file_path = BASE_DIR + separator + 'Parsed'
    myhelper.clean_dir(csv_file_path)

    """ Parsing goes here """
    parse_count = 0
    for xml_file in os.listdir(xml_file_path):
        parse_count += 1
        print('['+str(parse_count)+']Working With '+xml_file)
        parse(xml_file_path + separator + xml_file, ManagedObjectHandler())
    
    # Keep Parse ending time
    pt = time.ctime()

    """ SQL operation goes here """
    clean_db()
    create_tables()
    insert_data()

    """ Summary output """
    t = PrettyTable(['ManagedObject', 'Count'])
    for key, val in object_info.items():
        t.add_row([key,val])
    print('\nSummary:\n')
    print(t)
    
    if IS_ZIP_DB:
        with open(BASE_DIR+separator+DB_NAME, 'rb') as f_in, gzip.open(BASE_DIR+separator+DB_NAME+'.gz', 'wb') as f_out:
            f_out.writelines(f_in)
        print("DB ZIP DONE!")
        
        if IS_WEEKLY_BAKUP:
            myhelper.clean_dir(BASE_DIR+separator+'backup'+separator+time.strftime("%A"))
            shutil.copy2(BASE_DIR+separator+DB_NAME+'.gz', 
                        BASE_DIR+separator+'backup'+separator+time.strftime("%A")+separator+DB_NAME+'.gz')
            print("WEEKLY BACKUP("+time.strftime("%A")+") DONE!")
   
            os.system('tar -cvzf '+BASE_DIR+separator+time.strftime("%b-%U-%Y")+'.tar.gz '+BASE_DIR+separator+'backup/')
    # Keep end time
    et = time.ctime()

    #Final timing profile
    print("Timing Profile\n Start Time: {"+st+"}\n Parse Time: ("+pt+") \nEnd Time: {"+et+"}")
