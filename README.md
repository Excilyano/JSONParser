Please look at the README [there](https://excilyano.github.io/JSONParser/) !
Take a look at our [outputs](output/report/index_report.html) to have a hint of the result !
If you want to see the different elements we went through, please take a look at this [process](FLOW.md) document !

# JSONParser
JSONParser is a module meant to parse the JSON traces created by the execution of OpenStack's components.
The implementation currently creates a tree tracing the execution order of the stack.

## Implementation
There are four categories of information extracted from the JSON traces.
1. General information : this object contains information about the globality of the document (execution time, total number of requests...)
2. HTTP component : this object contains information about the HTTP request. It is necessary to get the execution stack of the application, as it is the root element of the tree, and may contain any kind of component as children.
3. Database component : this object contains information about the database requests. It is the most important element, as it lists which database was used, the duration of the request and information about the request itself.
4. Function component : this object contains information about the remaining elements, essentially about execution consistency.

## Dependencies
Before running the programm, you must install the dependencies specified in the [requirement](requirements.txt) file with the command :
```
pip install -r requirements.txt
```

## Run
Requires Python 3.0 or higher to run. Any lower version may work, but the consistency is not assured.

To run the program, make sure the directory [files](files) contains execution traces. You may use the following command line :
```
python main.py
```

## Output
The programm generates several things in the *output* directory :
  - logs :  textual information about what has been parsed in each trace under the [files](files) directory
  - report : global html report for each trace parsed
  - report/graphs : individual graphs generated which are combined to generate the full report

## Created by
* CASSIN Etienne
* DAVAZE Romain
* PELLETIER Flora
