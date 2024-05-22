from setuptools import setup,find_packages
from typing import List
def get_requirements(file_path:str)->List[str]:
    requirements=[]
    with open(file_path) as file:
        requirements=file.readlines()
        requirements=[req.replace('/n','')for req in requirements]
        
        if "-e ." in requirements:
            requirements.remove("-e .")
    return requirements
setup( 
    name='ml_flow', 
    version='0.0.1', 
    description='A sample ml workflow', 
    author='Adithya', 
    author_email='adithyakalidindi25@icloud.com', 
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    
) 