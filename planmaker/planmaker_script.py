import xlrd
from lxml import etree as ET
import sys,time,socket,os

class ReadInput:

    def __init__(self,in_filename, in_sheet_index):
        self.filename = in_filename[0]
        self.sheet_index = in_sheet_index
        self.param_range = 5
        self.param_value_st = 6
        self.param_name = []
        self.param_value = []
        self.data_array = []
        self.parameter_array = []
        #self.get_param_names()



    def get_param_names(self):
        wb = xlrd.open_workbook(self.filename)
        sh1 = wb.sheet_by_index(self.sheet_index)
        self.data_array = []
        self.parameter_array = []
        for rownum in range(1,sh1.nrows):
            data = []
            for i in sh1.row_values(rownum)[:self.param_range]:
                if str(i):
                    data.append(str(i).split('.')[0])
            self.data_array.append(data)
            data = []
            for i in sh1.row_values(rownum)[6:]:
                if str(i):
                    if len(str(i).split('.'))>2:
                        data.append(str(i))
                    else:
                        data.append(str(i).split('.')[0])
            self.parameter_array.append(data)
        return(self.data_array,self.parameter_array)


    def create_plan(self,update,progress,finished):
        self.sp = []
        localdistname = ''
        sp_cnt = 0
        raml = ET.Element("raml",version="2.0", xmlns="raml20.xsd")
        cmData = ET.SubElement(raml,"cmData",type="plan", scope="all", name="Tapon_Paul")
        header = ET.SubElement(cmData,"header")
        log = ET.SubElement(header,"log", dateTime=time.ctime(), action="created", appInfo=socket.gethostname())
        
        param_names = self.data_array[0]
        param_values = self.data_array[1:]
        inp = list(zip(param_names, zip(*param_values)))
        print (inp)
        mo_class = inp[-1][0]
        cnt = 0
        for i in self.parameter_array[1:]:
            print (i)
            distname = 'PLMN-PLMN'
            for j in inp:
                #print j[-1],cnt
                distname = distname+'/'+j[0]+'-'+j[-1][cnt]
            cnt+=1
            print ('-- '+distname)
            if 'sgwIpAddressList>sgwIpAddress' not in self.parameter_array[0]:

                mo = ET.SubElement(cmData,"managedObject")
                mo.set("class", mo_class)
                mo.set("distName", distname)
                mo.set("operation", "update")

                c = 0
                list_flag = True

                for pname in self.parameter_array[0]:

                    if pname.find('>')>=0 and list_flag:
                        list_flag = False
                        print ('Hierarchy')
                        a_list = ET.SubElement(mo,"list")

                        a_list.set("name",pname.split('>')[0].strip())
                        item = ET.SubElement(a_list,"item")

                    elif pname.find('delete')>=0:
                        mo.set("operation", "delete")

                        print ('-'*50)
                        continue
                    else:

                        if list_flag:

                            print ('No Hierarchy')
                            p = ET.SubElement(mo, "p")
                            print("{}, {}".format(list_flag,pname))
                            p.set("name", pname)



                    if not list_flag:
                        p = ET.SubElement(item,"p")
                        p.set("name", pname.split(">")[-1].strip())

                    p.text = self.parameter_array[cnt][c]
                    c+=1
            else:

                sp_cnt += 1

                if distname not in self.sp:

                    self.sp.append(distname)

                    mo = ET.SubElement(cmData,"managedObject")
                    mo.set("class", mo_class)
                    mo.set("distName", distname)
                    mo.set("operation", "update")
                    a_list = ET.SubElement(mo, "list")
                    a_list.set("name", str(self.parameter_array[0][0]).split('>')[0])
                    print ("list")

                item = ET.SubElement(a_list, "item")
                print ('*'*50)
                print (self.parameter_array,sp_cnt)
                p = ET.SubElement(item, "p")
                p.set("name", self.parameter_array[0][0].split('>')[1])
                p.text = self.parameter_array[sp_cnt][0]

                p = ET.SubElement(item, "p")
                p.set("name", self.parameter_array[0][1])
                p.text = self.parameter_array[sp_cnt][1]


                localdistname = distname

            

        tree = ET.ElementTree(raml)
        # x = ET.tostring(tree, pretty_print=True, xml_declaration=True, encoding="ISO-8859-1",doctype="<!DOCTYPE raml SYSTEM 'raml20.dtd'>")
        ET.indent(tree,space="     ")
        y = ET.tostring(raml).decode('utf-8')

        # y = x.decode('utf-8')
        update.emit(y)
        # #print(y)
        # path = '/'.join(self.filename.split('/')[:-1])+"/out_"+mo_class+".xml"
        # print(path)
        # fp = open(path,"wb+")
        # fp.write(x)
        # fp.close()
        # #a = showinfo("Info", "Plan Generated")
        # os.startfile(path)

