#!/usr/bin/env python3

import os
import csv
import time


class DeviceStats(object):
    timestamp = None
    read_ios = None
    read_merges = None
    read_sectors = None
    read_ticks = None
    write_ios = None
    write_merges = None
    write_sectors = None
    write_ticks = None
    ios_progress = None
    total_ticks = None
    rq_ticks = None
    discard_ios = None
    discard_merges = None
    discard_sectors = None
    discard_ticks = None
    flush_ios = None
    flush_ticks = None

    def __init__(self, data):
        self._parse(data)

    def __repr__(self):
        reprstr =\
            "<{}(ts={}, read_ios={}, read_merges={}, read_sectors={}, read_ticks={}, write_ios={}," \
            "write_merges={}, write_sectors={}, write_ticks={}, ios_progress={}, total_ticks={}, rq_ticks={}" \
            "discard_ios={}, discard_merges={}, discard_sectors={}, discard_ticks={}, flush_ios={}," \
            "flush_ticks={})>".format(
                self.__class__.__name__,
                self.timestamp,
                self.read_ios,
                self.read_merges,
                self.read_sectors,
                self.read_ticks,
                self.write_ios,
                self.write_merges,
                self.write_sectors,
                self.write_ticks,
                self.ios_progress,
                self.total_ticks,
                self.rq_ticks,
                self.discard_ios,
                self.discard_merges,
                self.discard_sectors,
                self.discard_ticks,
                self.flush_ios,
                self.flush_ticks)
        return reprstr

    def _parse(self, data):
        """
        Read a list of values, and place them into the proper fields

        :param data: A list of elements from a device's stats file
        :type data: list
        """
        self.timestamp = time.time()

        if len(data) >= 11:
            self.read_ios = int(data[0])
            self.read_merges = int(data[1])
            self.read_sectors = int(data[2])
            self.read_ticks = int(data[3])
            self.write_ios = int(data[4])
            self.write_merges = int(data[5])
            self.write_sectors = int(data[6])
            self.write_ticks = int(data[7])
            self.ios_progress = int(data[8])
            self.total_ticks = int(data[9])
            self.rq_ticks = int(data[10])

            if len(data) >= 15:
                self.discard_ios = int(data[11])
                self.discard_merges = int(data[12])
                self.discard_sectors = int(data[13])
                self.discard_ticks = int(data[14])

            if len(data) >= 17:
                self.flush_ios = int(data[15])
                self.flush_ticks = int(data[16])

    @staticmethod
    def fields():
        return ('timestamp', 'read ios', 'read merges', 'read sectors',
                'read ticks', 'write ios', 'write merges',
                'write sectors', 'write ticks', 'ios progress',
                'total ticks', 'rq ticks', 'discard ios', 'discard merges',
                'discard sectors', 'discard ticks', 'flush ios',
                'flush ticks')

    def list(self):
        """
        Return a tuple containing the values from DeviceStats

        :return: Tuple of values in DeviceStats
        :rtype: tuple
        """
        return (
            self.timestamp,
            self.read_ios,
            self.read_merges,
            self.read_sectors,
            self.read_ticks,
            self.write_ios,
            self.write_merges,
            self.write_sectors,
            self.write_ticks,
            self.ios_progress,
            self.total_ticks,
            self.rq_ticks,
            self.discard_ios if self.discard_ios is not None else 0,
            self.discard_merges if self.discard_merges is not None else 0,
            self.discard_sectors if self.discard_sectors is not None else 0,
            self.discard_ticks if self.discard_ticks is not None else 0,
            self.flush_ios if self.flush_ios is not None else 0,
            self.flush_ticks if self.flush_ticks is not None else 0
        )

    def sub(self, subtrahend):
        """
        Calculate the difference between the current values and the values supplied in new

        :param subtrahend: A DeviceStats to subtract from the current
        :type subtrahend: DeviceStats
        :return: tuple
        """
        return (
            self.timestamp - subtrahend.timestamp,
            self.read_ios - subtrahend.read_ios,
            self.read_merges - subtrahend.read_merges,
            self.read_sectors - subtrahend.read_sectors,
            self.read_ticks - subtrahend.read_ticks,
            self.write_ios - subtrahend.write_ios,
            self.write_merges - subtrahend.write_merges,
            self.write_sectors - subtrahend.write_sectors,
            self.write_ticks - subtrahend.write_ticks,
            self.ios_progress - subtrahend.ios_progress,
            self.total_ticks - subtrahend.total_ticks,
            self.rq_ticks - subtrahend.rq_ticks,
            self.discard_ios - subtrahend.discard_ios if self.discard_ios is not None else 0,
            self.discard_merges - subtrahend.discard_merges if self.discard_merges is not None else 0,
            self.discard_sectors - subtrahend.discard_sectors if self.discard_sectors is not None else 0,
            self.discard_ticks - subtrahend.discard_ticks if self.discard_ticks is not None else 0,
            self.flush_ios - subtrahend.flush_ios if self.flush_ios is not None else 0,
            self.flush_ticks - subtrahend.flush_ticks if self.flush_ticks is not None else 0,
        )


def collect_disk_stats(device, interval, iterations):
    """

    :param device: A block device name (ie: sda or nvme0n1)
    :type device: string

    :param interval: Number of seconds between collections
    :type interval: float

    :param iterations: Number of collections to perform
    :type iterations: int

    :return: List of DeviceStats objects
    :rtype: list
    """
    dev_stats_path = os.path.join('/sys/block', device, 'stat')
    iteration = 0
    stats = []

    while iteration < iterations:
        iteration += 1
        start_time = time.time()
        with open(dev_stats_path, 'r') as f:
            data = f.read().split()
            stats.append(DeviceStats(data))
        run_time = time.time() - start_time
        time.sleep(max(interval - run_time, 0))

    return stats


def stats_to_csv(values):
    with open('device-stat.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(DeviceStats.fields())
        for stat in values:
            writer.writerow(stat.list())


def print_stats(values):
    """
    Print the I/O stats between DeviceStats instances

    :param values: A list of DeviceStats to print
    :type values: list[DeviceStats]
    """
    last_stat = None
    print(DeviceStats.fields())
    for stat in values:
        if last_stat is None:
            print(stat.list())
        else:
            print(stat.sub(last_stat))
        last_stat = stat


if __name__ == '__main__':
    s = collect_disk_stats('sda', 10, 3)
    # print_stats(s)
    stats_to_csv(s)
