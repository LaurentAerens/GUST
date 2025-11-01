# Project Plan for GUST

## Vision
GUST (Genetic Universal Stockfish Trainer) aims to be a tool that leverages genetic algorithms to optimize and train Stockfish/ make a stockfish nnue or really any nural network (i think the stockfish bit can be done later as i but i needed it for the acronim)

## how it should work

so some the user defines a nn structure, how many nodes on what layer or default stofish arch (for later)
the programm generates a x amount of nn with random values 
the programm loads in a list of engines with there elo (just link to exe file)
the nn play against the engines if the engine they go up against a higher level (the nn is really only scoring a chess position so the programm need to generates all possible moves and pick the one the nn has rated highest)
if they win they get 10 points and move on to the next, lose there streak stops, draw is one point but you also move on.

then the population get's ranked. based on setting the higher you end up the higer your changes of survival (a setting determains how much of the population survives)
then based  on other settings part of the next population is (the engines that survived), some mutation of the survived engines and some childeren that are a combinarion of 2 surviving engines. only the top engine get to put mutations in the later population

some improvments
1) define a minimal level (once 80% or so passed an engine start for there to safe time)
2) start with an existing nn and the population is just a bunch of mutation of that nn
