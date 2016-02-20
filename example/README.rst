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


Once that's finished and you have an output file, let's check it out!

.. code::

    python2 -m SimpleHTTPServer 5001
      Serving HTTP on 0.0.0.0 port 5001 ...
      
      
Now point your browser at http://localhost:5001 and you should see the (albeit messy) product! Note that this is a half-example because the paths here are mostly meaningless to us, being a subsection of 1.0.0.0/12 PATHs. In your own environment, it can help you visualize perspective and you can also hide ASes that may make the graph look funky. (like AWS if you connect there in multiple ASes)
