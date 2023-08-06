## machine learning platform client SDK for python

### Update PyPI:

#####key: 
pypi-AgEIcHlwaS5vcmcCJDM2MTI5OGU3LTFjYWItNDRmMC05ZDQ1LTAzOWI4NjNmNjY2MgACJXsicGVybWlzc2lvbnMiOiAidXNlciIsICJ2ZXJzaW9uIjogMX0AAAYgQZWRSrMEPTnzvIJs07Xr9W43aAVJgaM37oe8ft_PHMs

#####command:
python3 setup.py sdist bdist_wheel

python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/* 

pip3 install --upgrade -i https://pypi.python.org/pypi ml-platform-client


