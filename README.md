# Propositional calculus satisfiability checker
A script that checks if a given formula is satisfiable
## Table of Content
1. [About](#about)
1. [Legend](#legend)
1. [Example](#example)
1. [How to use](#how-to-use)
1. [Tests](#tests)
## About
This script was created in order to solve the satisfiability problem. It outputs the formula in [disjunctive normal form](https://en.wikipedia.org/wiki/Disjunctive_normal_form)
and informs you whether it's satisfiable. The formula is not satisfiable if all of its elementary components contain a pair of opposite literals.  
To achieve it, the script applies suitable laws and definitions:
* Def. of implication
* Def. of equivalence
* DeMorgan's laws
* Double negation law
* Distributive law  
## Legend
Signs below represent logical conjunctions:
* `|`- disjunction (or)
* `&` - conjunction (and)
* `<>` - If and only if
* `>>` - implication
* `~` - negation
## Example
Here I'm gonna show how the script applies the laws and definitions on a simple example.  
Formula: `(p<>q)>>p&q`  
1. Def. of equivalence   
    `(p>>q)&(q>>p)>>p&q`
1. Def. of implication  
    `(~p|q)&(q>>p)>>p&q`
1. Def. of implication  
    `(~p|q)&(~q|p)>>p&q`
1. Def. of implication  
    `~[(~p|q)&(~q|p)]|(p&q)`
1. DeMorgan's laws   
    `~(~p|q)|~(~q|p)|(p&q)`  
1. DeMorgan's laws   
    `(p&~q)|~(~q|p)|(p&q)`  
1. DeMorgan's laws  
    `(p&~q)|(q&~p)|(p&q)`  
    
Formula is now in disjunctive normal form and the script proceeds to check if it's satisfiable.  
The verdict is that it is indeed satisfiable.
## How to use
It's very simple to use it as it doesn't require any 3rd party libraries. Script was written in Python 3.8.1. There's no formula validation so make sure you input a correct formula.
## Tests
There are tests written using unittest wchich are to ensure that any improvements or code refractoring won't generate wrong answers. There's 9 formulas wchich brings us to 54 unit tests.
