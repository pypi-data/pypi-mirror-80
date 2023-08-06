
import setuptools
#from setuptools import setup, find_packages


with open("README.md","r") as fh:
    long_description= fh.read()

setuptools.setup(
    name="TkOffice", # name
    version="0.0.1",
    author="Zin-Lin-Htun",
    author_email="zinlinhtun34@gmail.com",
    description='A Mordernised version of Tkinter, HighDPI for Windows 10, contains some new functions and widgets, Windows 10 exe development with Windows 10 looks ',
    long_description=long_description,
    #long_description_content_type="text/markdown",
    long_description_content_type="text/markdown",
    

    keywords="tkinter",
    install_requires=['Pillow','numpy'],

    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    #package_data={'ModTkinter':['ButDef.png'],'ModTkinter':[]},
    include_package_data = True,
    python_requires='>=3.8',
)


