from os import path, chdir, getcwd, system
from pathlib import Path as FilePath
import json
from filecmp import cmp
import importlib
import sys
from shutil import copyfile
import subprocess
from re import compile
from mokhaUtils import getAllSubFolders, printDivider
from platform import system as getOperatingSystem


modules = {}
baseConfig = {}
application_path = ""
data = None


def loadJSON(filePath):
    with open(filePath) as file:
        jsonData = json.load(file)
    return jsonData


def createBaseConfig():
    configTypes = {"methods": "./methods.json",
                   "accounts": "./accounts.json", "dependencies": "./dependencies.json"}
    baseConfig = {"config-types": configTypes,
                  "dependencies-path": "./dependencies"}
    with open("./config.json", "w") as f:
        json.dump(baseConfig, f, indent=2)


def loadBaseConfig():
    if not (path.exists("./config.json")):
        createBaseConfig()
        raise Exception("Closing so you can configure application.")
    else:
        configJSON = loadJSON('./config.json')
        configTypes = configJSON["config-types"]
        for configType in configTypes.keys():
            baseConfig[configType] = configTypes[configType]
        baseConfig["dependencies-path"] = configJSON["dependencies-path"]


def cloneGitRepo(gitDependency):
    cmd = ["git", "clone", gitDependency["url"],
           gitDependency["directoryName"]]
    print(" ".join(cmd))
    subprocess.run(cmd, stdout=subprocess.PIPE)


def checkGitRepo(gitDependency):
    cmd = ["git", "status"]
    chdir(gitDependency["directoryName"])
    res = subprocess.run(
        cmd, stdout=subprocess.PIPE).stdout.decode('utf-8').lower().strip()
    secondLine = res.split("\n")[1]
    pattern = compile("your branch is behind")
    upToDate = pattern.match(secondLine) == None
    if (not upToDate):
        cmd = ["git", "pull", "-f"]
        res = subprocess.run(cmd, stdout=subprocess.PIPE)
        print("Pulled latest changes for: %s" % gitDependency["url"])
    chdir(baseConfig["dependencies-path"])


def checkGitDependencies(gitDependencies):
    chdir(baseConfig["dependencies-path"])
    for gitDependency in gitDependencies:
        gitDirname = gitDependency["directoryName"]
        if (path.exists("%s" % (gitDirname))):
            checkGitRepo(gitDependency)
        else:
            cloneGitRepo(gitDependency)
    chdir(application_path)


def copyExternalDependencies(externalDependencies):
    for externalDependency in externalDependencies:
        # check if file exists in dependencies folder
        try:
            externalDependency = externalDependency[getOperatingSystem(
            ).lower()]
        except Exception as e:
            continue
        try:
            externalFileName = path.basename(externalDependency)
            # compare equality
            localFilePath = "%s/%s" % (
                baseConfig["dependencies-path"], externalFileName)
            updateDependency = True
            if (path.exists(localFilePath)):
                filesEqual = cmp(externalDependency, localFilePath)
                if (filesEqual):
                    updateDependency = False
            if (updateDependency):
                print("COPYING EXTERNAL DEPENDENCY:\n%s" %
                      (externalDependency))
                copyfile(externalDependency, localFilePath)
        except Exception as e:
            print(e)


def importDependencies():
    dependencyJSON = None
    with open(baseConfig["dependencies"]) as file:
        dependencyJSON = json.load(file)
    pip = dependencyJSON["pip"]
    checkPipDependencies(pip)
    gitDependencies = dependencyJSON["git"]
    checkGitDependencies(gitDependencies)
    external = dependencyJSON["external"]
    copyExternalDependencies(external)
    fileSystem = dependencyJSON["file-system"]
    checkFileSystemDependencies(fileSystem)
    appendSysPath()
    python = dependencyJSON["python"]
    importPythonModules(python)


def checkFileSystemDependencies(fileSystemDependencies):
    chdir(baseConfig["dependencies-path"])
    for fileSystemDependency in fileSystemDependencies:
        if(path.exists(fileSystemDependency) == False):
            raise Exception("Error checking file system dependencies.")
    print("Filesystem dependencies loaded successfully.")
    chdir(application_path)


def importMokhaEngine():
    print("Importing Mokha Engine.")
    mokhaEngine = importlib.import_module("mokhaEngine")
    modules["mokhaEngine"] = mokhaEngine


def appendSysPath():
    allSubfolders = getAllSubFolders(baseConfig["dependencies-path"])
    sys.path.extend(allSubfolders)


def checkPipDependencies(pipPackages):
    pipList = subprocess.run(
        "pip list".split(), stdout=subprocess.PIPE).stdout.decode('utf-8').lower()
    installCmd = ["pip", "install"]
    for pipPackage in pipPackages:
        pipType = type(pipPackage)
        if (pipType == dict):
            regexPattern = "%s\\s+%s" % (
                pipPackage["package-name"], pipPackage["version"])
            regex = compile(regexPattern)
            installed = regex.search(pipList) != None
            if(not installed):
                installCmd.append("%s==%s" % (
                    pipPackage["package-name"], pipPackage["version"]))
        elif (pipType == str):
            regexPattern = "%s\\s+" % (
                pipPackage)
            regex = compile(regexPattern)
            installed = regex.search(pipList) != None
            if(not installed):
                installCmd.append(pipPackage)
        else:
            raise Exception(
                "Don't know how to handle this type of object as Pip dependency mate. Fix ya config!")
    try:
        if (len(installCmd) > 2):
            print(" ".join(installCmd))
            subprocess.run(installCmd, stdout=subprocess.PIPE)
    except Exception as e:
        print(e)
        print("Error with installing Pip dependencies.")
        exit()


def importPythonModules(pythonDependencies):
    importMokhaEngine()
    outputStrings = []
    for dependency in pythonDependencies:
        try:
            module = importlib.import_module(dependency)
            modules[dependency] = module
            outputStrings.append("%s: ✅" % (dependency))
        except ModuleNotFoundError as e:
            print(e)
            outputStrings.append("%s: ❌" % (dependency))
            print("\n".join(outputStrings))
            raise Exception("Error importing python dependencies.")
    print(" ".join(outputStrings))


def setup():
    global application_path
    chdir(FilePath(path.abspath(__file__)).parent)
    application_path = getcwd()


def main():
    setup()
    loadBaseConfig()
    # Ensures python can see dependencies outside of root dir.
    sys.path.append(baseConfig['dependencies-path'])
    try:
        importDependencies()
    except Exception as e:
        print(e)
        exit("Could not import dependencies correctly. Please check your config.")
    printDivider()
    print("Welcome to Mokha V2.0! This is a tool designed to enable configuration of shortcuts to python code.")
    printDivider()
    accounts = loadJSON(baseConfig["accounts"])
    methods = loadJSON(baseConfig["methods"])
    kwargs = {"baseConfig": baseConfig, "accounts": accounts,
              "methods": methods, "modules": modules}
    mokhaEngine = modules["mokhaEngine"]
    mokhaEngine.main(**kwargs)


if (__name__ == "__main__"):
    main()
