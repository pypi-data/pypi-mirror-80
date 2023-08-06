# Python utilities for Gamayun

This is a package containing python utilities for writing Gamayun jobs. 
Main Gamayun repository can be found [here](https://github.com/ivan-brko/Gamayun).

## Contents
* [Getting the package](#getting-package)
* [Usage](#usage)
  * [Reporting results and errors](#reporting-results)
  * [Executing the script logic](#executing-script-logic)

<a name="getting-package"></a>
## Getting the package

Install the package with the following command:
```bash
pip3 install gamayun-utils
```

This package depends on gprcio, which needs C/C++ compilers installed on the system.
Needed dependencies on Alpine are:
```sh
apk add --no-cache python3 \
&& apk add --no-cache gcc \
&& apk add --no-cache g++ \
&& apk add --no-cache libc-dev \
&& apk add --no-cache linux-headers \
&& apk add --no-cache python3-dev
```
Note that suggested way of using Gamayun is by building a docker image based on Gamayun image, so you don't have to install these dependencies locally. See [Gamayun main repo](https://github.com/ivan-brko/Gamayun) for more information.

<a name="usage"></a>
## Usage
This part documents the package API

<a name="reporting-results"></a>
### Reporting results and errors

Functions for reporting results or errors from the script are following:

```python
def report_result(results)
```
```python
def report_error(error)
```

```report_result``` receives a list of strings which represent results and ```report_error``` receives a string which represents the error.

Note that once result or error is reported for the script/gamayun-job, Gamayun will stop listening for results/errors for that job, so in entire job there should be only one call to ```report_result``` or ```report_error```.

<a name="executing-script-logic"></a>
### Executing the script logic

There is a function with the following signature in this package:
```python 
def run_gamayun_script_logic(callback)
```

All the script logic should be placed in some function and that function should be given to ```run_gamayun_script_logic``` as argument as this will ensure that all uncought exceptions are cought and reported as errors to Gamayun. 

So, a job script file should look something like this:
```python
from gamayun_utils import report_result
from gamayun_utils import report_error
from gamayun_utils import run_gamayun_script_logic

def script_logic():
    # place the script logic here
    if OK:
        report_result(results)
    else:
        report_error(error)

run_gamayun_script_logic(script_logic)
```