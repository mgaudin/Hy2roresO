Documentation
=========

Coming soon!

.. py:class:: Hydroreso(self, test)
    """Docstring for class Foo.

    This text tests for the formatting of docstrings generated from output
    ``sphinx.ext.autodoc``. Which contain reST, but sphinx nests it in the
    ``<dl>``, and ``<dt>`` tags. Also, ``<tt>`` is used for class, method names
    and etc, but those will *always* have the ``.descname`` or
    ``.descclassname`` class.

    Normal ``<tt>`` (like the <tt> I just wrote here) needs to be shown with
    the same style as anything else with ````this type of markup````.

    It's common for programmers to give a code example inside of their
    docstring::

        from test_py_module import Foo

        myclass = Foo()
        myclass.dothismethod('with this argument')
        myclass.flush()

        print(myclass)
    """

.. py:function:: make_stuff(val1, val2)
    
    Return the added values.
    
    :param val1: First number to add.
    :type val1: int
        
    :param val2: Second number to add.
    :type val2: int
    
    :return: Sum
    :rtype: int


.. py:method:: name(parameters)

.. py:attribute:: name
