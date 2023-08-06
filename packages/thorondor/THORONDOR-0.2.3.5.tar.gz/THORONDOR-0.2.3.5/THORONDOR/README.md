# Presentation of THORONDOR, a program for data analysis and treatment in NEXAFS

Authors : Simonne and Martini

#### The Program is meant to be imported as a python package, if you download it, please save the THORONDOR folder in ...\Anaconda3\Lib\site-packages
The installation command can be found here : https://pypi.org/project/THORONDOR/
There are two main classes at the core of THORONDOR:

Data should be of the same type, either .txt, .dat or .csv. Please use a comma instead of a dot as decimal separator.

### The class Dataset
A new instance of the Dataset class will be initialized for each Dataset saved in the data folder. This object is then saved in the list "ClassList", attribute of the second class "GUI".
For each Dataset, all the different dataframes that will be created as well as specific information e.g. $E_0$ the edge jump can be find as attributes of this class. Certain attributes are instanced directly with the class, such as:
* Name of Dataset
* Path of original dataset
* Timestamp

At the end of the data reduction, each Dataset should have at least three different data sets as attributes, saved as `pandas.DataFrame()`:
* df : Original data
* ShiftedDf : If one shifts the energy 
* ReducedDf : If one applies some background reduction or normalization method 
* ReducedDfSplines : If one applied the specific Splines background reduction and normalization method.

A Logbook entry might also be associated, under `Dataset.LogbookEntry`, this is done via the GUI, the logbook should be in the common excel formats.

It is possible to add commentaries for each Dataset by using the `Dataset.Comment()` and to specify some additional inf with the function `Dataset.AdditionalInfo()`.

Each Dataset can be retrieved by using the function Dataset.unpickle() with the path of the saved Class as an argument.

### The class GUI
This  class is a Graphical User Interface (GUI) that is meant to be used to process important amount of XAS datasets, that focus on similar energy range (same nb of points) and absorption edge.
There are two ways of initializing the procedure in a jupyter notebook:
* `GUI = THORONDOR.GUI()`; one will have to write the name of the data folder in which all his raw datasets are saved, in a .txt format.
* `GUI = THORONDOR.GUI.GetClassList(DataFolder = "<yourdatafolder>")` ;if one has already worked on a folder and wishes to retrieve his work.

This class makes extensive use of the ipywidgets and is thus meant to be used with a jupyter notebook. Additional informations are provided in the "ReadMe" tab of the GUI.

All the different attributes of this class can also be exported in a single hdf5 file using the pandas .to_hdf5 methods. They should be accessed using the read_hdf methods from pandas.

The necessary Python packages are : numpy, pandas, matplotlib, glob, errno, os, shutil, ipywidgets, IPython, scipy, datetime, importlib, pickle, lmfit, encee and inspect.

### FlowChart

![FlowChart](https://user-images.githubusercontent.com/51970962/81314649-aae0cd00-9089-11ea-9300-4c2e8ce47dc1.PNG)

### Tutorial

![Slide0](https://user-images.githubusercontent.com/51970962/80913188-01c16c00-8d43-11ea-812a-8f688d6b8707.PNG)
![Slide1](https://user-images.githubusercontent.com/51970962/81327644-e1bfde80-909b-11ea-9a4c-7c77c135e3f5.png)
![Slide2](https://user-images.githubusercontent.com/51970962/81314727-bf24ca00-9089-11ea-8fb0-0e679da491c3.PNG)
![Slide3](https://user-images.githubusercontent.com/51970962/81314767-c946c880-9089-11ea-9ed8-c64f3999a058.PNG)
![Slide4](https://user-images.githubusercontent.com/51970962/80913204-24538500-8d43-11ea-8da1-a92b3b774345.PNG)
![Slide5](https://user-images.githubusercontent.com/51970962/80913209-29b0cf80-8d43-11ea-8cd0-0ac539d19cd2.PNG)
![Slide6](https://user-images.githubusercontent.com/51970962/81314821-d5328a80-9089-11ea-81bc-d0505c6e8d66.PNG)
![Slide7](https://user-images.githubusercontent.com/51970962/80913211-2e758380-8d43-11ea-9aea-4a9428ab79c4.PNG)
![Slide8](https://user-images.githubusercontent.com/51970962/80913216-36cdbe80-8d43-11ea-9fb4-66ef5cba2468.PNG)
![Slide10](https://user-images.githubusercontent.com/51970962/80913217-3c2b0900-8d43-11ea-8fd4-2433d614bded.PNG)

### Please follow the following architecture when using the software


![Architecture1](https://user-images.githubusercontent.com/51970962/92746823-e36c1c80-f383-11ea-8850-79a7ab35b114.PNG)
![Architecture2](https://user-images.githubusercontent.com/51970962/92746753-d4856a00-f383-11ea-9b1c-6c05cc00423d.PNG)


### For users on Jupyter Lab, please follow this thread : https://stackoverflow.com/questions/49542417/how-to-get-ipywidgets-working-in-jupyter-lab