Init 
https://packaging.python.org/tutorials/packaging-projects/
https://setuptools.readthedocs.io/en/latest/setuptools.html

Steps to build and publish package
Build wheel:
python3 setup.py bdist_wheel

Install it locally:
pip3 install -e .

Source dist (tar ball):
python3 setup.py sdist

Simplified:
python3 setup.py bdist_wheel sdist