
===--------------===        ____
|                  |       /  _ \
| KhNoDe - Read me |       \ / _/ \
|                  |         \____/
===--------------===



==-------------------==
   Table of contents
==-------------------==

I.   Description
II.  Installation
III. Usage
IV.  Citation
V.   Contact
VI.  To do










==----------------==
   I. Description
==----------------==

This program determines when a given Khovanov homology class is nontrivial by verifying that a representative chain is not a boundary in the Khovanov chain complex. Moreover, it verifies that the chain is a cycle, and therefore, represents a homology class. To do this, the program populates the Khovanov chain complex with respect to the standard basis of generators (i.e., diagram smoothings whose components are labeled with 1 or x). The chain is expressed as a vector b with respect to the basis of the chain group in the relavent bigrading, say (h,q). The differential in the Khovanov chain complex has two relevant bigradings: we represent the differential (h-1,q)->(h,q) as a matrix A and the differential (h,q)->(h+1,q) as A'. We verify that the given chain is a cycle by showing A'b = 0. We use the linsolve method from SymPy to check for solutions to the equation Ax=b.

This program is written in Python and runs SymPy, which replaces the SageMath component from previous versions. In the past, SageMath would throw an error for links whose diagrams have more than 13 crossings (solving Ax=b produced memory allocation errors). We have not encountered the same behavior for the current version, however, a threshold has not been determined. It seems likely that SymPy runs a more efficient method, and in extreme cases, the user can increase memory allocation.

The GUI uses Tkinter. The current version is suitable for diagrams with a small number of crossings, and in future versions, we plan to fix the current scaling issues that make crossings difficult to see. Additional GUI improvements include: better labels for the enumerations (crossings, smoothings, components, smoothing components, etce) and smoothing labels. 










==----------------------------==
   II. Installation & Running
==----------------------------==

This program is supported for Windows machines running Python 3.9 or later - other operating systems running Python 3.9 or later have not been tested (though they are likely supported under similar installation methods). Installation files and instructions for Python can be found at [https://www.python.org/downloads/]

There are two ways to run KhNoDe, and installation varies between these options:

(A) use a Python IDE, such as PyCharm (recommended)
Download the individual files from the KhNoDe github repository and create a Python project. Verify that the SymPy module is installed (on PyCharm this can be done locally by hovering over the line 'import SymPy' in any of the .py files). Run the main.py file.

(B) use command prompt/terminal
Install SymPy on your machine; instructions can be found at [https://docs.sympy.org/latest/install.html]. Download the khnode.py file and place in a folder. In command prompt/terminal/whatever, move to the folder and run khnode.py










==------------==
   III. USAGE
==------------==




-----------------
III.i New Diagram
-----------------

To begin, the user inputs a diagram with File -> New Diagram. Here, the user traces a diagram with the arrow keys, beginning in the highlighted square. The user may translate the highlighted square by holding control and using the arrow keys. By default, overcrossings are created when two paths would intersect. To make undercrossings, hold shift when a crossing is made. Links can be created by translating the highlighted box to a new location and continuing drawing from there; there are two ways to translate the highlighted box: by pressing the return key when a component is complete and translating the highlighted square with control+arrow, or by entering a coordinate in the entry boxes (x and y) and moving the highlighted box to that square by pressing New Component. Finally, press Submit Diagram to have the diagram accepted.

[!] Avoid all unneccessary arrow keystrokes (e.g., do not backtrack on your diagram). Also, avoid unnecessary corners... diagrams are compressed when they have rows/columns that do not contain corners/crossings, so avoid staircases for the compression to work.

[!] Avoid parallel strands in adjacent rows/columns (the program does not handle crossing them well, as in the left of the figure below). Instead, leave an empty row/column between the parallel strands (as in the right of the figure)

          ------          ---|---             ------        ---|---
          ------    ->    ---|---                      ->      |
                                              ------        ---|---

[!] If it looks bad, it is bad (e.g., avoid corners touching).





--------------
III.ii Diagram
--------------

Once a diagram has been submitted, the main page will be populated. In the diagram section, you can view the diagram locally, or alternatively, a larger view is generated by clicking View Diagram. After viewing the diagram, you may wish to alter the diagram to your liking. First, the orientation of a single component may be reversed by inputting the component enumeration (visible in the View Diagram image) and pressing Change orientation. Second, the enumeration of the crossings can be changed by providing a new enumeration, where the entry should use the second line from Cauchy's two-line notation. For example, the permutation which switches the 2nd and 4th crossings has the following two-line notation:

   | 1 2 3 4 5 |
   | 1 4 3 2 5 |

The user would then enter 1,4,3,2,5 in the New order entry-box and press Re-enumerate.





------------------
III.iii Generators
------------------

Once the user is satisfied with the diagram, generators can be added. First, the user provides a binary sequence for the smoothing based on the enumeration of the crossings in the diagram. At this point, they may press Preview smoothing to see the smoothing with an enumeration of the components. Second, the user provides a label based on the enumeration of the strands in the smoothing. Finally, pressing Add generator will include this generator in the end of the list of generators provided by the user. These generators can be viewed on the left-most grid; the < and > keys will cycle through them. The user can view the currently visible generator by pressing View generator. Alternatively, they can delete it by pressing Remove generator.





------------
III.iv Chain
------------

Once all the desired generators g_i have been added, the user may provide a list of coefficients c_i for the generators (based on the order they are viewed on the Generators grid). Once the coefficients have been entered, a chain representing the sum c_i(g_i) is created. The bigrading will be automatically populated.

[!] The user should provide generators from a consistent bigrading. Nontriviality of a homology class consisting of generators from distinct bigradings can be determined by checking the nontriviality of the summands from distinct bigradings (i.e., if one is nontrivial, the class must be nontrivial).





---------------------------
III.v Cycles and Boundaries
---------------------------

In the final section of the main page, the user can check if the input chain is a cycle and/or a boundary. The answer will be automatically populated to the right of the buttons. In the case that the element is a boundary, a solution will be printed in the console. With the notation from the Description (above), the solution to Ax=b will be given as a row-vector

   x = | gen1  gen2  gen3  . . . |

where gen# represents the ith generator from the relevant bigrading. In certain cases, there are infinitely many solutions, and a list of symbols are provided to express the solution set. We give two examples: 

(1) a unique solution

      A = | 1  1 |      b = | 1 |
          | 0 -1 |          | 1 |

    the output will be

      gen1 = 2
      gen2 = -1

    So x = | 2  -1 |.

(2) a family of solutions

      A = | 1  1 |      b = | 1 |
          | 1  1 |          | 1 |

    the output will be

      gen1 = 1 - c2
      gen2 = c2

    Setting c2 = 0 gives x = | 1  0 |.
    
In the end, the interpretation of these solutions is up to the user. We still provide the user with access to the generators, namely, gen# can be accessed by entering the # into the entry box and pressing View boundary generator. The corresponding generator will be displayed in a separate window.





--------------------
III.vi Save and load
--------------------

The user may save and load diagrams and generators. Any changes in the enumeration/orientation will be lost in the process, but we plan to fix this in future versions.









==--------------==
   IV. Citation
==--------------==

Isaac Sundberg, KhNoDe, a program for determining nontriviality of Khovanov homology classes, 2023

Bibtex:
@software{handle, author = {Isaac Sundberg}, title = {KhNoDe, a program for determining nontriviality of Khovanov homology classes}, url = {imsundberg.github.io/KhNoDe}, version = {2.0}, date = {2023}}










==------------==
   V. Contact
==------------==

Please direct all feedback, bug reports, and questions to my email sundberg@mpim-bonn.mpg.de










==-----------==
   VI. To do
==-----------==

(1) Include enumerations and orientations into the save/load data
(2) Better support for displaying diagrams with many crossings
(3) Search option for nontrivial classes (with depth control on the chains in the search, based on (a) the number of generators and (b) the size of the coefficients)
(4) Option to toggle on/off the enumerations










Isaac Sundberg, 2023
