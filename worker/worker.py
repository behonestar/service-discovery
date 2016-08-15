import redis
import urllib
import time

r = redis.StrictRedis(host='haproxy', port=80, db=0)
while True:
	r.set('foo','bar')
	print r.get('foo')
	time.sleep(3)
