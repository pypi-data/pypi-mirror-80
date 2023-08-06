# Pyomc
Pyomc if the Python Object Model Compiler for making it easier to integrate Python scripts into your Java codebase so you can share properties between your Java and Python code.  
This command line tool takes in a config and directory of Python files and compiles them replaceing all instances of properties in the form of "${property.from.config.property.section}" into a target directory and runs the given entrypoint Python file.

### Usage 
```
$ pyomc --help
Usage: pyomc.py [OPTIONS] [FILE] [ARGS]...

Options:
  --directory TEXT  Directory to compile Python files from
  --target TEXT     Directory to save compiled Python files to
  --config TEXT     Location of config file to compile with
  --compile-only    Only compile files and don't run
  --help            Show this message and exit.

```

Example
```.env
pyomc my-python-app.py arg1
```

Defaults:  
```
--directory=./  
--target=./py-target  
--config=./pom.xml
```  


### Future tasks
- Accept java.properties file instead of pom in config flag  
- Add aliases  
- Add rc support  