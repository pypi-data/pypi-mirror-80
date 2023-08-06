# Mission
* AutoML with aidb; keeps track of the moving parts of machine learning (model tuning, feature selection, and dataset splitting) so that data scientists can stay focused on data science.
* Local-first; empowers non-cloud users (academic/ institute HPCs, private cloud companies, desktop hackers, or even EC2 users) with the same quality ML services in their local IDE as present in the cloud (e.g. SageMaker).
* Integrated; it doesn’t force your entire workflow into the confines of a GUI app or specific IDE because it integrates with your existing scripts and tools.


### Functionality:
* Calculates and saves model metrics in local files.
* Visually compare model metrics to find the best model.
* Queue for hypertuning jobs and batches.
* Treats cross-validated splits (k-fold) and validation sets (3rd split) as first level citizens.
* Feature engineering to select the most informative columns.
* If you need to scale (data size, training time) just switch to `cloud_queue=True`.

---

# Installation:
Requires Python 3+. You will only need to do this the first time you use the package. Enter the following commands one-by-one and follow any instructions returned by the command prompt to resolve errors:

_Starting from the command line:_
```bash
$ pip install --upgrade pydatasci
$ python
```
_Once inside the Python shell:_
```python
>>> import pydatasci as pds
>>> pds.create_folder()
>>> pds.create_config()
>>> from pydatasci import aidb
>>> aidb.create_db()
```

PyDataSci makes use of `appdirs` for an operating system (OS) agnostic location to store configuration and database files. This not only keeps your `$HOME` directory clean, but also helps prevent careless users from deleting your database.

> The installation process checks not only that the corresponding appdirs folder exists on your system but also that you have permission to read from as well as write to that location. If these conditions are not met, then you will be provided instructions during the installation about how to create the folder and/ or grant yourself permissions necessary to do so. We have attempted to support both Windows (`icacls` permissions and backslashes `\\`, `\`) and POSIX including Mac, Linux (`chmod`permissions and slashes `/`). If you run into trouble with the installation process on your OS, please submit a GitHub issue so that we can attempt to resolve and release a fix as quickly as possible.

_Installation Location Based on OS_ `appdir.user_data_dir('pydatasci')`:
* Mac: `/Users/Username/Library/Application Support/pydatasci`
* Linux - Alpine and Ubuntu: `/root/.local/share/pydatasci`
* Windows: `C:\Users\Username\AppData\Local\pydatasci`


### Deleting & Recreating the Database:
When deleting the database, you need to either reload the aidb module or restart the Python shell before you can attempt to recreate the database.

```python
>>> aidb.delete_db(True)
>>> from importlib import reload
>>> reload(aidb)
>>> create_db()
```

---

# PyPI Package - Steps to Build & Upload:
```bash
$ pip3 install --upgrade wheel twine
$ python3 setup.py sdist bdist_wheel
$ python3 -m twine upload --repository pypi dist/*
$ rm -r build dist pydatasci.egg-info
# proactively update the version number in setup.py next time
$ pip install --upgrade pydatasci; pip install --upgrade pydatasci
```