import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Python-EasyGraph",                                     
    version="0.2a3",                                        
    author="Fudan MSN Group",                                       
    author_email="easygraph@163.com",                      
    description="Easy Graph",                            
    long_description=long_description,                      
    long_description_content_type="text/markdown",          
    url="https://github.com/easy-graph/Easy-Graph",                              
    packages=setuptools.find_packages(),                    
    classifiers=[                                           
        "Programming Language :: Python :: 3",              
        "License :: OSI Approved :: BSD License",           
        "Operating System :: OS Independent",               
    ],
)

