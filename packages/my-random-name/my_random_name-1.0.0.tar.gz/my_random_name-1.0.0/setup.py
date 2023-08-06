from setuptools import find_packages, setup

setup(
    name ='my_random_name',
    version='1.0.0',
    author = 'maciagm',
    author_email = 'mmm@o2.pl',
    packeges = find_packages(),
    include_packege_data= True,
    description = 'Random Name',
    instal_requires =['names'],
)