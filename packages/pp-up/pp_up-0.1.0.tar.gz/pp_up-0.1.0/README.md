pp-up
=====

Overview
--------
Script to update your dependencies by checking if there are new versions
available on pypi.

This script parses your requirements.txt and setup.py files, and updates any
pinned version you may have to the latest version available on pypi.

When you have a version pinned for a specific reason add `# pp_up: pin` to the line you want
to pin, this only works on requirements files example:

```
pp_up==0.0.1 # pp_up: pin
```

The files are backupped before modification.

Usage
-----
```bash
cd $YOUR_PROJECT_DIR
python -m pp_up
```
