## Installation

### Clone and enter the repository

```
git clone git@github.com:MarcinKadziolka/grid.git
cd grid
```

### Create virtual environment and activate it

```
python3 -m venv .venv
source .venv/bin/activate
```

### Install required packages

```
pip install -r requirements.txt
```

### Move the script

Script must be placed into main project directory:
```
C:\Users\<username>\source\repos\WindowsApp\WindowsApp
```
```
├── WindowsApp
│   ├── WindowsApp
│   │   ├── **grid.py**
│   │   ├── dump
│   │   │   ├── save
│   │   ├── models
│   │   │   ├── <dataset_1>
│   │   │   ├── <dataset_2>
│   │   │   ├── <dataset_n>
│   │   ├── x64\
       .
       .
       .
│   │   ├── config.txt    
│   │   ├── WindowsApp.cpp
│   ├── x64
│   │   ├── Release
│   │   │   ├── WindowsApp.exe
```

### Run the program

```
python3 grid.py
```
