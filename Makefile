# This file is part of whoson.
# https://github.com/heynemann/whos-on-server

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Bernardo Heynemann <heynemann@gmail.com>

# lists all available targets
list:
	@sh -c "$(MAKE) -p no_targets__ | awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {split(\$$1,A,/ /);for(i in A)print A[i]}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"
# required for list
no_targets__:

# install all dependencies (do not forget to create a virtualenv first)
setup:
	@pip install -U -e .\[tests\]

# test your application (tests in the tests/ directory)
test: redis_test unit

unit:
	@coverage run --branch `which nosetests` -vv --with-yanc -s tests/
	@coverage report -m --fail-under=80

# show coverage in html format
coverage-html: unit
	@coverage html

# get a redis instance up (localhost:4444)
redis: kill_redis
	redis-server ./redis.conf; sleep 1
	redis-cli -p 4444 info > /dev/null

# kill this redis instance (localhost:4444)
kill_redis:
	-redis-cli -p 4444 shutdown

# get a redis instance up for your unit tests (localhost:4448)
redis_test: kill_redis_test
	@redis-server ./redis.tests.conf; sleep 1
	@redis-cli -p 4448 info > /dev/null

# kill the test redis instance (localhost:4448)
kill_redis_test:
	@-redis-cli -p 4448 shutdown

kill-redis-sentinel:
	-redis-cli -p 57575 shutdown
	-redis-cli -p 57576 shutdown
	-redis-cli -p 57577 shutdown
	-redis-cli -p 57574 shutdown
	-redis-cli -p 57573 shutdown

redis-sentinel: kill-redis-sentinel
	redis-sentinel ./redis-conf/redis_sentinel.conf --daemonize yes; sleep 1
	redis-sentinel ./redis-conf/redis_sentinel2.conf --daemonize yes; sleep 1
	redis-server ./redis-conf/redis_test.conf --daemonize yes; sleep 1
	redis-server ./redis-conf/redis_test2.conf --daemonize yes; sleep 1
	redis-server ./redis-conf/redis_test3.conf --daemonize yes; sleep 1
	redis-cli -p 57574 info > /dev/null

run:
	@whoson -vvv -p 3128 -c ./whoson/config/local.conf
