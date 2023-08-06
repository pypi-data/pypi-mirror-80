from Hmm.HmmState cimport HmmState
from DataStructure.CounterHashMap cimport CounterHashMap
import math


cdef class Hmm(object):

    def calculatePi(self, observations: list):
        pass

    def calculateTransitionProbabilities(self, observations: list):
        pass

    def viterbi(self, s: list) -> list:
        pass

    def __init__(self, states: set, observations: list, emittedSymbols: list):
        """
        A constructor of Hmm class which takes a Set of states, an array of observations (which also
        consists of an array of states) and an array of instances (which also consists of an array of emitted symbols).
        The constructor initializes the state array with the set of states and uses observations and emitted symbols
        to calculate the emission probabilities for those states.

        PARAMETERS
        ----------
        states : set
            A Set of states, consisting of all possible states for this problem.
        observations : list
            An array of instances, where each instance consists of an array of states.
        emittedSymbols : list
            An array of instances, where each instance consists of an array of symbols.
        """
        cdef int i
        cdef dict emissionProbabilities
        i = 0
        self.stateCount = len(states)
        self.states = []
        self.stateIndexes = {}
        for state in states:
            self.stateIndexes[state] = i
            i = i + 1
        self.calculatePi(observations)
        for state in states:
            emissionProbabilities = self.calculateEmissionProbabilities(state, observations, emittedSymbols)
            self.states.append(HmmState(state, emissionProbabilities))
        self.calculateTransitionProbabilities(observations)

    cpdef dict calculateEmissionProbabilities(self, object state, list observations, list emittedSymbols):
        """
        calculateEmissionProbabilities calculates the emission probabilities for a specific state. The method takes the
        state, an array of observations (which also consists of an array of states) and an array of instances (which also
        consists of an array of emitted symbols).

        PARAMETERS
        ----------
        states : set
            A Set of states, consisting of all possible states for this problem.
        observations : list
            An array of instances, where each instance consists of an array of states.
        emittedSymbols : list
            An array of instances, where each instance consists of an array of symbols.

        RETURNS
        -------
        dict
            A HashMap. Emission probabilities for a single state. Contains a probability for each symbol emitted.
        """
        cdef CounterHashMap counts
        cdef dict emissionProbabilities
        cdef int i, j
        counts = CounterHashMap()
        emissionProbabilities = {}
        for i in range(len(observations)):
            for j in range(len(observations[i])):
                currentState = observations[i][j]
                currentSymbol = emittedSymbols[i][j]
                if currentState == state:
                    counts.put(currentSymbol)
        total = counts.sumOfCounts()
        for symbol in counts:
            emissionProbabilities[symbol] = counts[symbol] / total
        return emissionProbabilities

    cpdef double safeLog(self, double x):
        """
        safeLog calculates the logarithm of a number. If the number is less than 0, the logarithm is not defined, therefore
        the function returns -Infinity.

        PARAMETERS
        ----------
        x : float
            Input number

        RETURNS
        -------
        float
            The logarithm of x. If x < 0 return -infinity.
        """
        if x <= 0:
            return -1000
        else:
            return math.log(x)
