# RoVer
Transforming data generated tools like CA ARD, HP ALM to ALM Octane

## Purpose
This custom solution bridges the gap between widely known tools in the market, namely CA Agile Requirements Designer [ARD], HP Application Lifecycle Management [ALM] and MicroFocus ALM Octane.

Currently, CA ARD provides an integration capability with HP QC/ALM and automatically uploads the test cases generated from ARD to QC/ALM. However, CA ARD and does not integrate with the advanced version of QC/ALM, which is MicroFocus ALM Octane. Likewise, test cases in HP ALM cannot be directly fed into Octane. 

A custom solution is written in Python which reads the data generated from CA ARD or HP ALM [.xlsx], transforms and writes the data [.xlsx] to Octane undestandable format. The transformed data in [.xlsx] is further used for import into ALM Octane.

For the easy of usage, custom solution is wrapped as a standard python package using PYPI and made available as **da-rover**   

![RoVer](https://upload.wikimedia.org/wikipedia/commons/d/d3/Octane-transformer.jpg)


## Usage

#### Prerequisites
1. Python Interpreter to be installed on the machine where this utility is planned to be run. Python can be downloaded from https://www.python.org/downloads/

#### Installation
1. Run the following command to install the package
    
        pip install da-rover

#### Execution
1. Utility can be run using the command below

       rover

2. Use one of the command below to list the possible command line arguments

       rover -h
       rover --help

3. Usage 
    
        rover [-h] [-v] [-p PATH] [-s SOURCE] [-m MODULE] [-i INPUT] [-o OUTPUT]
   
        Arguments:

            -p PATH     Path of input and output files
            -s SOURCE   Source System of input file (ARD or ALM)
            -m MODULE   Source Module of input file (Tests or Defects)
            -i INPUT    Name of Input file
            -o OUTPUT   Name of Output file
          
3. Below are example commands

        rover -p C:/work -s ard -i ard.xlsx -o octane.xlsx
        rover -p C:/work -s alm -m tests -i alm.xlsx -o octane.xlsx
        rover -p C:/work -s alm -m defects -i alm.xlsx -o octane.xlsx
    
 
