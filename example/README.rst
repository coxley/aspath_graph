Example
-------

In this directory, there are:

* ``paths.txt``: Contains newline-delimited ASPATHs
* ``example.yaml``: Used for labeling well-known ASes and ignoring others
* ``index.html``: Some netjsongraph.js boilerplate, set to use
  ``./example.json`` which we will generate


Running ``aspath_graph --help`` will remind you what options are available. For
this situation, our ``mode`` will be txt, ``INPUT`` will be paths.txt, and
we'll ``output`` to example.json.


.. code::

    aspath_graph paths.txt -m txt -o example.json --yaml config.yaml
