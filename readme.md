golpy is an implementation of Conway's Game of Life (and other life-like cellular automata) using python

Created as a student project to practice OOP and MVC with python.
Implemented in 'pure' python for that purpose

much thanks to golly (https://sourceforge.net/projects/golly/) for inspiration

created and maintained by dkuska


CMD Arguments:

-rule, -r: The rulestring specifying the CA. 
            Supported formats are B0..8/S0..8 and B0..8/S0..8/C
-mode, -m : Specifyes the way the rulestring is to be interpreted.
            Currently not used.
-size, -s : Integer telling how many cells are on each of the axis of the universe. 
            Currently only square universes are permitted.
-topology, -t: String specifying the topology of the universe. 
            Currently supported formats: torus
-speed, -sp: Integer specifying the maximum amount of FPS at which the animation runs.
            Default value = 30
-windowsize, -w: Integer specifying the dimensions of the window in pixels. 
            Currently only square windows are permitted.
