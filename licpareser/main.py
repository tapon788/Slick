from Slick.licpareser.logParser import ParseLog
from Slick.licpareser.licenseModel import lic_info,ucap
import xlsxwriter
import os

if __name__ == '__main__':
    fp = open(os.getcwd()+'\\..\\widgets\\logs\\bsc.log', 'r')
    log = fp.readlines()
    fp.close()
    wb = xlsxwriter.Workbook(os.getcwd()+'\\..\\widgets\\output\\lic_report.xlsx')

    ############################### LIC FULL ############################################

    inst_parse_log = ParseLog()
    collectedlog = inst_parse_log.grep(log,'ZW7I:LIC','<W7_>','----------------------------------------------','ZW7I:LIC','mcBSC')
    specific_info = ['CONTROLLER NAME','CONTROLLER CNUM','CUSTOMER ID','LICENCE CODE', 'LICENCE NAME', 'LICENCE FILE NAME', 'LICENCE CAPACITY','CUSTOMER NAME']
    object_array= []

    ws = wb.add_worksheet('BSC LIC')
    row = 0
    for spinfo in specific_info:
        ws.write(row,specific_info.index(spinfo),spinfo)

    for array in collectedlog:
        inst_lic_info = lic_info(specific_info)
        col = -1
        for i in array:
            for spinfo in specific_info:
                if i.find(spinfo) >= 0:
                    inst_lic_info.value[inst_lic_info.match.index(spinfo)] = i.split(':')[-1].replace('.', '').strip()
        row+=1
        for d in inst_lic_info.value:
            col+=1
            ws.write(row,col,d)

    # -----------------------------------------------------------------------------------------------------------------

    ############################### BSC FEA ############################################

    inst_parse_log = ParseLog()
    collectedlog = inst_parse_log.grep(log,'ZW7I:FEA','<W7_>','----------------------------------------------','ZW7I:FEA','mcBSC')

    specific_info = ['CONTROLLER NAME','CONTROLLER CNUM','FEATURE CODE', 'FEATURE NAME', 'FEATURE STATE']
    object_array = []

    ws = wb.add_worksheet('BSC FEA')
    row = 0
    for spinfo in specific_info:
        ws.write(row, specific_info.index(spinfo), spinfo)

    for array in collectedlog:
        inst_lic_info = lic_info(specific_info)
        col = -1
        for i in array:
            for spinfo in specific_info:
                if i.find(spinfo) >= 0:
                    inst_lic_info.value[inst_lic_info.match.index(spinfo)] = i.split(':')[-1].replace('.', '')
        row += 1
        for d in inst_lic_info.value:
            col += 1
            ws.write(row, col, d)

    ############################### BSC UCAP ############################################

    inst_parse_log = ParseLog()
    collectedlog = inst_parse_log.grep_ucap(log)


    object_array = []

    for array in collectedlog:

        inst_ucap = ucap()

        for i in array:
            if i.find('CONTROLLER NAME:') >= 0:
                inst_ucap.bsc_name = i.split(':')[-1].replace('.', '')
            if i.find('CONTROLLER CNUM:') >= 0:
                inst_ucap.bsc_cnum = i.split(':')[-1].replace('.', '')

            inst_ucap.feature_code = i.split('          ')[0].strip()
            inst_ucap.capacity_usage = i.split('          ')[-1].strip()

        object_array.append(inst_ucap)

    ws = wb.add_worksheet('BSC UCAP')
    ws.write(0, 0, 'CONTROLLER NAME')
    ws.write(0, 1, 'CONTROLLER CNUM')
    ws.write(0, 2, 'FEATURE CODE')
    ws.write(0, 3, 'USED CAPACITY')

    row = 0
    for i in object_array:
        row += 1
        ws.write(row, 0, i.bsc_name)
        ws.write(row, 1, i.bsc_cnum)
        ws.write(row, 2, i.feature_code)
        ws.write(row, 3, i.capacity_usage)

    # -----------------------------------------------------------------------------------------------------------------
    ############################### RNC LIC ############################################

    fp = open(os.getcwd()+'\\..\\widgets\\logs\\rnc.log', 'r')
    log = fp.readlines()
    fp.close()
    inst_parse_log_rnc = ParseLog()
    collectedlog = inst_parse_log_rnc.grep(log, '@RNC-', 'The total number of licenses ', '------------------------------------------------------------------', '@RNC-', '@RNC-')



    specific_info = ['RNC ID','License Code', 'License Name','Allowed Capacity','License Serial Number','License Start Time','License End Time',
                     'Order ID','Customer ID','Customer Name','Feature Code','Feature Name','License State','License State']
    object_array = []

    ws = wb.add_worksheet('RNC LIC')
    row = 0
    for spinfo in specific_info:
        ws.write(row, specific_info.index(spinfo), spinfo)

    for array in collectedlog:
        inst_lic_info = lic_info(specific_info)
        col = -1
        for i in array:
            #print (i)
            for spinfo in specific_info:
                if i.find(spinfo) >= 0:
                    #print (i)
                    inst_lic_info.value[inst_lic_info.match.index(spinfo)] = ''.join(i.split(':')[1:]).replace('.', '').strip()
        row += 1
        for d in inst_lic_info.value:
            col += 1
            ws.write(row, col, d)
    wb.close()
    input('\n\t\tLicense Parsing Done\n\t\tCheck output at ['+os.getcwd()+'\\out\\lic_report.xlsx] \n\t\tPress [ENTER] to exit')


