import time , thread , redis , sys
#######################
filename = 'sms.log'
url = '127.0.0.1'
redis_port = 6379
key = 'wml:20160929:test'

if __name__ == "__main__":
    print 1
    a = 'asdfasdafsdf'
    b = 'asd'
    print (b in a)


    # for j in range(1,50):
    #     client =  redis.StrictRedis(host=url, port=redis_port)
    #     client.lpush(key,'12341234')
    #     for i in range(1,50):
    #         client.lpush(key,'12341234' + str(i))
