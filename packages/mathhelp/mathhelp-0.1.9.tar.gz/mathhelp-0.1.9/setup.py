from distutils.core import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()



setup(
  name = 'mathhelp',         # How you named your package folder (MyLib)
  packages = ['mathhelp'],   # Chose the same as "name"
  version = '0.1.9',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Help for complex calculations, and homework',   # Give a short description about your library
  author = 'Ishan Roychowdhury',                   # Type in your name
  author_email = 'piklenews@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/hi101000/mathhelp',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/hi101000/mathhelp/releases/tag/v.0.1.9',    # I explain this later on
  keywords = ['Help', 'Math'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'scipy',
          'matplotlib'
          'matplotlib',
    ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
  long_description=long_description
)