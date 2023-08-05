#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from distutils.core import setup

setup(name='pantext',
      packages = ['pantext'],
      version= '0.0.1',
      description= 'text cleaning package for use on pandas dataframes and lists',
      url='https://github.com/halmga/pantext',
      download_url = 'https://github.com/halmga/pantext/archive/0.0.1.tar.gz',
      author='halmga',
      author_email="halm.gabriel@gmail.com",
      license='MIT',
      install_requires= ['pandas','nltk','tqdm'])
