#!/usr/bin/env python

import sys
from scapy.all import *
import dpkt
import Gnuplot
#import numpy


def ip4packet(packet):
	'''Process an IPv4 packet'''
	if type(packet) == dpkt.ip.IP:
		if type(packet.data) == dpkt.udp.UDP:
			udppacket = ippacket.data
			if type(udppacket.data) == dpkt.dns.DNS:
				dnspacket = dpkt.dns.DNS(udppacket.data)
				if dnspacket.qr != dpkt.dns.DNS_R: continue
				if dnspacket.opcode != dpkt.dns.DNS_QUERY: continue
				if dnspacket.rcode != dpkt.dns.DNS_RCODE_NOERR: continue
				if len(dnspacket.an) < 1: continue


def ip6packet(packet):
	'''Process an IPv6 packet'''
	if type(packet) == dpkt.ip6.IP6:
		print 'IPv6 Packet found'


def udppacket(packet):
	'''Process a UDP packet'''
	if type(packet) == dpkt.udp.UDP:
		print 'UDP Packet found'


def dnspacket(packet):
	'''Process a DNS packet'''
	if type(packet) == dpkt.dns.DNS:
		print 'DNS Packet found'


def plotdata(xdata, ydata, xlabel, ylabel, graphtitle, filename, graphtype):
	'''Create a Gnuplot graph and save it to a file'''
	gplot = Gnuplot.Gnuplot()
	gplot.ylabel(ylabel)
	gplot.xlabel(xlabel)
	gplot_data = Gnuplot.Data(xdata, ydata, title=graphtitle)
	gplot.plot(gplot_data)
	gplot.hardcopy(filename, terminal=graphtype)
	gplot.reset()


def printheader(headtext):
	'''Print the specified text with decorations to mark it as header text'''
	sepline = '-' * (len(headtext) + 2)
	print '\n' + sepline
	print ' %s' % headtext
	print sepline


def dictinc(dictionary, key):
	'''Increment the value of the specified dict key. If the key doesn't exist,
	create the key and set the value to 1.'''
	if key in dictionary:
		dictionary[key] += 1
	else:
		dictionary[key] = 1
	return dictionary


def printdictascsv(dictionary):
	'''Print the key, value pairs in a dictionary as CSV text'''
	for key, val in dictionary.iteritems():
		print '%d,%d' % (key, val)


def dictascsv(dictionary):
	'''Print the key, value pairs in a dictionary as CSV text'''
	csvstr = ''
	for key, val in dictionary.iteritems():
		csvstr += str(key) + ',' + str(val) + '\n'
	return csvstr


def countinstances(items):
	'''Return a dictionary containing an instance of each item as a key
	and the count of times the item appears in the original list as the value'''
	outdict = {}
	for item in items:
		if item in outdict:
			outdict[item] += 1
		else:
			outdict[item] = 1
	return outdict


#ipv4_total = 0
#ipv6_total = 0
#
#ipv4_ihl_frequency = {}
#ipv4_tos_frequency = {}
#ipv4_len_frequency = {}
#ipv4_id_frequency = {}
#ipv4_flag_frequency = {}
#ipv4_frag_frequency = {}
#ipv4_ttl_frequency = {}
#ipv4_checksum_frequency = {}
#ipv4_option_frequency = {}
#
#udp_sport_frequency = {}
#udp_len_frequency = {}
#
#dns_id_frequency = {}
#dns_qr_frequency = {}
#dns_opcode_frequency = {}
#dns_aa_frequency = {}
#dns_tc_frequency = {}
#dns_rd_frequency = {}
#dns_ra_frequency = {}
#dns_z_frequency = {}
#dns_rcode_frequency = {}
#dns_qdcount_frequency = {}
#dns_ancount_frequency = {}
#dns_nscount_frequency = {}
#dns_arcount_frequency = {}

packets = []
if len(sys.argv) == 1:
	print 'You must specify a pcap file to process on the command line!'
	sys.exit(1)
else:
	try:
		for capfile in sys.argv[1:]:
			cap = open(capfile, 'r')
			packets += dpkt.pcap.Reader(cap).readpkts()
	except:
		print 'Couldn\'t read pcap file!'

# Loop through each packet in the sniffed collection and gather
# information from the headers.
for ts, data in packets:
	ether = dpkt.ethernet.Ethernet(data)
	if type(ether.data) == dpkt.ip.IP:
		ippacket = ether.data
		ip4packet(ippacket)
	elif type(ether.data) == dpkt.ip6.IP6:
		ippacket = ether.data
		ip6packet(ippacket)


	#
	# IP packet information
	#
#	if IP in packet:
#		if packet[IP].dst.startswith('204.13') or \
#			packet[IP].dst.startswith('208.78'):
#			# The packet is destined for a DNS4 anycast server
#			if DNS in packet:
#				# The IP packet contains a DNS segment
#				if UDP in packet:
#					# The IP packet contains a UDP segment
#					if packet[UDP].dport == 53:
#						ipv4_total += 1
#
#						# IPv4 packet information
#						ipv4_ihl_frequency = dictinc(ipv4_ihl_frequency, packet[IP].ihl)
#						ipv4_tos_frequency = dictinc(ipv4_tos_frequency, packet[IP].tos)
#						ipv4_len_frequency = dictinc(ipv4_len_frequency, packet[IP].len)
#						ipv4_id_frequency = dictinc(ipv4_id_frequency, packet[IP].id)
#						ipv4_flag_frequency = dictinc(ipv4_flag_frequency, packet[IP].flags)
#						ipv4_frag_frequency = dictinc(ipv4_frag_frequency, packet[IP].frag)
#						ipv4_ttl_frequency = dictinc(ipv4_ttl_frequency, packet[IP].ttl)
#						ipv4_checksum_frequency = dictinc(ipv4_checksum_frequency, \
#							packet[IP].chksum)
#						#ipv4_option_frequency = dictinc(ipv4_option_frequency, \
#						#	packet[IP].options)
#
#						# UDP packet information
#						udp_sport_frequency = dictinc(udp_sport_frequency, \
#							packet[IP][UDP].sport)
#						udp_len_frequency = dictinc(udp_len_frequency, packet[IP][UDP].len)
#
#						#
#						# DNS packet information
#						#
#						#dns_aa_frequency = {}
#						#dns_tc_frequency = {}
#						#dns_rd_frequency = {}
#						#dns_ra_frequency = {}
#						#dns_z_frequency = {}
#						#dns_rcode_frequency = {}
#						#dns_qdcount_frequency = {}
#						#dns_ancount_frequency = {}
#						#dns_nscount_frequency = {}
#						#dns_arcount_frequency = {}
#						dns_id_frequency = dictinc(dns_id_frequency, \
#							packet[IP][UDP][DNS].id)
#						dns_qr_frequency = dictinc(dns_qr_frequency, \
#							packet[IP][UDP][DNS].qr)
#						dns_opcode_frequency = dictinc(dns_opcode_frequency, \
#							packet[IP][UDP][DNS].opcode)
#
#
##
## IP packet statistics
##
#printheader('IP Packet Statistics')
#print 'ipv4,', ipv4_total
#print 'ipv6,', ipv6_total
#
#printheader('IPv4 IHL Statistics')
#csvout = open('ipv4_ihl_frequency.csv', 'w')
#csvout.write('ihl,count\n')
#csvout.write(dictascsv(ipv4_ihl_frequency))
#
#printheader('IPv4 TOS Statistics')
#csvout = open('ipv4_tos_frequency.csv', 'w')
#csvout.write('tos,count\n')
#csvout.write(dictascsv(ipv4_tos_frequency))
#
#printheader('IPv4 len Statistics')
#csvout = open('ipv4_len_frequency.csv', 'w')
#csvout.write('len,count\n')
#csvout.write(dictascsv(ipv4_len_frequency))
#plotdata(xdata=ipv4_len_frequency.values(), ydata=ipv4_len_frequency.keys(),
#	xlabel='Frequency', ylabel='Length', graphtitle='IPv4 Length Frequency',
#	filename='ipv4_len_frequency.png', graphtype='png')
#
#printheader('IPv4 ID Statistics')
#csvout = open('ipv4_id_frequency.csv', 'w')
#csvout.write('id,count\n')
#csvout.write(dictascsv(ipv4_id_frequency))
#plotdata(xdata=ipv4_id_frequency.values(), ydata=ipv4_id_frequency.keys(),
#	xlabel='Frequency', ylabel='ID', graphtitle='IPv4 ID Frequency',
#	filename='ipv4_id_frequency.png', graphtype='png')
#
#printheader('IPv4 Flag Statistics')
#csvout = open('ipv4_flag_frequency.csv', 'w')
#csvout.write('flag,count\n')
#csvout.write(dictascsv(ipv4_flag_frequency))
#plotdata(xdata=ipv4_flag_frequency.values(), ydata=ipv4_flag_frequency.keys(),
#	xlabel='Frequency', ylabel='Flag', graphtitle='IPv4 Flag Frequency',
#	filename='ipv4_flag_frequency.png', graphtype='png')
#
#printheader('IPv4 Frag Statistics')
#csvout = open('ipv4_frag_frequency.csv', 'w')
#csvout.write('frag,count\n')
#csvout.write(dictascsv(ipv4_frag_frequency))
#plotdata(xdata=ipv4_frag_frequency.values(), ydata=ipv4_frag_frequency.keys(),
#	xlabel='Frequency', ylabel='Fragments',
#	graphtitle='IPv4 Fragment Frequency', filename='ipv4_frag_frequency.png',
#	graphtype='png')
#
#printheader('IPv4 TTL Statistics')
#csvout = open('ipv4_ttl_frequency.csv', 'w')
#csvout.write('ttl,count\n')
#csvout.write(dictascsv(ipv4_ttl_frequency))
#plotdata(xdata=ipv4_ttl_frequency.values(), ydata=ipv4_ttl_frequency.keys(),
#	xlabel='Frequency', ylabel='TTL', graphtitle='IPv4 TTL Frequency',
#	filename='ipv4_ttl_frequency.png', graphtype='png')
#
#printheader('IPv4 Checksum Statistics')
#csvout = open('ipv4_checksum_frequency.csv', 'w')
#csvout.write('checksum,count\n')
#csvout.write(dictascsv(ipv4_checksum_frequency))
#plotdata(xdata=ipv4_checksum_frequency.values(),
#	ydata=ipv4_checksum_frequency.keys(), xlabel='Frequency', ylabel='Checksum',
#	graphtitle='IPv4 Checksum Frequency', filename='ipv4_checksum_frequency.png',
#	graphtype='png')
#
##
## UDP Statistics
##
#printheader('UDP Source Ports')
#csvout = open('udp_sport_frequency.csv', 'w')
#csvout.write('port,count\n')
#csvout.write(dictascsv(udp_sport_frequency))
#plotdata(xdata=udp_sport_frequency.values(),
#	ydata=udp_sport_frequency.keys(), xlabel='Frequency', ylabel='Port',
#	graphtitle='UDP Source Port Frequency', filename='udp_sport_frequency.png',
#	graphtype='png')
#
#printheader('UDP Packet Length')
#csvout = open('udp_len_frequency.csv', 'w')
#csvout.write('length,count\n')
#csvout.write(dictascsv(udp_len_frequency))
#plotdata(xdata=udp_len_frequency.values(),
#	ydata=udp_len_frequency.keys(), xlabel='Frequency', ylabel='Length',
#	graphtitle='UDP Length Frequency', filename='udp_len_frequency.png',
#	graphtype='png')
#
#
##
## DNS Statistics
##
##dns_id_frequency = {}
##dns_qr_frequency = {}
##dns_opcode_frequency = {}
##dns_aa_frequency = {}
##dns_tc_frequency = {}
##dns_rd_frequency = {}
##dns_ra_frequency = {}
##dns_z_frequency = {}
##dns_rcode_frequency = {}
##dns_qdcount_frequency = {}
##dns_ancount_frequency = {}
##dns_nscount_frequency = {}
##dns_arcount_frequency = {}
#
#printheader('DNS ID Frequency')
#csvout = open('dns_id_frequency.csv', 'w')
#csvout.write('ID,count\n')
#csvout.write(dictascsv(dns_id_frequency))
#plotdata(xdata=dns_id_frequency.values(),
#	ydata=dns_id_frequency.keys(), xlabel='Frequency', ylabel='ID',
#	graphtitle='DNS ID Frequency', filename='dns_id_frequency.png',
#	graphtype='png')
#
#printheader('DNS QR Frequency')
#csvout = open('dns_qr_frequency.csv', 'w')
#csvout.write('QR,count\n')
#csvout.write(dictascsv(dns_qr_frequency))
#plotdata(xdata=dns_qr_frequency.values(),
#	ydata=dns_qr_frequency.keys(), xlabel='Frequency', ylabel='QR',
#	graphtitle='DNS QR Frequency', filename='dns_qr_frequency.png',
#	graphtype='png')
#
#printheader('DNS OPCODE Frequency')
#csvout = open('dns_opcode_frequency.csv', 'w')
#csvout.write('OPCODE,count\n')
#csvout.write(dictascsv(dns_opcode_frequency))
#plotdata(xdata=dns_opcode_frequency.values(),
#	ydata=dns_opcode_frequency.keys(), xlabel='Frequency', ylabel='Opcode',
#	graphtitle='DNS OPCODE Frequency', filename='dns_opcode_frequency.png',
#	graphtype='png')
#
