
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='storagemodel',
     version='0.1.3',
    #  scripts=['storagemodel', 'trainmodel'] ,
     author="Arvind Ravish",
     author_email="arvind.ravish@gmail.com",
     description="A simple Databricks package",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="",
     packages=['storagemodel'],  #setuptools.find_packages(),
      #  py_modules=['storagemodel'],
    install_requires=[
        'pandas', 'numpy', 'matplotlib', 'sklearn', 'joblib'
    ],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )