# ILS Telecom Network
An Iterated Local Search algorithm in Python, built for resolving a telecommunication network problem.
This project was part the "Networked Systems" course at the IMT Atlantique engineering school in 2020.

## What is the problem about ?
We want to find the cheapset way to build a network that connects a certain percentage of customers to each other, via end offices and digital hubs.
We have to choose the digital hubs and how we connect them to each other, we have to choose how we connect the end offices to the digital hubs, and finally how and which customers we connect to the end offices.
A complete explanation of the problem can be found in the problem_description directory.

## Why do we need an ILS ?
The small sized problem can be solved with the pulp python package, which gives us the optimal solution and score (the implementation is in petit_probleme_pulp.py), however this can't be done for the large problem, thus we need to think about some heuristic and metaheuristic algorithms to solve our problem.

## If you want more details for the algorithm
The Rapport_SER.pdf file contains a detailed explanation of our code in french.