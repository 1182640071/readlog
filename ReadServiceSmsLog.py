#coding=utf-8
'''
the code is utf-8

this .py is used to read log, then insert the information to redis

import third party module redis

'''
import time , thread , redis , sys ,threading , os


logList = list()  #used to save the information of log
lock = thread.allocate_lock() #make a lock
filename = 'sms.log'
url = '127.0.0.1'
redis_port = 6379
key = 'wml:20160929:test'
mutex = threading.Lock()
date = '20161101'
fileszie = 0

def writeredis(a,b):
    '''
    this function is used to insert the information of logList to redis
    :return:
    '''
    print '[INFO]the writeRedis thread start...'
    indexlist = list()

    while 1:
        lt = len(logList)
        size = 500

        if lt < 500:
            size = lt
        try:
            if size > 0:
                for index in range(size):
                    if mutex.acquire(1):
                        infomationLog = getinfo()
                        mutex.release()
                    if '' != infomationLog:
                        indexlist.append(infomationLog)
                print "[INFO]read:{0}".format(size)

                if len(indexlist) > 0:
                    write(indexlist)
                    print "[INFO]write:{0}".format(size)
        except:
            print '[ERROR]read or write the information of logList error'

        indexlist = []
        time.sleep(1)

def write(list):
    '''
    this function is used to write information to redis
    :param list:
    :return:
    '''
    try:
        client =  redis.StrictRedis(host=url, port=redis_port)
        for line in list:
            client.lpush(key,line.decode("ISO-8859-2").encode('utf-8'))
    except:
        print '[ERROR]write the information of logList error'

def getinfo():
    '''
    this function is used to get information from logList
    :return:
    '''
    global lock
    rs = ''
    #to protect the thread-safe , get the lock , when run over , realse the lock
    # lock.acquire()
    if len(logList) != 0:
        rs = logList.pop()
        # lock.release()
    return rs

def readlog(targetport):
    '''
    this function is used to read log,then save information to logList
    :return:
    '''
    global logList
    global date
    pt = targetport
    while 1:
        bl = 1
        dateRight = time.strftime("%Y-%m-%d",time.localtime(time.time()))
        size = os.path.getsize(filename)
        print '[INFO]today {0} , tomorrow {1} , size now {2} , size last {3}'.format(dateRight , date , size , fileszie)
        print '[INFO]size {0} , filezie {1}'.format(size , fileszie)
        if dateRight != date and size < fileszie:
            print '[INFO]change date , sleep...'
            time.sleep(10)
            print '[INFO]change the start byte for 0bt , start...'
            pt = 0
            date = dateRight
        f = open(filename)
        try:
            f.seek(pt,0)
            while bl > 0:
                info = f.readline()
                info = info.strip()
                if info != '':
                    while len(logList) > 2000:
                        time.sleep(0.2)
                    logList.append(info)
                else:
                    bl = 0
        except:
            print '[ERROR]read log error , please recheck the config or the information of your .py'
        finally:
            pt = f.tell()
            changeFileSize()
            print '[INFO]the .py has read {0} byte'.format(pt)
            f.close()
        time.sleep(1)

def changeFileSize():
    '''
    update the size of file
    :return:
    '''
    global fileszie
    fileszie = os.path.getsize(filename)


def get_lastport():
    '''
    this function is used to get the last point
    :return:last_port
    '''
    f = open(filename)
    f.seek(0,2)
    last_port = f.tell()
    f.close()
    return last_port


if __name__ == "__main__":

    print '[INFO]the .py start...'
    date = time.strftime("%Y-%m-%d",time.localtime(time.time()))
    # d = time.strftime("%Y-%m-%d  %H:%M:%S",time.localtime(time.time() - 3600))

    #start the threads of writing
    for index in range(3):
        thread.start_new_thread(writeredis , ('',''))

    # get the last point of the file
    try:
        lpt = get_lastport()
    except:
        print '[ERROR] get the last point of file error , stop the .py...'
        sys.exit()
    # #read log
    try:
        readlog(lpt)
    except:
        print '[ERROR] read error , stop the .py...'

