#!/usr/bin/env python

import bz2

#queryoutput = bz2.BZ2File(options.queryoutputfile + '.bz2', mode='w',
#	buffering=BUFFSIZ, compresslevel=COMPLVL)

outfile = open('testdata.bz2', mode='w')

data1 = 'a' * 1048576
data2 = 'b' * 1048576
data3 = 'c' * 1048576
data4 = 'd' * 1048576

cdata1 = bz2.compress(data1)
cdata2 = bz2.compress(data2)
cdata3 = bz2.compress(data3)
cdata4 = bz2.compress(data4)

outfile.write(cdata1 + cdata2 + cdata3 + cdata4)
outfile.flush()
outfile.close()
