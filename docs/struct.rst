Structure
==================================

.. graphviz::

    digraph G {
    rankdir=LR;
    node [fontsize=8,style=filled, fillcolor=white];
    fontsize=8;

    subgraph cluster_0 {
        label = "PyVirtualDisplay";
        style=filled;
        subgraph cluster_2 {
            style=filled;
            fillcolor=white;
            label = "wrappers";

            XvfbDisplay;
            XephyrDisplay;
        }
        Display -> XvfbDisplay;
        Display -> XephyrDisplay;
    }
    XvfbDisplay -> Xvfb;
    XephyrDisplay -> Xephyr;

    application -> Display;


    }
