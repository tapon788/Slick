import memory_profiler
import time


def xml_mo_chunker():
    st = time.ctime()
    fp = open('noklte_srbts.xml', 'r')
    mo_chunk = []
    cnt = 0
    mo = False
    header = ''
    for line in fp:
        if line.find('<managedObject ') >= 0:
            mo = True

        if line.find('</managedObject>') >= 0:
            cnt += 1
            mo_chunk.append(line)
            mo = False
            if (cnt % 100) == 0:
                fp = open('C:\\Python36\\Scripts\\python3env\\Scripts\\MyQt5\\Slick\\parser\\ToBeParsed\\' + str(int(cnt / 100)) + '.xml', 'w+')
                fp.write('<raml version="2.0">\n')
                for line in mo_chunk:
                    fp.write(line)
                fp.write('</raml>')
                fp.close()
                mo_chunk = []
        if mo:
            mo_chunk.append(line)
    fp.close()


if __name__ == '__main__':
    m1 = memory_profiler.memory_usage()
    t1 = time.clock()
    cubes = xml_mo_chunker()
    t2 = time.clock()
    m2 = memory_profiler.memory_usage()
    time_diff = t2 - t1
    mem_diff = m2[0] - m1[0]
    print ("It took "+str(time_diff)+" Secs and "+str(mem_diff)+" Mb to execute this method")



end = time.ctime()






