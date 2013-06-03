import glob
import os


class PluginBase(object):
	"""Base class for all plugin classes to inherit, so we can walk down the list of plugins from the top"""

	def __init__(self):
		self.PluginPath = ''

	def LoadPlugins(self):
		"""Default function to load all plugins"""
		for curfile in [f for f in glob.glob(os.path.join('plugins', self.PluginPath, '*.py'))
					if not os.path.basename(f) in ['__init__.py']]:
			LoadPluginFile(curfile)

	def Test(self):
		for sc in self.__class__.__subclasses__():
			if getattr(sc, 'Test', None):
				sc().Test()


class Raid(PluginBase):
	"""Parent class used for all RAID plugins"""

	def __init__(self):
		self.PluginPath = 'raid'


class Filesystems(PluginBase):
	"""Parent class used for all filesystem plugins"""

	def __init__(self):
		self.PluginPath = 'filesystem'


class Logs(PluginBase):
	"""Parent class used for all log file plugins"""

	def __init__(self):
		self.PluginPath = 'logs'


class System(PluginBase):
	"""Parent class used for all system check plugins"""

	def __init__(self):
		self.PluginPath = 'system'


class Permissions(PluginBase):
	"""Parent class used for all permission check plugins"""

	def __init__(self):
		self.PluginPath = 'permissions'


#------------------------------------------------------------------------------ 
# General plugin functions
#------------------------------------------------------------------------------ 
def RecursivePluginPrinter(PluginClass, prefix=''):
	for PluginType in PluginClass.__subclasses__():
		if PluginType.__subclasses__():
			newprefix = prefix + PluginType.__name__ + '.'
			RecursivePluginPrinter(PluginType, newprefix)
		else:
			print prefix + PluginType.__name__

def LoadPluginFile(fname):
	print 'Importing', fname
	dummy = __import__(os.path.splitext(fname)[0].replace('/', '.'))

def PluginsLoad():
	print '\nLoading plugins:\n----------------'
	for PluginType in PluginBase.__subclasses__():
		PluginType().LoadPlugins()
	print ''

def PluginsPrint():
	print '\nLoaded Plugins:\n---------------'
	RecursivePluginPrinter(PluginBase)

def PluginsTest():
	print '\nTesting Plugins:\n----------------'
	PluginBase().Test()

