import os
import sqlite3
#
# tc = 0
# for f in os.listdir(os.getcwd()+'\\Parsed'):
#     flag = True
#     length12 = 0
#
#     with open(os.getcwd()+'\\Parsed\\'+f,'r') as f1:
#         cnt = 0
#         for line in f1.readlines():
#             length1 = len(line.split(','))
#             if cnt > 1:
#                 if length12 != length1:
#                     flag = False
#                     break
#             cnt+=1
#
#             length12 = len(line.split(','))
#
#     if not flag:
#         tc += 1
#     print(str(cnt)+':'+f+': '+str(flag))
# print(tc)


def get_lines(f):
    with open(os.getcwd()+'\\Parsed\\'+f, 'r') as adce:
        print('Working with '+f)
        while True:
            line = adce.readline().strip()
            if not line:
                break
            yield line


conn = sqlite3.connect('test.db')
cursor = conn.cursor()
#cursor.execute("CREATE TABLE ADCE ('plmn', 'BSC', 'BCF', 'BTS', 'ADCE', 'frequencyBandInUse', 'gprsMsTxPwrMaxCCH1x00', 'msTxPwrMaxGSM1x00', 'name', 'targetCellDN', 'adjCellBsicBcc', 'adjCellBsicNcc', 'adjCellLayer', 'adjacentCellIdCI', 'adjacentCellIdLac', 'adjacentCellIdMCC', 'adjacentCellIdMNC', 'adjcIndex', 'amrDadlbTargetCell', 'bcchFrequency', 'cellType', 'chainedAdjacentCell', 'dadlbTargetCell', 'drThreshold', 'dtmEnabled', 'dtmPowerBudgetMargin', 'enableDerivedHandoverPower', 'enableHoMarginLevQual', 'fastMovingThreshold', 'gprsEnabled', 'gprsMsTxpwrMaxCCH', 'gprsPenaltyTime', 'gprsRxlevAccessMin', 'gprsTemporaryOffset', 'hcsPriorityClass', 'hcsThreshold', 'hoLevelUmbrella', 'hoLoadFactor', 'hoMarginDelayTime', 'hoMarginLev', 'hoMarginPbgt', 'hoMarginQual', 'hoPriorityLevel', 'hoTargetArea', 'msPwrOptLevel', 'msTxPwrMaxGSM', 'nccrEgprsPbgtMargin', 'nccrGprsPbgtMargin', 'neighbourCellRanking', 'rac', 'rxLevMinCell', 'synchronized', 'trhoTargetLevel', 'reportingPriority');")

for f in os.listdir(os.getcwd()+'\\Parsed'):
    if f.find('create_') >= 0:
        with open(os.getcwd()+'\\Parsed\\'+f) as create_table:
            print(f)
            cursor.execute(create_table.readline().strip())

conn.commit()
#
# for f in os.listdir(os.getcwd()+'\\Parsed'):
#     if not f.find('create_') >= 0:
#         for l in get_lines(f):
#             cursor.execute(l)

for f in os.listdir(os.getcwd()+'\\Parsed'):
    if not f.find('create_') >= 0:
        print("Working with "+f)
        with open(os.getcwd()+'\\Parsed\\'+f) as insert_q_file:
            for line in insert_q_file.readlines():
                cursor.execute(line)
        conn.commit()
cursor.close()