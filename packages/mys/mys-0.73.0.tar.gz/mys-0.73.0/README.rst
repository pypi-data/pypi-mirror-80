|buildstatus|_
|coverage|_

🐁 Mys
======

The Mys (/maɪs/) programming language - an attempt to create a
statically typed Python-like language that produces fast binaries.

Mys is heavily inspired by Python's syntax and Rust's packaging.

.. code-block:: python

   from random import random

   def main():
       print(random())

.. code-block:: toml

   [package]
   name = "robot"
   version = "0.1.0"

   [dependencies]
   random = "1.4.0"

Mys is mainly targeting resource constrained single and multi core
embedded systems.

Project homepage: https://github.com/eerimoq/mys

🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧
🚧 🚧 🚧 🚧 🚧 🚧 🚧

**IMPORTANT INFORMATION**

The language and build system implementation is still in a very early
stage. Some arithmetic, print and conditional statements works, but
not much more.

🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧
🚧 🚧 🚧 🚧 🚧 🚧 🚧

Quick start
-----------

.. image:: https://github.com/eerimoq/mys/raw/master/docs/quick-start.gif

Installation
------------

Install Python 3.6 or later, and then install Mys using ``pip``.

.. code-block:: python

   $ pip install mys

You must also have recent versions of ``g++``, ``make`` and
``pylint`` installed.

Tutorial
--------

First of all, create a package called ``foo`` with the command ``mys
new foo``, and then enter it. This package is used in throughout the
tutorial.

.. image:: https://github.com/eerimoq/mys/raw/master/docs/new.png

``src/main.mys`` implements the hello world application. This file is
only part of application packages (executables).

.. code-block:: python

   def main():
       print('Hello, world!')

Build and run the application with the command ``mys run``. It prints
``Hello, world!``, just as expected.

.. image:: https://github.com/eerimoq/mys/raw/master/docs/run.png

``src/lib.mys`` implements the function ``add()`` and it's test
``test_add()``. This file is normally part of both application and
library packages.

.. code-block:: python

   def add(first: int, second: int) -> int:
       return first + second

   @test
   def test_add():
       assert_eq(add(1, 2), 3)

Build and run the tests with the command ``mys test``.

.. image:: https://github.com/eerimoq/mys/raw/master/docs/test.png

Add the `bar package`_ as a dependency and use it's ``hello()``
function.

``package.toml`` with the ``bar`` dependency added:

.. code-block:: toml

   [package]
   name = "foo"
   version = "0.1.0"
   authors = ["Mys Lang <mys.lang@example.com>"]

   [dependencies]
   bar = "*"

``src/main.mys`` importing ``hello()`` from the ``bar`` module:

.. code-block:: python

   from bar import hello

   def main(args: [str]):
       hello(args[1])

Build and run the new application. Notice how the dependency is
downloaded and that ``mys run universe`` prints ``Hello, universe!``.

.. image:: https://github.com/eerimoq/mys/raw/master/docs/run-universe.png

Replace the code in ``src/main.mys`` with the code below. It
examplifies how to use functions, classes, exceptions, types and
command line arguments. The syntax is almost identical to Python, so
most readers should easily understand it.

**NOTE**: This code does not yet work. This is just an example of what
an application could look like in the future. The `Fibonacci example`_
works, so try that instead!

.. code-block:: python

   def func_1(a: i32) -> (i32, Final[str]):
       return 2 * a, 'Bar'

   def func_2(a: i32, b: i32 = 1) -> i32:
       for i in range(b):
           a += i * b

       return a

   def func_3(a: i32) -> {i32: [f32]}:
       return {
           1: [],
           10 * a: [7.5, -1.0]
       }

   def func_4():
       try:
           raise Exception()
       except:
           print('func_4():      An exception occurred.')

   class Calc:

       value: i32

       def triple(self):
           self.value *= 3

   def main(args: [str]):
       value = i32(args[1])
       print('func_1(value):', func_1(value))
       print('func_2(value):', func_2(value))
       print('func_3(value):', func_3(value))
       func_4()
       calc = Calc(value)
       calc.triple()
       print('calc:         ', calc)

Build and run it.

.. code-block::

   $ mys run 5
   func_1(value): (5, 'Bar')
   func_2(value): 7
   func_3(value): {1: [], 50: [7.5, -1,0]}
   func_4():      An exception occurred.
   calc:          Calc(value=15)

Built-in functions and classes
------------------------------

+----------------------------------------------------------------------------------------+
| Built-in functions and classes                                                         |
+=================+=================+=================+=================+================+
| ``abs()``       | ``all()``       | ``any()``       | ``bool()``      | ``bytes()``    |
+-----------------+-----------------+-----------------+-----------------+----------------+
| ``chr()``       | ``dict()``      | ``enumerate()`` | ``float()``     | ``format()``   |
+-----------------+-----------------+-----------------+-----------------+----------------+
| ``int()``       | ``len()``       | ``list()``      | ``max()``       | ``min()``      |
+-----------------+-----------------+-----------------+-----------------+----------------+
| ``open()``      | ``ord()``       | ``print()``     | ``range()``     | ``reversed()`` |
+-----------------+-----------------+-----------------+-----------------+----------------+
| ``round()``     | ``str()``       | ``sum()``       | ``tuple()``     | ``zip()``      |
+-----------------+-----------------+-----------------+-----------------+----------------+

All built-ins aims to behave like their Python counterparts, with the
following differences.

- ``abs()`` only supports integer and floating point numbers.

- ``all()`` and ``any()`` only supports lists of ``bool()``.

- ``min()`` and ``max()`` only supports lists of integer and floating
  point numbers, and a fixed number of integer and floating points
  parameters.

- ``sum()`` only supports lists of integer and floating point numbers.

Types
-----

Variables may all be set to ``None`` if declared
``Optional``. ``class`` variables may always be set to ``None``.

Variables declared ``Final`` can't be modified.

+-----------------------------------+-----------------------------------+-----------------------+----------------------------------------------------------+
| Type                              | Default value                     | Example               | Comment                                                  |
+===================================+===================================+=======================+==========================================================+
| ``i8``, ``i16``, ``i32``, ``i64`` | ``0``                             | ``1``, ``-1000``      | Signed integers of 8, 16, 32 and 64 bits.                |
+-----------------------------------+-----------------------------------+-----------------------+----------------------------------------------------------+
| ``u8``, ``u16``, ``u32``, ``u64`` | ``0``                             | ``1``, ``1000``       | Unsigned integers of 8, 16, 32 and 64 bits.              |
+-----------------------------------+-----------------------------------+-----------------------+----------------------------------------------------------+
| ``f32``, ``f64``                  | ``0.0``                           | ``5.5``, ``-100.0``   | Floating point numbers of 32 and 64 bits.                |
+-----------------------------------+-----------------------------------+-----------------------+----------------------------------------------------------+
| ``bool``                          | ``False``                         | ``True``, ``False``   | A boolean.                                               |
+-----------------------------------+-----------------------------------+-----------------------+----------------------------------------------------------+
| ``str``                           | ``''``                            | ``'Hi!'``             | A unicode string.                                        |
+-----------------------------------+-----------------------------------+-----------------------+----------------------------------------------------------+
| ``bytes``                         | ``b''``                           | ``b'\x00\x43'``       | A sequence of bytes.                                     |
+-----------------------------------+-----------------------------------+-----------------------+----------------------------------------------------------+
| ``tuple(T1, T2, ...)``            | ``(T1 default, T2 default, ...)`` | ``(5.0, 5, 'foo')``   | A tuple with items of types T1, T2, etc.                 |
+-----------------------------------+-----------------------------------+-----------------------+----------------------------------------------------------+
| ``list(T)``                       | ``[]``                            | ``[5, 10, 1]``        | A list with items of type T.                             |
+-----------------------------------+-----------------------------------+-----------------------+----------------------------------------------------------+
| ``dict(TK, TV)``                  | ``{}``                            | ``{5: 'a', -1: 'b'}`` | A dictionary with keys of type TK and values of type TV. |
+-----------------------------------+-----------------------------------+-----------------------+----------------------------------------------------------+
| ``class Name``                    | ``None``                          | ``Name()``            | A class.                                                 |
+-----------------------------------+-----------------------------------+-----------------------+----------------------------------------------------------+

Packages
--------

A package contains modules that other packages can use. All packages
contains a file called ``lib.mys``, which is imported from with ``from
<package> import <function/class/variable>``.

There are two kinds of packages; library packages and application
packages. The only difference is that application packages contains a
file called ``src/main.mys``, which contains the application entry
point ``def main(...)``. Application packages produces an executable
when built (``mys build``), libraries does not.

A package:

.. code-block:: text

   my-package/
   ├── LICENSE
   ├── package.toml
   ├── pylintrc
   ├── README.rst
   └── src/
       ├── lib.mys
       └── main.mys         # Only part of application packages.

The mys command line interface:

.. code-block:: text

   mys new      Create a new package.
   mys build    Build the appliaction.
   mys run      Build and run the application.
   mys test     Build and run tests.
   mys clean    Remove build output.
   mys lint     Perform static code analysis.
   mys publish  Publish a release.

Importing functions and classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Import functions, classes and variables from other packages with
``from <package>[[.<sub-package>]*.<module>] import
<function/class/variable>``.

Import functions, classes and variables from current package with
``from .+[[<sub-package>.]*<module>] import
<function/class/variable>``. One ``.`` per directory level.

Use ``from ... import ... as <name>`` to use a custom name.

Here are a few examples:

.. code-block:: python

   from mypkg1 import func1
   from mypkg2.subpkg1.mod1 import func2 as func3
   from mypkg2 import Class1
   from mypkg2 import var1
   from .mod1 import func4           # ../mod1.mys
   from ...mypkg3.mod1 import func5  # ../../../mypkg3/mod1.mys

   def foo():
       func1()
       func3()
       Class1()
       print(var1)
       func4()
       func5()

List of packages
^^^^^^^^^^^^^^^^

- `random`_ - Random numbers.

- `math`_ - Basic math operations.

- `time`_ - Date and time.

Extending Mys with C++
----------------------

Extending Mys with C++ is extremly easy and flexible. Strings that
starts with ``mys-embedded-c++`` are inserted at the same location in
the generated code.

.. code-block:: python

   def main():
       a: i32 = 0

       '''mys-embedded-c++

       i32 b = 2;
       a++;
       '''

       print('a + b:', a + b)

Memory management
-----------------

Integers and floating point numbers are allocated on the stack, passed
by value to functions and returned by value from functions, just as
any C++ program.

Strings, bytes, tuples, lists, dicts and classes are normally
allocated on the heap and managed by `C++ shared pointers`_. Objects
that are known not to outlive a function are allocated on the stack.

Reference cycles are not detected and will result in memory leaks.

There is no garbage collector.

Classes
-------

- Instance members are accessed with ``self.<variable/method>``.

- Overridden methods must be decorated with ``@override``.

- Automatically added methods (``__init__()``, ``__str__()``, ...)
  are only added if missing.

Below is a class with a data member ``value`` and a method
``inc()``.

The constructor ``def __init__(self, value: int = 0)`` (and more
methods) are automatically added to the class as they are missing.

.. code-block:: python

   class Foo:

       value: int

       def inc(self):
           self.value += 1

   def main():
       print('f1:')
       f1 = Foo()
       print(f1)
       f1.inc()
       print(f1)

       print('f2:')
       f2 = Foo(5)
       print(f2)

.. code-block:: text

   $ mys run
   f1:
   Foo(value=0)
   Foo(value=1)
   f2:
   Foo(value=5)

Build options
-------------

``--unsafe``: Disable runtime safety checks for faster and smaller
binaries. Disables ``None`` access checks, ``list()`` / ``str`` /
``bytes`` out of bounds checks and message ownership checks.

``--optimize {level}``: Optimize the build for given level. Optimizes
for speed by default.

Message passing
---------------

See `examples/wip/message_passing`_ for some ideas.

Major differences to Python
---------------------------

- All variables must have a known type at compile time. The same
  applies to function parameters and return value.

- Threads can run in parallel. No GIL exists.

  **WARNING**: Data races will occur when multiple threads uses a
  variable at the same time, which will likely make the program crash.

- Decorators does not exist.

- Variable function arguments ``*args`` and ``**kwargs`` are not
  supported, except to some built-in functions.

- Async is not supported.

- Generators are not supported.

- The majority of the standard library is not implemented.

- Dictionary keys must be integers, floats, strings or bytes.

- Strings, bytes and tuple items are **mutable** by default. Mark them
  as ``Final`` to make them immutable.

- Classes, functions and variables are public by default. Add a
  leading ``_`` to their name make them private.

- Lambda functions are not supported.

Text editor settings
--------------------

Visual Code
^^^^^^^^^^^

Use the Python language for ``*.mys`` files by modifying your
``files.associations`` setting.

See the `official Visual Code guide`_ for more detils.

.. code-block:: json

   "files.associations": {
       "*.mys": "python"
   }

Emacs
^^^^^

Use the Python mode for ``*.mys`` files by adding the following to
your ``.emacs`` configuration file.

.. code-block:: emacs

   (add-to-list 'auto-mode-alist '("\\.mys\\'" . python-mode))

Performance
-----------

ToDo: Create a benchmark and present its outcome in this section.

Build time
^^^^^^^^^^

Mys should be slower.

Runtime
^^^^^^^

Mys should be faster.

Memory usage
^^^^^^^^^^^^

Mys should use less memory.

Build process
-------------

``mys build``, ``mys run`` and ``mys test`` does the following:

#. Use Python's parser to transform the source code to an Abstract
   Syntax Tree (AST).

#. Generate C++ code from the AST.

   Probably generate three files:

   - ``<module>.mys.types.hpp``, which contains forward declarations
     of all types.

   - ``<module>.mys.hpp``, which contains all declarations.

   - ``<module>.mys.cpp``, which contains the implementation.

   Goals:

   - Only make methods virtual if overridden by another class.

#. Compile the C++ code with ``g++``.

#. Link the application with ``g++``.

.. |buildstatus| image:: https://travis-ci.com/eerimoq/mys.svg?branch=master
.. _buildstatus: https://travis-ci.com/eerimoq/mys

.. |coverage| image:: https://coveralls.io/repos/github/eerimoq/mys/badge.svg?branch=master
.. _coverage: https://coveralls.io/github/eerimoq/mys

.. _official Visual Code guide: https://code.visualstudio.com/docs/languages/overview#_adding-a-file-extension-to-a-language

.. _C++ shared pointers: https://en.cppreference.com/w/cpp/memory/shared_ptr

.. _examples: https://github.com/eerimoq/mys/tree/master/examples

.. _tests: https://github.com/eerimoq/mys/tree/master/tests/files

.. _Fibonacci example: https://github.com/eerimoq/mys/blob/master/examples/fibonacci/src/main.mys

.. _bar package: https://github.com/eerimoq/mys-bar

.. _examples/wip/message_passing: https://github.com/eerimoq/mys/tree/master/examples/wip/message_passing

.. _random: https://github.com/eerimoq/mys-random

.. _math: https://github.com/eerimoq/mys-math

.. _time: https://github.com/eerimoq/mys-time
