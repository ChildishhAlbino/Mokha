from os import path, chdir, getcwd, system, environ
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
import time
import concurrent.futures

modules = {}
baseConfig = {}
application_path = ""
data = None
gitUpdate = False


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
    print("Base Config: ✅")


def cloneGitRepo(gitDependency):
    cmd = ["git", "-C", baseConfig["dependencies-path"], "clone", "--single-branch",
           "--branch", gitDependency["branch"], gitDependency["url"], gitDependency["directory-name"]]
    print("Git Clone on %s" % (gitDependency["url"]))
    subprocess.run(cmd, stdout=subprocess.PIPE)


def pullGitRepo(gitDependency):
    global gitUpdate
    t1 = time.perf_counter()
    statusCMD = ["git", "-C",
                 path.join(baseConfig["dependencies-path"], gitDependency["directory-name"]), "status"]

    fetchCMD = ["git", "-C", path.join(baseConfig["dependencies-path"], gitDependency["directory-name"]),
                "fetch", "origin", gitDependency["branch"], "-q"]

    cmd = []
    cmd.extend(fetchCMD)
    cmd.append("&&")
    cmd.extend(statusCMD)
    res = subprocess.run(
        cmd, stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8').lower().strip()
    t2 = time.perf_counter()
    print("%s took %s seconds" % (gitDependency["url"], round(t2 - t1, 2)))
    secondLine = res.split("\n")[1]
    pattern = compile("your branch is behind")
    upToDate = pattern.match(secondLine) == None
    if (not upToDate):
        cmd = ["git", "-C", path.join(
            baseConfig["dependencies-path"], gitDependency["directory-name"]), "pull", "-f"]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
        print("Pulled latest changes for: %s" % gitDependency["url"])
        gitUpdate = True


def checkGitRepo(gitDependency):
    t1 = time.perf_counter()
    gitDirname = path.join(
        baseConfig["dependencies-path"], gitDependency["directory-name"])
    if (path.exists("%s" % (gitDirname))):
        pullGitRepo(gitDependency)
    else:
        cloneGitRepo(gitDependency)
    t2 = time.perf_counter()
    # print("%s took %s seconds" % (gitDependency, round(t2 - t1, 2)))


def checkGitDependencies(gitDependencies):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        try:
            executor.map(checkGitRepo, gitDependencies)
        except Exception as e:
            print(e)
    print("Git Dependencies: ✅")


def copyExternalDependencies(externalDependencies):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(copyExternalDependency, externalDependencies)
    print("External Dependencies: ✅")


def copyExternalDependency(externalDependency):
    try:
        externalDependency = externalDependency[getOperatingSystem(
        ).lower()]
    except Exception as e:
        return
    try:
        externalFileName = path.basename(externalDependency)
        # compare equality
        localFilePath = "%s/%s" % (
            baseConfig["dependencies-path"], externalFileName)
        updateDependency = True
        if (path.exists(localFilePath)):
            filesEqual = cmp(externalDependency, localFilePath)
            updateDependency = not filesEqual
        if (updateDependency):
            copyfile(externalDependency, localFilePath)
    except Exception as e:
        print(e)


def handleDependencies(args):
    method = args["method"]
    dependencies = args["dependencies"]
    method(dependencies)


def importDependencies():
    global gitUpdate

    dependencyJSON = None
    with open(baseConfig["dependencies"]) as file:
        dependencyJSON = json.load(file)
    print("Loading user dependencies now!")

    firstWaveDependencies = [
        {"method": checkGitDependencies,
         "dependencies": dependencyJSON["git"]},
        {"method": checkPipDependencies,
         "dependencies": dependencyJSON["pip"]},
        {"method": copyExternalDependencies,
         "dependencies": dependencyJSON["external"]},
        {"method": addEnvironmentVariables,
         "dependencies": dependencyJSON["environment-vars"]},
    ]

    secondWaveDependencies = [{"method": checkFileSystemDependencies,
                               "dependencies": dependencyJSON["file-system"]},
                              {"method": importPythonModules,
                               "dependencies": dependencyJSON["python"]}]

    with concurrent.futures.ThreadPoolExecutor() as executor:

        executor.map(handleDependencies, firstWaveDependencies)

        appendSysPath()

        p = executor.map(handleDependencies, secondWaveDependencies)
        l = list(p)
    if(gitUpdate):
        print("There was a git update detected.")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            appendSysPath()
            executor.map(handleDependencies, secondWaveDependencies)


def addEnvironmentVariables(environmentVars={}):
    try:
        environ.update(environmentVars)
    except:
        raise Exception("Error setting environment variables.")
    print("Environment Variables: ✅")


def checkFileSystemDependencies(fileSystemDependencies):
    chdir(baseConfig["dependencies-path"])
    for fileSystemDependency in fileSystemDependencies:
        if(path.exists(fileSystemDependency) == False):
            raise Exception("Error checking file system dependencies.")
    print("Filesystem dependencies: ✅")
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
    args = [{"pipPackage": pipPackage, "list": pipList}
            for pipPackage in pipPackages]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(checkPipDependency, args)
    print("Pip Dependencies: ✅")


def checkPipDependency(args):
    pipPackage = args["pipPackage"]
    pipList = args["list"]
    pipType = type(pipPackage)
    installCmd = ["pip", "install", "--quiet"]
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
        if (len(installCmd) > 3):
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
    startingTime = time.perf_counter()
    setup()
    loadBaseConfig()
    try:
        importDependencies()
        if(gitUpdate):
            print("There was a git update detected. Please rerun mokha")
            time.sleep("2")
            exit()
    except Exception as e:
        print(e)
        exit("Could not import dependencies correctly. Please check your config.")
    printDivider()
    accounts = loadJSON(baseConfig["accounts"])
    methods = loadJSON(baseConfig["methods"])
    kwargs = {"baseConfig": baseConfig, "accounts": accounts,
              "methods": methods, "modules": modules}
    mokhaEngine = modules["mokhaEngine"]
    print("Welcome to Mokha V2.0! {Booted in %s seconds(s)} This is a tool designed to enable configuration of shortcuts to python code." % (
        round(time.perf_counter() - startingTime, 2)))
    printDivider()
    mokhaEngine.main(**kwargs)
    time.sleep(1)


if (__name__ == "__main__"):
    main()
