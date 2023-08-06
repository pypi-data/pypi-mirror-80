Used
----

To use, simple do::

>>> from odinsupport import bump_version, read_json_file, write_json_file

Public python package
---------------------

>>> python3 setup.py sdist
>>> twine check dist/*
>>> twine upload dist/*