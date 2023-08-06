import setuptools
import io

def parse_requirements_file(filename):
    with io.open(filename, encoding="utf-8") as fid:
        requires = [l.strip() for l in fid.readlines() if l]
    return requires

install_requires = parse_requirements_file("requirements.txt")

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Python-EasyGraph",                                     
    version="0.2a7",                                        
    author="Fudan MSN Group",                                       
    author_email="easygraph@163.com",                      
    description="Easy Graph",                            
    long_description=long_description,                      
    long_description_content_type="text/x-rst",          
    url="https://github.com/easy-graph/Easy-Graph",                              
    packages=setuptools.find_packages(),                    
    classifiers=[                                           
        "Programming Language :: Python :: 3",              
        "License :: OSI Approved :: BSD License",           
        "Operating System :: OS Independent",               
    ],
    install_requires=install_requires,
)

