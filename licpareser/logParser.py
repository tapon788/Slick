######################################### LIC INFO ###############################################
lic_info_flag = 0
new_lic_flag = 0
all_lic_info = []
aLicInfo = []
get_bsc_flag = 0
bsc_cnum = '999999'
bsc_name = 'XXXXXX_X'

class ParseLog:

    def __init__(self):
        self.lic_info_flag = 0
        self.new_lic_flag = 0
        self.all_lic_info = []
        self.aLicInfo = []
        self.get_bsc_flag = 0
        self.bsc_cnum = '999999'
        self.bsc_name = 'XXXXXX_X'
        self.rnc_id = '999'
        self.lic_info_grep = []



    def grep(self,log,log_start_text,log_end_text,info_start_text,controller_info_start_text,controller_info):
        #print controller_info
        for line in log:
            if line.find(log_start_text) >= 0:
                self.lic_info_flag = 1



            if line.find(controller_info_start_text) >= 0:
                self.get_bsc_flag = 1


            if self.get_bsc_flag == 1:
                if line.find(controller_info) >= 0:
                    self.bsc_name = [i for i in line.split(' ') if i is not ''][1]
                    self.bsc_cnum = [i for i in line.split(' ') if i is not ''][2]
                    if line.find('@RNC-')>=0:
                        self.rnc_id = line.split('                            ')[0].split('-')[-1]
                    #print ("Parsing "+log_start_text+" for "+self.bsc_name+" ("+self.bsc_cnum+")")

                    self.get_bsc_flag = 0

            if self.lic_info_flag:
                if line.find(info_start_text) >= 0 or line.find(log_end_text)>=0:
                    self.aLicInfo.append('CONTROLLER NAME:' + self.bsc_name)
                    self.aLicInfo.append('CONTROLLER CNUM:' + self.bsc_cnum)
                    self.aLicInfo.append('RNC ID:' + self.rnc_id)
                    self.all_lic_info.append(self.aLicInfo)


                    self.aLicInfo = []
                else:
                    self.aLicInfo.append(line)

            if self.lic_info_flag and line.find(log_end_text) >= 0:
                self.lic_info_flag = 0


        self.all_lic_info = self.all_lic_info[1:]
        return self.all_lic_info


    def grep_ucap(self,log):
        self.aLicInfo = []
        for line in log:
            if line=='\n':
                #print ("continuing")
                continue
            if line.find('ZW7I:UCAP') >= 0:
                self.get_bsc_flag = 1

            if line.find('USED CAPACITY REPORT:') >= 0:
                self.lic_info_flag = 1


            if self.get_bsc_flag == 1:
                if line.find('mcBSC') >= 0:
                    self.bsc_name = [i for i in line.split(' ') if i is not ''][1]
                    self.bsc_cnum = [i for i in line.split(' ') if i is not ''][2]

                    self.get_bsc_flag = 0

            if self.lic_info_flag and line.find('<W7_>') >= 0:
                self.lic_info_flag = 0

            if self.lic_info_flag:
                if line.find('SUCCESS') >= 0:
                    #
                    # print '--'*20
                    # print self.aLicInfo
                    # print '--'*20


                    self.all_lic_info.append(self.aLicInfo)
                    self.aLicInfo = []
                else:
                    if line.find('          ') >= 0:
                        self.aLicInfo.append('CONTROLLER NAME:' + self.bsc_name)
                        self.aLicInfo.append('CONTROLLER CNUM:' + self.bsc_cnum)
                        self.aLicInfo.append(line)
                    #print len(self.aLicInfo)



        return self.all_lic_info


    def make_excel(self,workbook,worksheet,header,lic_info_objects):
        column = 0
        for i in header:
            column += 1
            worksheet.write(0, column, i)

        row = 0

        for obj in lic_info_objects:
            row+=1
            worksheet.write(row, 3, obj.licence_code)
            worksheet.write(row, 4, obj.licence_name)

            worksheet.write(row, 5, obj.licence_filename)
            worksheet.write(row, 6, obj.serial)
            worksheet.write(row, 7, obj.target_ne_type)
            worksheet.write(row, 8, obj.target_id)
            worksheet.write(row, 9, obj.start_date)
            worksheet.write(row, 10, obj.expiration_warning)
            worksheet.write(row, 11, obj.licence_capacity)
            worksheet.write(row, 12, obj.customer_id)
            worksheet.write(row, 13, obj.customer_name)
            worksheet.write(row, 14, obj.order_identifier)
            worksheet.write(row, 15, obj.licence_state)
