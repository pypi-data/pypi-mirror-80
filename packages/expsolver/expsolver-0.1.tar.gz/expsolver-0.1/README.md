
### Table of Contents

1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [Algorithm](#algorithm)
4. [File Descriptions](#files)
5. [Inputs and Outputs](#inputoutput)
6. [Example code](#example)
7. [Limitations](#limitations)
8. [Improvements](#improvements)
9. [Licensing, Authors, and Acknowledgements](#licensing)

## Installation <a name="installation"></a>

The code was developed using <b>Python version 3.6.11.</b><br>

## Project Motivation<a name="motivation"></a>

<b>The intent is to solve multiple kinds of equations (expression = 0) efficiently and return: </b><br>
1. Roots
2. Local maxima
3. Local minima

## Algorithm <a name="algorithm"></a>

The basic logic consists of moving two brackets of x values, one in negative and the other in the
positive direction and checking for roots, maxima and minima. The psuedocode is as below: <br>

Determining order of equation: <br>
1. IF "**" in expression, find the highest value following the "**" as order
2. Else if "*x" in expression, order is 1
3. Else if "x" in expression, order is 1
4. Else order is zero
5. If any execption occurs in steps "a" through "d"
   If "x" in expresssion, order= 10
   else order = 0
Order of expression is used to calculate the tolerance (xtol and ytol),since for higher orders,
small changes in "x" can result in significant changes in expression value

Determining roots of equation: </br>
1. Find a semi-random starting "x" value as a function of order
2. create a list of "x" values (xlist) as [x, x+tol, x, x-tol]
3. Evaluate exp for xlist to obtain ylist
4. If ylist has a zero, append the x value to roots list
5. If ylist[0]*ylist[1] < 0 indicating the root lies between xlist[0] and xlist[1]
   add the arithmetic mean of xlist[0] and xlist[1] to roots
6. If ylist[2]*ylist[3] < 0 indicating the root lies between xlist[2] and xlist[3]
   add the arithmetic mean of xlist[2] and xlist[3] to roots
7. Else make xlist as [x=x+tol, x+tol=x+2*tol, x=x-tol, x-tol=x-2*tol]
8. Repeat steps a through f for a certain number of times (a large value, based on xtol)
9. Change xtol = xtol / order and repeat step h till exp(roots) is within ytol around zero

Determining maxima and minima:</br>
 1. If the difference in ylist[0] and ylist[1] from ylist goes from negative to positive,
    add xlist[0] to minima 
 2. If the difference in ylist[0] and ylist[1] from ylist goes from positive to negative,
    add xlist[0] to maxima 
 3. If the difference in ylist[2] and ylist[3] from ylist goes from negative to positive,
    add xlist[2] to minima 
 4. If the difference in ylist[2] and ylist[3] from ylist goes from positive to negative,
    add xlist[2] to maxima  

## File Descriptions <a name="files"></a>

The important files include: <br>
1. expsolver.py: The "Solver" class

## Inputs and Outputs <a name="inputoutput"></a>

<b>Inputs:</b><br>
1. exp: expression to be solved e.g. 2*x**2+3*x-100=0
<b>Solve:</b><br>
1. solve(): solves for "exp = 0"
<b>Outputs:</b><br>
1. get_order(): Integer order of equation "exp=0"
2. get_root(): List of roots for "exp=0"
3. get_delta(): List of "0-exp(root)"
4. get_minima(): List of local minima
5. get_maxima(): List of local maxima

## Example Code<a name="example"></a>

<b>Code snippet:</b><br> 
from expsolver import Solver as solver <br>
exp='x**3-2*x**2-3*x-100' # Expression to be solved <br>
solv_obj=solver(exp)  # Solver object exp <br>
solv_obj.solve() # Solve exp <br>

<b>Results:</b><br>
solv_obj.get_order() <br>
2 <br>
solv_obj.get_maxima() <br>
[-0.5375000000000474] <br>
solv_obj.get_roots() <br>
[5.65625] <br>
solv_obj.get_delta() <br>
[-0.006256103515625] <br>
solv_obj.get_minima() <br>
[1.8624999999999483] <br>

## Limitations<a name="limitations"></a>
1. Currently cannot solve advanced functions from the math library
2. May be unable to compute very large roots
3. May return multiple roots for root / maxima/minima values too close to each other

## Improvements<a name="improvements"></a>
1. Modified to include math functions
2. Efficiency can be improved by optimizing tolerances and tolerance based iteration logic

## Licensing, Authors, Acknowledgements<a name="licensing"></a>

For licensing information check the LICENSE file <br>
[Link to Github]https://github.com/kgraghav/expsolver/

