#import paramiko
from paramiko import SSHClient,AutoAddPolicy
from time import sleep,strftime
from os import getcwd
from re import compile

from deputy.os_utility import clean_dir

class SlickSSH:
    def __init__(self,connection_info_details,return_char,cmd_list):
        self.connection_info_details = connection_info_details
        self.cmd_list = cmd_list
        self.return_char = return_char

    def execute_cmd(self, update, progress):
        print('*'*50)
        print (self.connection_info_details)
        clean_dir(getcwd()+'\\logs')
        fp = open(getcwd()+'\\logs\\'+self.connection_info_details[0]['Group']+(strftime("_%w_%B_%X")).replace(":",'')+'.log','w+')
        for connections in self.connection_info_details:
            update.emit('Connecting to '+connections['Name'])
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy)
            ssh.connect(connections['Address'], connections['Port'], connections['User'], connections['Pass'])
            update.emit('Invoking shell')
            channel = ssh.invoke_shell()
            update.emit('Connected')
            buffer = str()

            cnt = 0
            update.emit("\nRunning command on Node: " + connections['Name'])
            for cmd in self.cmd_list:

                progress.emit(1)
                update.emit('cmd: '+cmd)
                channel.send(cmd + self.return_char)
                sleep(1)
                while True:
                    sleep(0.1)
                    if channel.recv_ready():

                        out = channel.recv(1024).decode('utf-8')
                        print('-'*20)
                        print (out)
                        # print(out.split('\r\n'))
                        now = buffer + '\r\n'.join(out.split('\r\n')[:-1])+'\r\n'
                        now = compile(r'\x1b[^m]*m').sub('', now)
                        #print ('now:'+now)
                        # print ('-'*20)
                        buffer = out.split('\r\n')[-1]
                        #print ('buffer: '+buffer)
                        # print ('-'*20)
                        if out.find('\r\n') < 0:
                            now = now.replace('\r\n', '')
                        fp.write(now)
                        #screen.append(now)
                        # print('*' * 20)
                    else:
                        #sleep(1)
                        fp.write(buffer)
                        #screen.append(buffer)
                        break

                '''
                while True:
                    time.sleep(0.2)
                    if channel.recv_ready():
                        while not buf.find(':~# ')>=0:
                            buf += channel.recv(100).decode('utf-8')
                        fp.write(buf)
                        screen.append(buf)
                    else:
                        print ("break")
                        break
                '''

                progress.emit((100 / (len(self.cmd_list) - cnt)))
                cnt += 1
            ssh.close()
            fp.write('\n')
        fp.close()