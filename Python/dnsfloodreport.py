#!/usr/bin/env python
import os
import sys
import glob
import pandas as pds
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

# class Graph(object):
#
#     def __init__(self, options):
#         self.output_path = options.output_path
#         self.groupby = options.groupby
#         self.axes = options.axes
#
#         try:
#             self.input_file = open(self.input_filename)
#         except IOError as e:
#             print "%s: '%s'" % (e.strerror, e.filename)
#             sys.exit(3)
#
#         try:
#             os.mkdir(self.output_dir)
#         except (IOError, OSError) as e:
#             print "%s: '%s'" % (e.strerror, e.filename)
#             sys.exit(3)
#
#     def process(self):
#         self.temp = []
#         self.header = ''
#
#         for line in self.input_file:
#             if line.startswith('#'):
#                 try:
#                     self.generate()
#                 except ValueError:
#                     print "Error generate graph"
#
#                 self.header = split_re.split(line.strip())
#                 self.temp = []
#             else:
#                 self.temp.append(split_re.split(line.strip()))
#
#         try:
#             self.generate()
#         except ValueError:
#             print "Error generate graph"
#
#     def gen_title(self):
#         if self.header:
#             return '__'.join(self.header[3:]).replace('/', '-per-')
#         return ''
#
#     def generate(self):
#         if not self.temp:
#             return
#
#         print "\nrows count: %d" % len(self.temp)
#         print self.gen_title()
#
#         plt.hold(True)
#         fig = plt.figure()
#         ax = fig.add_subplot(111)
#
#         if self.is_csv:
#             f = open(os.path.join(self.output_dir, "%s.csv" % self.gen_title()),
#                     'wt')
#             writer = csv.writer(f)
#             writer.writerows([self.header] + self.temp)
#             f.close()
#
#         i = 0
#
#         if self.header[3] in self.sub_categories:
#             k = -1
#             categories = defaultdict(list)
#             for item in self.temp:
#                 categories[item[3]].append(item)
#
#             for category in sorted(categories)[:10]:
#                 i = 0
#                 k += 1
#                 for j in range(4, len(self.header)):
#                     list_date = []
#                     list_value = []
#
#                     for item in categories[category]:
#                         # import pdb; pdb.set_trace()
#                         list_date.append(
#                         dt.datetime.strptime(item[2], '%Y-%m-%d %H:%M:%S UTC'))
#                         list_value.append(item[j])
#
#                     if k == len(line_styles):
#                         k = 0
#                         i += 1
#
#                     ax.plot_date(mpl.dates.date2num(list_date),
#                         list_value, linestyle = line_styles[k],
#                         label = '%s %s %s' % (self.header[3], category,
#                             self.header[j]), c = color_scheme20[i],
#                         marker = choice(marker_styles))
#
#                     if self.is_stat:
#                         list_value = map(float, list_value)
#                         f = open(os.path.join(
#                             self.output_dir, "%s.txt" % self.gen_title()), 'a')
#                         f.write('%s %s %s max : %s \n' % (self.header[3],
#                             category, self.header[j], max(list_value)))
#                         f.write('%s %s %s min : %s \n' % (self.header[3],
#                             category, self.header[j], min(list_value)))
#                         f.write('%s %s %s avg : %s \n' % (self.header[3],
#                             category, self.header[j],
#                             sum(list_value) / float(len(list_value))))
#                         f.close()
#
#                     i += 1
#
#         else:
#             for j in range(3, len(self.header)):
#                 list_date = []
#                 list_value = []
#
#                 for item in self.temp:
#                     list_date.append(
#                         dt.datetime.strptime(item[2], '%Y-%m-%d %H:%M:%S UTC'))
#                     list_value.append(item[j])
#
#                 ax.plot_date(mpl.dates.date2num(list_date),
#                         list_value, linestyle = '-',
#                         label = self.header[j], c = color_scheme20[i],
#                         marker = choice(marker_styles))
#
#                 if self.is_stat:
#                     list_value = map(float, list_value)
#                     f = open(os.path.join(
#                         self.output_dir, "%s.txt" % self.gen_title()), 'a')
#                     f.write('%s max : %s \n' % (self.header[j], max(list_value)))
#                     f.write('%s min : %s \n' % (self.header[j], min(list_value)))
#                     f.write('%s avg : %s \n' % (self.header[j],
#                         sum(list_value) / float(len(list_value))))
#                     f.close()
#
#                 i += 1
#
#         ax.grid(True)
#         minute_fmt = mpl.dates.DateFormatter('%H:%M')
#         ax.xaxis.set_major_formatter(minute_fmt)
#
#         minute_loc = mpl.dates.MinuteLocator()
#         ax.xaxis.set_major_locator(minute_loc)
#
#         if self.is_minor:
#             second_fmt = mpl.dates.DateFormatter('%S')
#             second_loc = mpl.dates.SecondLocator(bysecond = range(10, 60, 10))
#             ax.xaxis.set_minor_formatter(second_fmt)
#             ax.xaxis.set_minor_locator(second_loc)
#
#         fig.autofmt_xdate()
#
#         ax.set_title(self.gen_title())
#
#         plt.ylabel('Value')
#
#         box = ax.get_position()
#         ax.set_position([box.x0, box.y0 + box.height * 0.1,
#                          box.width, box.height * 0.9])
#
#         # Put a legend below current axis
#         ax.legend(loc = 'upper center', bbox_to_anchor = (0.5, -0.05),
#                   fancybox = True, shadow = True, ncol = 5)
#
#         # plt.show()
#         plt.savefig(os.path.join(self.output_dir, "%s.png" % self.gen_title()))


def PrintHeader(printstring):
    print('\n')
    print('-' * len(printstring))
    print(printstring)
    print('-' * len(printstring))


def PrintBullet(printstring, indent=1):
    print('%s* %s' % (' ' * (indent * 2), printstring))


# 2D compare graphs to produce
compares_2d = [('IPs', 'Received',), ('Ports', 'Received',),
               ('Sent', 'Received',), ('Target_QPS', 'Received_QPS',)]

# 2D graphs to produce
graphs_2d = [('IPs', 'Received',), ('Ports', 'Received',),
             ('Sent', 'Received',), ('Target_QPS', 'Received_QPS',)]

# 3D graphs to produce
graphs_3d = [('IPs', 'Ports', 'Received',), ('IPs', 'Sent', 'Received',),
             ('Ports', 'Sent', 'Received',)]

if '--help' in sys.argv or '-h' in sys.argv:
    print('Usage: %s inputglob outputdir' % sys.argv[0])
    sys.exit(1)

if not os.path.isdir(sys.argv[2]):
    print('Output path is not a directory: %s' % sys.argv[2])
    sys.exit(1)

for fname in glob.glob(sys.argv[1]):
    PrintHeader('Setting up plotting environment')
    PrintBullet('Reading data from %s' % fname)
    srcdata = pds.read_csv(fname, delimiter=',')

    PrintBullet('Calculating plot limits')
    LimitData = {}
    for k in srcdata.keys():
        if not k in ['OS']:
            # Calculate minimum and maximum values for the current column
            minval = srcdata[k].min() * 0.99
            maxval = srcdata[k].max() * 1.01
            if minval < 0:
                # Minimum shouldn't be less than zero in this report.
                minval = 0

            # Save the minimum and maximum values as a tuple in our value dict
            LimitData[k] = (minval, maxval,)
            PrintBullet('%s: %d %d' % (k, minval, maxval), indent=2)

    PrintHeader('Producing graphs')
    #
    # Iterate through each QPS group
    #
    for qpsgroup in srcdata.groupby(['Target_QPS']):
        qpsgroupval = qpsgroup[0]
        qpsgroupdata = qpsgroup[1]

        PrintBullet('Charting Target_QPS: %d' % qpsgroupval)

        #
        # Iterate through each OS group
        #
        try:
            osgroup = qpsgroupdata.groupby(['OS'])
            fig_ipvreceived, axes_ipvreceived = plt.subplots(len(osgroup), sharex = True)

            #
            # Iterate through each graph
            #
            for graph in graphs_2d:
                try:
                    subplotid = 0

                    fig_plots, axes_plots = plt.subplots(2, sharex=True, figsize=(10.24, 7.68))
                    fig_plots.suptitle('%s vs. %s @ %d QPS\n' % (graph[0], graph[1],
                                                                 qpsgroupval))
                    for (osgroupval, osgroupdata) in osgroup:
                        try:
                            axes_plots[subplotid].scatter(x=osgroupdata[graph[0]], y=osgroupdata[graph[1]])
                            axes_plots[subplotid].set_xlim(LimitData[graph[0]][0], LimitData[graph[0]][1])
                            axes_plots[subplotid].set_ylim(LimitData[graph[1]][0], LimitData[graph[1]][1])
                            if subplotid == 1:
                                # Only print the X label if this is the final plot.
                                axes_plots[subplotid].set_xlabel(graph[0])
                            axes_plots[subplotid].set_ylabel(graph[1])
                            axes_plots[subplotid].set_title('%s' % osgroupval)
                            axes_plots[subplotid].grid(True)

                            # Increment our subplot counter
                            subplotid += 1
                        except:
                            print('ERROR: Charting %s vs. %s for %s' % (graph[0], graph[1], osgroupval))
                            continue

                    fig_plots.savefig('%s/dnsflood-%sVs%s-%dqps.png' %
                                      (sys.argv[2], graph[0], graph[1], qpsgroupval))
                except:
                    print('ERROR: Charting %s vs. %s' % (graph[0], graph[1]))
                    continue

            for graph in graphs_3d:
                try:
                    for (osgroupval, osgroupdata) in osgroup:
                        try:
                            fig_plot = plt.figure(figsize=(10.24, 7.68))
                            fig_plot.suptitle('%s vs. %s vs. %s @ %d QPS\n' %
                                              (graph[0], graph[1], graph[2], qpsgroupval))

                            axes_plot = fig_plot.add_subplot(111, projection='3d')
                            axes_plot.scatter(osgroupdata[graph[0]], osgroupdata[graph[1]], osgroupdata[graph[2]])
                            axes_plot.set_xlim(LimitData[graph[0]][0], LimitData[graph[0]][1])
                            axes_plot.set_ylim(LimitData[graph[1]][0], LimitData[graph[1]][1])
                            axes_plot.set_zlim(LimitData[graph[2]][0], LimitData[graph[2]][1])
                            axes_plot.set_xlabel(graph[0])
                            axes_plot.set_ylabel(graph[1])
                            axes_plot.set_zlabel(graph[2])
                            axes_plot.set_title('%s' % osgroupval)
                            axes_plot.grid(True)
                            fig_plot.savefig('charts/dnsflood-%sVs%sVs%s-%dqps-%s.png' %
                                             (graph[0], graph[1], graph[2], qpsgroupval, osgroupval))
                        except:
                            print('ERROR: Charting %s vs. %s vs. %s for %s' % (graph[0], graph[1], graph[2],
                                                                               osgroupval))
                            continue

                except:
                    print('ERROR: Charting %s vs. %s vs. %s' % (graph[0], graph[1], graph[2]))
                    continue

        except:
            print('ERROR: Creating graphs for QPS value %s.' % qpsgroupval)
            continue
