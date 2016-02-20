aspath_graph
============

``aspath_graph`` converts raw ASPATHs to NetJSON Graph

.. image:: http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-2.png
   :target: http://www.wtfpl.net/
   :alt: Do what the fuck you want
   :height: 25px

NetJSON is a series of JSON schema for defining networks, NetJSON Graph
being specific to defining how nodes interconnect. "aspath_graph" uses
this to represent BGP autonomous systems as 'nodes' and how they connect
from the perspective of INPUT

INPUT can either be a device or file depending on value of MODE. This
defaults to a file. (txt)

OUTPUT can be '-' to send results to STDOUT.

If not passing '--nopassword', you will be prompted for a password for the
relevant modes.

When using "--asdot" to provide ASDOT notation, the raw ASPLAIN will also
be provided on the node - just under the "raw" attribute.

YAML can be formatted as such: (Note that "ignore" must ONLY be ASPLAIN)

.. code::yaml

    ---
    label_map:
        65001: SFO
        65002: ORD
        65003: NYC
        65003.1: NYC-R1
        65003.2: NYC-R2
    ignore:
        + 7224
        + 9059

By default, ASDOT will be labeled according to the firsthalf. Eg, if 65001
is configured to be labeled as DFW, 65001.211 will appear as DFW-R21. This
assumes your ToR ASN is your spine ASN + (racknumber*10+1) - to disable
this simply set APG_ASDOT_RAW to true/yes/anything.

Any of the supported options can be passed via ENV by upping the case,
replacing '-' with '_', and prefixing with 'APG'. Eg, 'APG_MODE'


Usage
-----

.. code::

    $ aspath_graph --help    Usage: aspath_graph [OPTIONS] INPUT

    Options:
      -v, --version                   Show the version and exit.
      -m, --mode [junos-netconf|txt]  Mode to use
      -o, --output FILENAME           Output file
      --asdot                         Whether to add ASDOT notation
      --ownas TEXT                    Apply perspective of own AS at the beginning
                                      of PATHS
      --runserver                     Run local server on 8000
      --user TEXT                     Only used for relevant modes
      --nopassword                    If using a login mode, this will enable
                                      public key auth
      --yaml FILENAME                 YAML for mapping and ignoring ASes
      --pprint                        Pretty print JSON
      -h, --help                      Show this message and exit.
