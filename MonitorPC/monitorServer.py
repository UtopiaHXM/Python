#! /usr/bin/env python
#coding=utf-8
import time
import zmq
from zmq.eventloop import ioloop,zmqstream

import json
import optionalSearch

import pymongo

import random
from threading import Thread
from Queue import Queue

"""
ioloop.install() must be called prior to instantiating *any* tornado objects,
and ideally before importing anything from tornado, just to be safe.
install() sets the singleton instance of tornado.ioloop.IOLoop with zmq's
IOLoop. If this is not done properly, multiple IOLoop instances may be
created, which will have the effect of some subset of handlers never being
called, because only one loop will be running.
"""

ioloop.install()

import tornado
import tornado.web

port = "5556"
queue = Queue(50)

conn = pymongo.Connection("localhost",27017)
db = conn.processMonitor
systemStatue = db.systemStatue

class Producer(Thread):
	def run(self,):
		global queue
		context = zmq.Context()
		socket = context.socket(zmq.REP)
		socket.bind("tcp://*:%s" % port)
		while True:
			msg = socket.recv()
			socket.send("from server:has recieved...")
			systemInfo = json.loads(msg)
			print type(systemInfo)
			queue.put(systemInfo)
			print "Produced..."
			time.sleep(random.random())

class Consumer(Thread):
	def run(self,):
		global queue,systemStatue
		while True:
			msg  = queue.get()
			queue.task_done()
			print "Consumed::",msg
			#存储客户机监控信息
			systemStatue.insert(msg)
			#搜素算法（最优二叉查找树）
			optionalSearch.monitorClientStatue(msg)
			time.sleep(random.random())

# def zmq_rep():
# 	"""用于接收数据"""
# 	context = zmq.Context()
# 	socket = context.socket(zmq.REP)
# 	socket.bind("tcp://*:%s" % port)
# 	while True:
# 		msg = socket.recv()
# 		print msg
# 		socket.send("from server:has recieved...")

if __name__ == '__main__':
	#zmq_rep()
	# worker = threading.Thread(target=zmq_rep)
	# worker.start()
	Producer().start()
	Consumer().start()
