# Finance Analytics

The Finance Analytics package is intended to be an open source, easily modifiable and configurable framework for relatively plug-and-play processing of personal finance data. Current functionality limited to extracting transactions from Bank Statements to output Excel file for users own analytics. Future development to contain out-of-the-box analytics to be applied to the output.

## How to Use

1) Set up the file and folder hierarchy
2) Run the application

### Setting Up the File and Folder Hierarchy
- The root folder can take on any name
- The child folder(s) directly under the root folder MUST be a supported Bank name (see current supported Banks below)
- Any number of subfolders below the Bank level are user defined to accommodate user defined dimensions
- The lowest level of folder should contain all PDF financial statements

Example folder structure:
* Root Folder
  * RBC
    * Chequing
      * Chequing Statement-0000 2000-01-11.pdf
      * Chequing Statement-0000 2000-02-14.pdf
      * Chequing Statement-0000 2000-03-12.pdf
      * Chequing Statement-0000 2000-04-16.pdf
    * Visa
      * Visa Statement-9999 2000-02-11.pdf
      * Visa Statement-9999 2000-03-10.pdf
      * Visa Statement-9999 2000-04-12.pdf
      * Visa Statement-9999 2000-05-07.pdf

### Running the Application
Navigate to the root folder of the cloned repo (FinanceAnalytics)

Run the following command in the command prompt / terminal
```
python main.py
``` 

## Listing of currently supported Bank-Products:
* RBC
  * Chequing
  * Visa

## Modules
The application is split into several modules for ease of enhancement and support as follows:
* Main
* Data Loader
* Data Quality
* Statement Processor

### Main Module
This module represents the interface between the application and the user. Currently, the interface is command prompt only, with intentions to extend to a graphical user interface.

### Data Loader
This module supports traversing the tree structure to determine the folder dimensions/hierarchy and translate this into a structured table for tagging dimensions to the extracted files. This structured table is also input to the Data Quality module.

### Data Quality
This module performs preliminary data quality assessment at the metadata level prior to extracting transaction data. This module will provide the user with simple completeness analytics, such as the range of statements for each dimension, as well as whether or not there are gaps in the statements which will cause data to be missing.

### Statement Processor
This module extracts transaction data from individual statements. Extraction is configured based on the Bank-Product combination and facilitated through PDF Plumber.

## Feature Enhancement Ideas / Roadmap
Refer to Issues for currently known bugs and core features to be added.

## Contributing
Contributing is currently open for:
* Feature additions/code
* Documentation
* DevOps/Deployment Pipelines
* Other ideas welcome

Pull requests required for any changes to the repo, no formalized process as of yet. Feel free to suggest enhancements or reach out for collaboration opportunities on the discussion board.