#! /usr/bin/env python
#coding=utf-8
'''
version：1.0
监控windows信息：CPU占有率，内存占有率，端口开放情况，当前进程名称
数据格式：	[{'IP':getIp(),'CPUstate':getCPUState(),'Memorystate':getMemoryState(),
			'PortState':getPortState(),'ProcessName':getProcessName()},{},...]
'''
import time
import zmq
import psutil
import socket
import json
port = "5556"
server_addr = "192.168.116.133"
'''
获取被监控客户机的基本状态

'''
class MachineStatue:
	def _getHostName(self,):
		self._hostname = socket.getfqdn(socket.gethostname())
		return self._hostname

	def _getIP(self,):
		return socket.gethostbyname(self._hostname)

	def _getCPUState(self, interval=1):
		return psutil.cpu_percent(interval)

	def _getProcessInfo(self,):
		proc_pids = psutil.pids()
		proc_name = []
		for pid in proc_pids:
			proc = psutil.Process(pid)
			proc_name.append(proc.name())
		return zip(proc_pids,proc_name)

	def getInfo(self,):
		hostname = self._getHostName()
		ip = self._getIP()
		CPUState = self._getCPUState()
		processInfo = self._getProcessInfo()
		info = {'hostname':hostname,'ip':ip,'CPUState':CPUState,'processInfo':processInfo}
		return info
def main():
	print 'begin'
	machineStatue = MachineStatue()
	context = zmq.Context()
	req_socket = context.socket(zmq.REQ)
	print req_socket
	req_socket.connect("tcp://%s:%s"%(server_addr,port))
	while True:
		package = machineStatue.getInfo()
		req_socket.send(json.dumps(package))
		print "sending..."
		rev_info = req_socket.recv(copy=False)
		print rev_info
		time.sleep(5)
if __name__ == '__main__':
	main()
