golpy is an implementation of Conway's Game of Life 
(and other life-like cellular automata)

Created as a student project to practice OOP and MVC with python.

Implemented in 'pure' python for that purpose.

Inspired by golly (https://sourceforge.net/projects/golly/)

created and maintained by dkuska

**USAGE:**

1. Create and activate venv
   `python -m venv .venv`
   `source .venv/bin/activate`


2. Install dependencies with:
   `pip install -r requirements.txt`

3. Go into the golpy directory and run main.py with your python interpreter
and the command line arguments you'd like to pass.
`python main.py -rule 3/23 -size 150`

**CMD Arguments:**

**-rule, -r:** The rulestring specifying the CA. 
    Supported formats are B0..8/S0..8 and B0..8/S0..8/C (Life-like and Generations)

**-mode, -m :** Specifyes the way the rulestring is to be interpreted.
    Currently not used.

**-size, -s :** Integer telling how many cells are on each of the axis of the universe. 
    Currently only square universes are allowed.

**-topology, -t:** String specifying the topology of the universe.
    Currently not used.

**-speed, -sp:** Integer specifying the maximum amount of FPS at which the animation runs.
    Default value = 30

**-windowsize, -w:** Integer specifying the dimensions of the window in pixels.
    Currently only square windows are permitted.

**-start, -st:** String specifing the starting configuration.
    Currently supported: soup, glider
