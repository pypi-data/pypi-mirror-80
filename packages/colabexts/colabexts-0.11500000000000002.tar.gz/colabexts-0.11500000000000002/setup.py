from setuptools import setup

version=0.11500000000000002

setup(name='colabexts', 
      version=str(version), 
      description='Some simple Utilities',
      url='https://github.com/meyers007/labext.git',
      author='Code Red',
      author_email='meyers@geospaces.org',
      license='Apache License 2.0',
      packages = ['colabexts'],
      package_data={'colabexts':['*', 'imgs/*']},
      zip_safe=False,
      install_requires=['matplotlib', 'openpyxl'],
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',
            
          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          #'Topic :: Jupyter Prettification :: Utilities ',
      
          # Pick your license as you wish (should match "license" above)
           'License :: OSI Approved :: Apache Software License',
      
          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          #'Programming Language :: Python :: 2',
          #'Programming Language :: Python :: 2.6',
          #'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
)
