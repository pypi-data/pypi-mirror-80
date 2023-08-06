Optionset: parameter studies made easy
======================================

About Optionset
---------------

Optionset allows users to succinctly set up and conduct parameter studies for
applications that reference text-based dictionary files.

Author
------

Matthew C. Jones <matt.c.jones.aoe@gmail.com>

Installation
------------

The easiest way to install Optionset is with the Python package manager :code:`pip`:

.. code-block:: bash

    $ pip install optionset

Documentation
-------------

Basic Usage
^^^^^^^^^^^

The program enables and disables user-predefined options in text-based
dictionary files in the base directory and below.  The user specifies the lines
in the files that will either be enabled or disabled by adding macro commands
as commented text.

For example, suppose a parameter study involved varying fluid properties and
the kinematic viscosity was listed in a dictionary file as,

.. code-block:: cpp

    nu = 1.5e-5; // air [m^2/s]
    //nu = 1e-6; // water [m^2/s]

In the above text, the property of water will be ignored, since the second line
is commented out.  To enable water instead of air, the user could simply switch
which line is commented.  However, this task is often inconvenient, especially
with numerous variable properties listed across multiple files.  Alternatively,
the following macro instructions can be added to the commented part of the text
to mark them as a parameters to be varied.

.. code-block:: cpp

    nu = 1.5e-5; // air [m^2/s] ~nu air
    //nu = 1e-6; // water [m^2/s] ~nu water

This setup allows the user to easily switch between air and water simulations
without manually editing the dictionary file.  On the command line, simply run,

.. code-block:: bash

    $ optionset.py ~nu water

and the dictionary file will be modified and re-written as,

.. code-block:: cpp

    //nu = 1.5e-5; // air [m^2/s] ~nu air
    nu = 1e-6; // water [m^2/s] ~nu water

so that water is now the active property. Within the prescribed macros,
:code:`~nu` is the 'option' while :code:`air` and :code:`water` are the 'settings'.  An unlimited
number of unique options and settings are allowed.  Each can only be composed
of alphanumerical words with dots, pluses, minuses, and underscores, and
the first 1+ characters in the option must be a symbol such as :code:`~@$^&=|?`.

Use :code:`optionset.py -a` to view all of the options that you have set, or even
:code:`optionset.py -a ~nu` to view all options that begin with :code:`~nu`.  Additionally,
:code:`optionset.py -a -f` will show all options and their associated files.

Multi-line Options
^^^^^^^^^^^^^^^^^^

To avoid comment clutter, multi-line options are encouraged by annotating :code:`*`
in front of the first and last options in a series.  For example, suppose
a dictionary file specified a series of functions to run.

.. code-block:: cpp

    functions                   // ~functions on
    {                           // ~functions on
        #include "cuttingPlane" // ~functions on
        #include "streamLines"  // ~functions on
    }                           // ~functions on
    // // ~functions off

The five repeated macros could instead be written more succinctly as,

.. code-block:: cpp

    functions                   // *~functions on
    {
        #include "cuttingPlane"
        #include "streamLines"
    }                           // *~functions on
    //   // ~functions off

And running :code:`optionset.py ~functions off` would result in the following
modifications to the file, thereby disabling the functions.

.. code-block:: cpp

    //functions                   // *~functions on
    //{
    //    #include "cuttingPlane"
    //    #include "streamLines"
    //}                           // *~functions on
       // ~functions off

Variable Options
^^^^^^^^^^^^^^^^

An additional feature is the variable option.  For variable options the macro
command must be formatted with a Perl-styled regular expression :code:`='<regex>'`
that matches the desired text to be changed with parentheses :code:`()`, for example,

.. code-block:: cpp

    rho = 1.225; // ~varOptionRho ='rho = (.*);'

Here, :code:`(.*)` matches '1.225' in :code:`rho = 1.225;`.  To change :code:`rho` to '1025', run
:code:`optionset.py ~varOptionRho 1025`, and the line within the file now becomes,

.. code-block:: cpp

    rho = 1025; // ~varOptionRho ='rho = (.*);'

Bash Tab Completion
^^^^^^^^^^^^^^^^^^^

To enable Bash tab completion add the following lines to your :code:`~/.bashrc`,

.. code-block:: bash

    function os {
        optionset.py "$@" --bash-completion;
        source $HOME/.optionset/bash_completion;
    }

and run the program using :code:`os` instead of :code:`optionset.py`.

Scripting
^^^^^^^^^

Using your favorite scripting language, it is convenient to glue this program
into more advanced option variation routines to create parameter sweeps and
case studies.  While this program is generally called from the command line, it
is also possible to directly import this functionality into a Python script.

.. code-block:: python

    from optionset import optionset
    optionset(['~nu', 'water'])  # set kinematic viscosity to that of water

Command-Line Arguments
^^^^^^^^^^^^^^^^^^^^^^

For command line usage, the following arguments are permitted.

.. code-block:: bash

    positional arguments:
    option             'option' name
    setting            'setting' for given 'option'

    optional arguments:
    -h, --help         show this help message and exit
    -H, --help-full    show full help message and exit
    -a, --available    show available option-setting combinations; allows for
                        unix-style glob-expression searching; '-a' is implicitely
                        enabled when no 'setting' is input
    -f, --show-files   show files associate with available options
    -v, --verbose      turn on verbose output
    -q, --quiet        turn off all standard output
    -d, --debug        turn on debug output in log file
    -n, --no-log       do not write log file to
                        '$HOME/.optionset/log.optionset.py'
    --bash-completion  auto-generate bash tab-completion script
                        '$HOME/.optionset/bash_completion'
    --version          show version and exit


License
-------

Optionset is licensed under GNU GPLv3. See the LICENSE document.

See Also
--------

* `pyexpander`_: macro-processing with Python

.. _pyexpander: https://pypi.org/project/pyexpander/
