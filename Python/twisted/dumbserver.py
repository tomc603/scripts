#!/usr/bin/env python

from twisted.internet import reactor, protocol, endpoints


class UpperProtocol(protocol.Protocol):
	"""Protocol class"""

	def connectionMade(self):
		"""Handle a new connection"""
		self.transport.write('Garbage out\n')

	def connectionLost(self, reason):
		"""Handle a closed connection"""
		pass

	def dataReceived(self, data):
		"""Handle received data"""
		self.transport.write(data.upper())
		self.transport.loseConnection()

factory = protocol.ServerFactory()
factory.protocol = UpperProtocol

endpoints.serverFromString(reactor, "tcp:8000").listen(factory)
reactor.run()
