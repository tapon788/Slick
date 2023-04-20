__author__ = 'tapon'


import os,xlrd,xlwt,sys,time



class Read_XL:

    def __init__(self,filename,sheetname):
        self.input_file = filename
        self.sheetname = sheetname
        self.parameter_name = []
        self.parameter_value = []
        pass


    def read_excel(self):
        """


        :return:
        """
        wb = xlrd.open_workbook(self.input_file)
        sh1 = wb.sheet_by_name(self.sheetname)
        self.parameter_name =  sh1.row_values(0)

        #print self.parameter_name
        for i in range (1,sh1.nrows):
            self.parameter_value.append(sh1.row_values(i))
        return (self.parameter_name, self.parameter_value)


    '''
    def write_excel(self,filename,data):
        relation_cname = data[0]
        n_cmd = data[1]
        ext_controller = data[2]
        ext_cmd = data[3]

        for d in range(len(relation_cname)-len(ext_controller)):
            ext_controller.append('')
            ext_cmd.append('')

        fp = open(filename,"w+")
        fp.writelines("Cname_Neighbor_Add\tCMD_Neighbor_Add\tCname_External_Create\tCMD_External_Create\n")
        for i in range(len(relation_cname)):
            fp.writelines(relation_cname[i]+"\t"+n_cmd[i]+"\t"+ext_controller[i]+"\t"+ext_cmd[i]+"\n")
        fp.close()
    '''