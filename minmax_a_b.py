#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 10:02:30 2018

@author: liujie
"""
import sys
import ast

class GameTree(object):
    statelist = []    
    childstates = dict()
    stateutility = dict()
    rootstate = None
    buildstatelist = []
    
    def __init__(self, statelist):
        self.buildGameTree(statelist[0], statelist[1:])
        self.rootstate = statelist[0]
        
    def appendChildState(self, rootstate, childstate):
        if(self.childstates.has_key(rootstate)):
            self.childstates[rootstate].append(childstate)
        else:
            self.childstates[rootstate] = [childstate]
            
    def addStateUtility(self, state, utility):
        self.stateutility[state] = float(utility)
        
    def getStateUtility(self, state):
        if(state in self.stateutility.keys()):
            return self.stateutility[state]
        else:
            return float("inf")

    def getChildStates(self, state):
        
        if(state in self.childstates.keys()):
            return self.childstates[state]
        else:
            return []
        
    def addStateNode(self, childstate):
        if childstate not in self.buildstatelist:
            self.buildstatelist.append(childstate)
             
    def buildGameTree(self, rootstate, statelist):
        self.addStateNode(rootstate)
        if(len(statelist) > 0 and statelist is not None):
           for state in statelist:
               if(type(state) is tuple):
                   childstate = state[0]
                   self.addStateNode(childstate)
                   self.appendChildState(rootstate, childstate)
                   self.addStateUtility(childstate, state[1])
               else:
                   childstate = state[0]
                   self.addStateNode(childstate)
                   self.appendChildState(rootstate, childstate)
                   state = self.buildGameTree(childstate, state[1:])
                   
    def terminalTest(self, state):
        if state in self.stateutility.keys():
            return True
        else:
            return False
        
        
class PlayGame(object):
    
    def __init__(self,gametree):
        self.gametree = gametree
        self.terminaltest = gametree.terminalTest
        self.utility = gametree.getStateUtility
        self.childstates = gametree.getChildStates
    
    # minamx without alpha-beta pruning    
    def minmaxDecision(self): 
        v = self.maxValue(self.gametree.rootstate)
        return v
    
    def maxValue(self, state):
        print state
        if self.terminaltest(state) == True:
            return self.utility(state)
        v = float("-inf")
        for state in self.childstates(state):
            v = max(v, self.minValue(state))
        return v
    
    def minValue(self, state):
        print state
        if self.terminaltest(state) == True:
            return self.utility(state)
        v = float("inf")
        for state in self.childstates(state):
            v = min(v, self.maxValue(state))
        return v
    
    # minmax with alpha-beta pruning
    
    def alphabetaMinmaxDecision(self):
        v = self.alphabetamaxValue(self.gametree.rootstate, float("-inf"), float("inf"))
        return v
    
    def alphabetamaxValue(self, state, alpha, beta):
        print state
        if self.terminaltest(state) == True:
            return self.utility(state)
        v = float("-inf")
        for state in self.childstates(state):
            v = max(v, self.alphabetaminValue(state, alpha, beta))
            if v > beta:
                return v
            alpha = max(alpha, v)
            
        return v
    
    def alphabetaminValue(self, state, alpha, beta):
        print state
        if self.terminaltest(state) == True:
            return self.utility(state)
        v = float("inf")
        for state in self.childstates(state):
            v = min(v, self.alphabetamaxValue(state, alpha, beta))
            if v <= beta:
                return v
            beta = min(beta, v)
            
        return v
               

# Parse the command line and generate a list of arguments
def parseArgument():
    arglist = []
    for arg in sys.argv:
      arglist.append(arg)
    return arglist

# Read the content from the input file
def readFileContent():
    inputfile = sys.argv[1]
    with open(inputfile, "r") as f:
        nodelist = ast.literal_eval(f.read())
    f.close()
    return nodelist

# Main function for minmax_a_b.py
if __name__ == '__main__':
           
      argumentlist = parseArgument()
      if len(argumentlist) != 2:
          print(" Enter the wrong arguments in the command line")
          exit(1)
      filecontent = readFileContent()
          
      gametree = GameTree(filecontent)
      playgame = PlayGame(gametree)
      
      print('The nodes visited for minmax is:')
      print('The utility of minmax is:' + str(playgame.minmaxDecision()))
      print('The nodes visited for minmax with alpha beta pruning is:')
      print('The utility of minmax with alpha beta pruning is:' + str(playgame.alphabetaMinmaxDecision()))

      
