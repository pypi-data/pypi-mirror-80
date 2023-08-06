import glob
import re
import subprocess
from collections import OrderedDict
from os import path, makedirs
from shutil import copyfile, rmtree
from typing import List

import click
import xmltodict

pyPathRegex = re.compile(r'(.*)\/.*.py')
propertyRegex = re.compile(r'.*\${(.*)}.*')

BLOCKLIST = ['setup.py', 'venv', 'py-target']


def printStep(step):
    def decorator(func):
        def wrapper(*args, **kwargs):
            click.echo(step)
            return func(*args, *kwargs)
        return wrapper
    return decorator


@click.command()
@click.option('--directory', default='./', help='Directory to compile Python files from')
@click.option('--target', default='./py-target', help='Directory to save compiled Python files to')
@click.option('--config', default='./pom.xml', help='Location of config file to compile with')
@click.option('--compile-only', is_flag=True, help='Only compile files and don\'t run')
@click.option('-r', is_flag=True, help='Run without compile')
@click.argument('file', nargs=-1, required=False)  # Maybe nargs will help
def pyomc(directory, target, config, compile_only, r, file):
    runOnly = r
    # Validation
    if (not compile_only or runOnly) and not file:
        click.echo('File path must be entered when running something.')
        click.echo('Ending pajama time.')
        return

    if runOnly:
        # Add validation for file and target directory
        click.echo("Run script.")
        run(target + '/' + file[0], file[1:])
    else:
        files = getPyFiles(directory, target)
        if files:
            # Delete target
            removeTarget(target)
            # Copy files to target folder
            copyFiles(files, target)
            # Parse pom for properties
            properties = parseXML(config)
            # Replace properties in target python files
            injectProperties(properties, target)
            click.echo('Compiling complete.')
            # Run py file
            if compile_only:
                click.echo('Skipping run.')
            else:
                click.echo("Run script.")
                run(target + '/' + file[0], file[1:])

            click.echo('Done.')
        else:
            click.echo('No files found.')


@printStep('Getting python files to compile...')
def getPyFiles(directory: str, target: str) -> List:
    # Optimize this to get less files
    files = getFiles(directory)
    # Make a filter function for files and accept an exclusion option
    files = [f for f in files if 'venv' not in f and target not in f and 'pyom' not in f]
    return files


def getFiles(directory: str) -> List:
    files = glob.glob(directory + '/**/*.py', recursive=True)
    return files


@printStep('Removing target directory...')
def removeTarget(target: str) -> None:
    if path.exists(target):
        rmtree(target)


@printStep('Copy python files to target directory...')
def copyFiles(files: List, target: str) -> None:
    for f in files:
        compileFile = target + f[1:]
        filePath = pyPathRegex.search(compileFile).group(1)
        if not path.exists(filePath):
            makedirs(filePath, exist_ok=True)
        copyfile(f, target + f[1:])


@printStep('Parsing xml...')
def parseXML(xmlfile: str) -> OrderedDict:
    with open(xmlfile) as fd:
        pom = xmltodict.parse(fd.read())
    return pom['project']['properties']


@printStep('Injecting properties...')
def injectProperties(properties: OrderedDict, directory: str) -> None:
    files = getFiles(directory)
    for f in files:
        # Think this would be better parsing each line and swapping files but this is easier for right now
        file1 = open(f, 'r')
        lines = file1.readlines()
        data = ''
        for line in lines:
            foundAllMatches = False
            while not foundAllMatches:
                regexMatch = propertyRegex.search(line)  # Gets the last one
                if regexMatch:
                    for group in regexMatch.groups():
                        try:
                            line = line.replace('${' + group + '}', properties.get(group))
                        except TypeError as error:
                            raise Exception('Property doesn\'t exist: ' + group)
                else:
                    foundAllMatches = True
            data = data + line
        file1.close()
        fin = open(f, "w")
        fin.write(data)
        fin.close()


@printStep('Running script...')
def run(file: str, params: list) -> None:
    subprocess.call('python ' + file + " " + ' '.join(params), shell=True)


if __name__ == "__main__":
    pyomc()
