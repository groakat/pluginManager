import inspect
import imp
import os


class PluginParser(object):
    def __init__(self, folder, baseClass):
        self.folder = folder
        self.baseClass = baseClass

    def retrieve(self):
        PluginParser.retrievePlugins(self.folder, self.baseClass)

    def check(self, pythonfile):
        self.checkFile(pythonfile, self.baseClass)

    @staticmethod
    def parseFolder(folder, extension=None):
        if extension is None:
            extension = '.py'

        fileList  = []
        for root,  dirs,  files in os.walk(folder):
            for f in files:
                if f.endswith(extension):
                    path = root + '/' + f
                    fileList.append(path)

        fileList = sorted(fileList)
        return fileList

    @staticmethod
    def loadModules(files):
        modules = []
        for f in files:
            moduleName = os.path.basename(f)[:-3]
            modules += [imp.load_source(moduleName, f)]

        return modules

    @staticmethod
    def filterClasses(modules):
        classes = []
        for m in modules:
            for k, i in m.__dict__.items():
                if inspect.isclass(i):
                    classes += [i]

        return classes

    @staticmethod
    def derivesFromBase(clss, baseClass):
        if baseClass in clss.__bases__:
            return True
        else:
            for c in clss.__bases__:
                if PluginParser.derivesFromBase(c, baseClass):
                    return True

            return False

    @staticmethod
    def filterBaseClass(classes, baseClass):
        filteredClasses = []
        for c in classes:
            if PluginParser.derivesFromBase(c, baseClass):
                filteredClasses += [c]

        return filteredClasses

    @staticmethod
    def retrievePlugins(folder, baseClass):
        pythonFiles = PluginParser.parseFolder(folder)
        modules = PluginParser.loadModules(pythonFiles)
        classes = PluginParser.filterClasses(modules)
        classes = PluginParser.filterBaseClass(classes, baseClass)
        return classes

    @staticmethod
    def checkFile(pythonFile, baseClass):
        modules = PluginParser.loadModules([pythonFile])
        classes = PluginParser.filterClasses(modules)
        classes = PluginParser.filterBaseClass(classes, baseClass)
        return classes



















