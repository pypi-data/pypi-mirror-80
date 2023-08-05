from distutils.core import setup
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'django_json_error_response',
  packages = ['django_json_error_response'],
  version = '0.1',
  license='MIT',
  description = 'Json Response for http error codes',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Subodh Popalwar',
  author_email = 'subodhpopalwar.345@gmail.com',    
  url = 'https://github.com/subodh358/django_status_response',
  download_url = 'https://github.com/subodh358/django_status_response/archive/v_01.tar.gz',
  keywords = ['Django', 'HttpResponse', 'Response'],   
  install_requires=[            
          'django',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
