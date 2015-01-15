In-house Development
--------------------

*Tested on Bragg-l, but should also work in other environments* Note
that Sambuca development is using virtual environments to facilitate
testing and development. To enable use of the optimised numpy and scipy
packages, the virtual environment is created
with --system-site-packages. However, for testing the package
installation and dependencies, a clean virtual environment should be
used. The goal is to create a Sambuca package that will install cleanly
using standard Python tools and have it "just work".

### Once only

1.  load the git module :

    > \$ module load git

2.  Setup virtualenvwrapper by adding the following 2 lines to your
    .bashrc (substituting your own desired locations) :

    > export WORKON\_HOME=\$HOME/.virtualenvs export
    > PROJECT\_HOME=\~/projects

3.  If they don't already exist, create the .virtualenvs and projects
    directories specified in the previous step.
4.  Create a directory in projects to act as the top level sambuca
    directory :

    > \$ cd \~/projects/ 
    > \$ mkdir sambuca\_project

5.  Clone the Git repositories for sambuca and sambuca\_agdc into the
    sambuca\_project directory :

    > \$ cd \~/projects/sambuca\_project/ 
    > \$ git clone
    > <https://col52j@stash.csiro.au/scm/~col52j/sambuca.git> 
    > \$ git
    > clone <https://col52j@stash.csiro.au/scm/~col52j/sambuca_agdc.git>

6.  Load the Python version used for development :

    > \$ module load python/2.7.6

7.  Activate the virtualenvwrapper scripts :

    > \$ source /apps/python/2.7.6/bin/virtualenvwrapper\_lazy.sh

8.  Change to the top-level sambuca project directory :

    > \$ cd \~/projects/sambuca\_project/

9.  Make a virtual environment called sambuca that will be shared by
    sambuca and sambuca\_agdc, associate it with the project directory,
    and allow the virtual environment to access the system site packages
    (required for access to site-optimised packages like numpy and
    scipy). :

    > \$ mkvirtualenv -a . --system-site-packages sambuca

10. Install the sambuca and sambuca\_agdc packages into your virtual
    environment in development mode. This makes the packages available
    via symlinks to your development code, so that code changes are
    reflected in the package without reinstallation (although you need
    to restart your python environment, or use the IPython %autoreload
    extension) :

    > \$ workon sambuca 
    > \$ cdproject 
    > \$ python setup.py develop

11. Install additional packages specified in the setup.py script :

    > \$ cd sambuca 
    > \$ pip install --upgrade -e.[dev,test] 
    > \$ cd ../sambuca\_agdc 
    > \$ pip install --upgrade -e.[dev,test]

### Every time

1.  Load the Python version used for development :

    > \$ module load python/2.7.6

2.  Activate the virtualenvwrapper scripts :

    > \$ source /apps/python/2.7.6/bin/virtualenvwrapper\_lazy.sh

3.  Activate the sambuca virtual environment :

    > \$ workon sambuca

4.  You can now work on the sambuca python code. Any Python packages you
    install with pip will be installed into the virtual environment.
    System packages are still available.
5.  To deactivate the virtual environment, simply use the
    virtualenvwrapper command (or simply close the terminal window) :

    > \$ deactivate

Testing
-------

-   Tests are implemented with pytest, with integration into the
    setup.py script. The simplest way to run the tests is to call
    py.test from the project directory :

    > \$ py.test

-   The tox framework was tested, as it provides automated testing
    against multiple Python versions (2 & 3). However, tox did not work
    correctly with the system-site-packages setting. The
    system-site-packages setting is required to access the system
    packages numpy and scipy. Compiling these packages is difficult and
    makes the use of fully encapsulated virtual enviroments
    problematic. - A workaround is to create separate virtual
    environments based on Python 2.7 and Python 3.4, and then run the
    tests within both environments. A helper script makes this easier.
