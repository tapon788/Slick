import deputy.os_utility as myhelper
from xml.sax.handler import ContentHandler
from xml.sax import parse


""" Library Imports """
from sys import platform, path
import os
path.append(os.getcwd())
from prettytable import PrettyTable

import deputy.os_utility as myhelper

import time
import gzip
import sqlite3
import shutil


class Prepare:
    def __init__(self,BASE_DIR,ABS_PATH,src,mobj,size,mo_list,db_name,is_dir_parse,raw_xml_db_dir):
        
        self.src = src
        self.mobj = mobj
        self.size = size
        self.path = ABS_PATH
        self.base_dir = BASE_DIR
        self.separator = myhelper.get_path_seperator()
        self.mo_list_filter = mo_list
        self.db_name = db_name
        self.is_dir_parse = is_dir_parse
        self.raw_xml_db_dir = raw_xml_db_dir
        """ Prepare xml path """
        self.xml_file_path = BASE_DIR + self.separator + ABS_PATH
        myhelper.clean_dir(self.xml_file_path)

        """ Prepare csv path """
        csv_file_path = BASE_DIR + self.separator + 'Parsed'
        myhelper.clean_dir(csv_file_path)
        
    def clean_db(self,path):
        """ Cleans sqllite database by deleting from the directory """
        if os.path.exists(path):
            os.remove(path)

    def xml_mo_chunker(self,update,progress,finished):

        """
        This method splits one big xml file into smaller pieces of xml files. It accepts
        4 arguments, src, mobj, self.size and path. src = source file, mobj = managedObject,  
        self.size = how many managedObjects in source file  will be chunked together and 
        path = absulute directory name relative to current folder.
        """
        
        raw_xml_databases = [self.src]
        if self.is_dir_parse:
            
            raw_xml_databases = []
            for raw_db in os.listdir(self.base_dir+self.separator+self.raw_xml_db_dir):
                if raw_db.find('.xml.gz')>=0:
                    raw_xml_databases.append(self.raw_xml_db_dir+self.separator+raw_db)
        
        
        for source_file in raw_xml_databases:
            print (source_file)
            update.emit('('+time.ctime()+')')
            update.emit('\nFile spliting started. This may take several minutes. Please keep patience..\n')

            mo_chunk = list()
            file_cnt = 0
            is_mo = False

            progress_segment = 0
            with gzip.open(self.base_dir+self.separator+source_file, 'rb') as src_file:

                for line in src_file:
                    line = line.decode()
                    if line.find('<'+self.mobj+' ') >= 0:
                        is_mo = True

                    if line.find('</'+self.mobj+'>') >= 0:
                        file_cnt += 1
                        mo_chunk.append(line)
                        is_mo = False
                        if (file_cnt % self.size) == 0:
                            update.emit('    From '+source_file+': Making ' + str(int(file_cnt / self.size)) + '.xml')

                            with open(self.base_dir + self.separator + self.path + self.separator + str(int(file_cnt / self.size)) + '.xml', 'w+', encoding="utf-8") as fp:
                                fp.write('<raml version="2.0">\n')
                                for xml in mo_chunk:
                                    fp.write(xml)
                                fp.write('</raml>')
                                mo_chunk = list()
                    if is_mo:
                        mo_chunk.append(line)
            
            finished.emit()

            pt = time.ctime()
            update.emit('\n'+'('+pt+') File Parsing Started ...\n')

            """ Parsing goes here """
            parse_count = 0
            total_files = len(os.listdir(self.xml_file_path))
            progress_segment = 0
            d = dict()
            for xml_file in os.listdir(self.xml_file_path):
                parse_count += 1
                #update.emit('    ['+self.src+':'+'] '+str(parse_count)+' - Working With '+xml_file)
                
                Handler = ManagedObjectHandler(self.mo_list_filter,self.base_dir,d)
                parse(self.xml_file_path + self.separator + xml_file, Handler)
                d = Handler.dict_table_headers
                progress_segment = progress_segment+(100/total_files)
                progress.emit(progress_segment)
            # Keep Parse ending time
            progress.emit(100)
            
            pt = time.ctime()
            update.emit('\n'+'('+pt+') File Parsing Ended ...\n')
            """ SQL operation goes here """
            print(self.base_dir + self.separator + self.db_name + source_file.split('\\')[-1].split('.')[0]+'.sqlite')
            self.clean_db(self.base_dir + self.separator + self.db_name + source_file.split('\\')[-1].split('.')[0]+'.sqlite')
            self.create_tables(self.base_dir + self.separator + self.db_name + source_file.split('\\')[-1].split('.')[0]+'.sqlite', d)
            info = self.insert_data(self.base_dir + self.separator + self.db_name  + source_file.split('\\')[-1].split('.')[0]+'.sqlite',source_file,progress)

            """ Summary output """
            t = PrettyTable(['File','ManagedObject', 'Count'])
            for key, val in info.items():
                t.add_row([source_file,key,val])
            
            update.emit('\n['+source_file+'] Summary:\n' + str(t))


    def create_tables(self, path, d):
        """ This function creates table from the dictinary loaded during parsing. It stores 
        table name as key from the class attr of managedObject. This dictionary stores all 
        possible parameter names as a list throughout the parsing cycle. """
        print (path)
        conn = sqlite3.connect(path)
        cursor = conn.cursor()

        for key, val in d.items():
            if val:
                try:
                    if len(val) == 1:
                        q_create_table_1 = 'CREATE TABLE ' + key
                        q_create_table_2 = str(tuple(val)).replace(',', '') + ';'
                        cursor.execute(q_create_table_1 + q_create_table_2)
                        with open(self.base_dir + self.separator + 'Parsed'+self.separator + 'create_' + key, 'a+') \
                                    as wr_table:
                            wr_table.write(q_create_table_1 + q_create_table_2 + '\n')
                    else:
                        cursor.execute('CREATE TABLE ' + key + str(tuple(val)) + ';')
                except:
                    print("********" + key + "********")
        conn.commit()
        conn.close()



    def insert_data(self,path,source_file,progress):
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        count_total_object = 0
        object_info = dict()
        total_files = len(os.listdir(self.base_dir + self.separator + 'Parsed'))
        progress_segment = 0
        for f in os.listdir(self.base_dir + self.separator + 'Parsed'):
            progress_segment = progress_segment+(100/total_files)
            if not f.find('create_') >= 0:
                count_object = 0
                print("["+source_file+"] Inserting data for " + f)
                with open(self.base_dir + self.separator + 'Parsed'+ self.separator + f) as insert_q_file:
                    for line in insert_q_file.readlines():
                        count_object += 1
                        cursor.execute(line)
                object_info[f] = count_object
                count_total_object += count_object
                conn.commit()
            progress.emit(progress_segment)
        cursor.close()
        object_info['Total'] = count_total_object
        progress.emit(100)
        return object_info


class ManagedObjectHandler(ContentHandler):
    """
    XML parser 
    """
    in_headline = False

    def __init__(self,mo_list,base_dir,d):
        ContentHandler.__init__(self)
        self.dict_table_headers = d
        self.mo_list_filter = mo_list
        self.base_dir = base_dir
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

        #New
        self.version = str()

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
            if self.mo_list_filter:
                if self.class_name in self.mo_list_filter:
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
            
            #New
            self.version = Attributes.values()[(Attributes.keys().index('version'))]
            self.parameters.append('version')
            self.values.append(self.version)
            
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

    def write_parsed(self, paramters,values):
        separator = myhelper.get_path_seperator()
        print(self.base_dir + separator + 'Parsed' + separator + self.class_name)
        with open(self.base_dir + separator + 'Parsed' + separator + self.class_name,'a+') as wr:
            #print(self.class_name,paramters,values)

            wr.write('INSERT INTO '+self.class_name+'('+','.join(paramters)+
                     ') VALUES('+str(values)[1:-1]+');\n')
            if self.class_name in self.dict_table_headers.keys():
                for p in self.parameters:
                    if p not in self.dict_table_headers[self.class_name]:
                        self.dict_table_headers[self.class_name].append(p)

            else:
                self.dict_table_headers[self.class_name] = paramters


