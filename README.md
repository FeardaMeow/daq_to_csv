# Converts DAQ files from the NADS driving simulators to CSV

An implementation of a full data pipeline for converting DAQ files to csv.

## Prerequisites
```python
python==2.7+
numpy==1.14.6
pandas==0.24.2
undaqTools==0.2.3
```

## Installing
Download the read_daq.py

## Usage
The script takes two command line arguements. First, '-dir' the directory where the DAQ files are located. Second, '-elemlist' a text file with the variable names to save to csv, with each variable name on a seperate line. The script will save a CSV at the same folder level where it finds DAQ files.
```
$ python read_daq.py -dir test_sample -elemlist elemlist.txt
Trying to read Voice_20150526095528.daq
Trying to read Voice_20150521095047.daq
Trying to read Voice_20150526093624.daq
Trying to read Voice_20150521093225.daq
```
