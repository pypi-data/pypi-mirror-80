
# Global dependencies
import sys
import random
import numpy as np
import pandas as pd
from func_timeout import func_timeout, FunctionTimedOut
from tqdm import tqdm

###############################################################################
###############################################################################
###############################################################################


class EvolutionaryAlgorithm():

    ###############################################################################

    '''
    @param function <Callable>: a callable function whose output is to be minimized
    @param parameters <list>: a list of dictionary input parameters, with each dictionary specifying the name, bounds, and type of the parameter
    @param function_time <int>: the maximum number of seconds to wait for an input function to return an output
    @param algorithm_parameters <dict>: a set of parameters to be passed to the evolutionary algorithm (not to the function to be minimized), which control the evolutionary algorithm's behavior
    '''

    ###############################################################################

    # Initialize class object
    def __init__(self, function, parameters, function_timeout=10,
                 algorithm_parameters={'max_num_iteration': None,
                                       'population_size': 100,
                                       'mutation_probability': 0.1,
                                       'elite_ratio': 0.05,
                                       'crossover_probability': 0.5,
                                       'parents_portion': 0.3,
                                       'crossover_type': 'uniform',
                                       'max_iteration_without_improv': None}):

        # Declare class object name attribute
        self.__name__ = EvolutionaryAlgorithm

        # Declare function reference
        self.f = function

        # Set number of dimensions to be optimized over
        self.dim = int(len(list(parameters)))

        # Set input variable names
        # self.var_names = [[p['name']] for p in parameters]
        self.var_names = [p['name'] for p in parameters]

        # Check that parameters object is type dict
        assert(type(parameters) ==
               list), "Error: argument parameters must be a list"

        # Validate input: Check that each item in parameters is a dictionary
        for p in parameters:
            assert(type(p) ==
                   dict), "Error: parameters object must contain only dictionaries"

        # Validate input: Check each input parameter for expected type
        for p in parameters:
            assert(p['type'] in ['bool', 'int', 'float', 'cat']
                   ), "Error: unknown parameter type '{}'".format(p['type'])

        # Validate input: All parameters must have bound and types
        for p in parameters:
            assert(
                p['bounds']), "\nError: every parameter item must have bounds"
            assert(
                p['type']), "\nError: every parameter item must have an explicit type"

            if p['type'] == 'bool':
                assert(
                    p['bounds'] == [0, 1]), "\nError: type 'bool' can only have bounds [0, 1]"

            if p['type'] == 'cat':
                for k in p['bounds']:
                    assert(
                        type(k) == str), "\nError: type 'cat' must have strings as bounds"

        # Create variable bounds object
        self.var_bound = np.array([[x for x in p['bounds']]
                                   for p in parameters], dtype=object)

        # Variable type declaration
        self.var_type = np.array([p['type'] for p in parameters])
        # sys.stdout.write('\n' + str(self.var_type))

        # Set function timeout
        self.funtimeout = float(function_timeout)

        # Set evolutionary algorithm parameters
        self.param = algorithm_parameters

        # Set initial population size
        self.pop_s = int(self.param['population_size'])

        # Validate input: parent proportion must be between 0 and 1
        assert (0 <= self.param['parents_portion'] <=
                1), "\nError: argument 'parents_portion' must be in range [0,1]"

        # Select initial number of parents
        self.par_s = int(self.param['parents_portion'] * self.pop_s)
        trl = self.pop_s - self.par_s
        if trl % 2 != 0:
            self.par_s += 1

        # Set mutation probability
        self.prob_mut = self.param['mutation_probability']

        # Validate input: mutation probability rate must be between 0 and 1
        assert (self.prob_mut <= 1 and self.prob_mut >=
                0), "\nError: parameter 'mutation_probability' must be in range [0,1]"

        # Set & validate crossover rate probability
        self.prob_cross = self.param['crossover_probability']
        assert (self.prob_cross <= 1 and self.prob_cross >=
                0), "\nError: parameter 'crossover_probability' must be in range [0,1]"

        # Set & validate elite ratio
        assert (self.param['elite_ratio'] <= 1 and self.param['elite_ratio'] >= 0),\
            "\nError: parameter 'elite_ratio' must be in range [0,1]"
        trl = self.pop_s * self.param['elite_ratio']
        if trl < 1 and self.param['elite_ratio'] > 0:
            self.num_elit = 1
        else:
            self.num_elit = int(trl)
        assert(self.par_s >= self.num_elit), "\nError: number of parents must be greater than number of generational elites"

        # Set max number of iterations
        if self.param['max_num_iteration'] == None:
            self.iterate = 10
        else:
            self.iterate = int(self.param['max_num_iteration'])

        # Set crossover type
        self.crossover_type = self.param['crossover_type']
        assert (self.crossover_type == 'uniform' or self.crossover_type == 'one_point' or
                self.crossover_type == 'two_point'),\
            "\nError: parameter 'crossover_type' must be either 'uniform', 'one_point' or 'two_point'"

        # Set early stopping threshold
        self.stop_mniwi = False
        if self.param['max_iteration_without_improv'] == None:
            self.mniwi = self.iterate+1
        else:
            self.mniwi = int(self.param['max_iteration_without_improv'])

    ###################################################################################

    def run(self):

        ###############################################################################
        # Define initial population

        pop = []
        var = np.zeros(self.dim)

        for p in range(0, self.pop_s):
            vars = {i: np.nan for i in self.var_names}

            for i in range(self.dim):

                if self.var_type[i] == 'int':
                    val = np.random.randint(
                        self.var_bound[i][0], self.var_bound[i][1]+1)
                    vars[self.var_names[i]] = val

                elif self.var_type[i] == 'float':
                    val = self.var_bound[i][0]+np.random.random() * \
                        (self.var_bound[i][1]-self.var_bound[i][0])
                    vars[self.var_names[i]] = val

                elif self.var_type[i] == 'bool':
                    val = random.choice(self.var_bound[i])
                    vars[self.var_names[i]] = val

                elif self.var_type[i] == 'cat':
                    val = random.choice(self.var_bound[i])
                    vars[self.var_names[i]] = val

            # Evaluate fitness of initial population members
            obj = self.sim(vars)
            vars['OBJ'] = obj
            pop.append(vars)

        ###############################################################################
        # Report

        self.report = []
        self.test_obj = obj
        self.best_variable = {i: vars[i] for i in self.var_names}
        self.best_function = obj

        ###############################################################################
        # Main loop

        # Initialize counter for early stopping condition
        counter = 0

        # Begin evolution
        for t in tqdm(range(self.iterate)):

            # Break loop if max number of iterations without improvement is met
            if self.stop_mniwi:
                break

            # Sort population by fitness, ascending
            pop = sorted(pop, key=lambda k: k['OBJ'], reverse=False)

            if pop[0]['OBJ'] < self.best_function:
                counter = 0
                self.best_function = pop[0]['OBJ']
                self.best_variable = {i: pop[0][i]
                                      for i in self.var_names}
            else:
                counter += 1

            self.report.append(pop[0]['OBJ'])

            ##########################################################################
            # Normalize objective function

            normobj = np.zeros(self.pop_s)
            minobj = pop[0]['OBJ']
            if minobj < 0:
                normobj = pop[0]['OBJ'] + abs(minobj)
            else:
                normobj = pop[0]['OBJ'].copy()

            maxnorm = np.amax(normobj)
            normobj = maxnorm-normobj+1

            ##########################################################################
            # Calculate probability

            sum_normobj = np.sum(normobj)
            prob = np.zeros(self.pop_s)
            prob = normobj/sum_normobj
            cumprob = np.cumsum(prob)

            ##########################################################################
            # Select parents

            par = []

            for k in range(0, self.num_elit):
                par.append(pop[k].copy())
            for k in range(self.num_elit, self.par_s):
                index = np.searchsorted(cumprob, np.random.random())
                par.append(pop[index].copy())

            ef_par_list = []
            par_count = 0
            while par_count == 0:
                for k in range(0, self.par_s):
                    if np.random.random() <= self.prob_cross:
                        ef_par_list.append(k)
                        par_count += 1

            ef_par = [par[i] for i in ef_par_list]

            ##########################################################################
            # Next generation

            pop = []
            for k in range(0, self.par_s):
                pop.append(par[k])

            for k in range(self.par_s, self.pop_s, 2):
                r1 = np.random.randint(0, par_count)
                r2 = np.random.randint(0, par_count)
                pvar1 = ef_par[r1]
                pvar2 = ef_par[r2]

            ch = self.cross(pvar1, pvar2, self.crossover_type)
            ch1 = ch[0]
            ch2 = ch[1]

            ch1 = self.mut(ch1)
            ch2 = self.mutmidle(ch2, pvar1, pvar2)
            obj = self.sim(ch1)
            ch1['OBJ'] = obj
            pop.append(ch1)
            obj = self.sim(ch2)
            ch2['OBJ'] = obj
            pop.append(ch2)

            ##########################################################################

            if counter > self.mniwi:
                pop = sorted(pop, key=lambda k: k['OBJ'], reverse=False)

                if pop[0]['OBJ'] >= self.best_function:
                    t = self.iterate
                    t += 1
                    self.stop_mniwi = True

        pop = sorted(pop, key=lambda k: k['OBJ'], reverse=False)

        if pop[0]['OBJ'] < self.best_function:

            self.best_function = pop[0]['OBJ'].copy()
            self.best_variable = {i: pop[0][i] for i in self.var_names}

        self.report.append(pop[0]['OBJ'])
        self.output_dict = {'variable': self.best_variable, 'function':
                            self.best_function}
        self.best_parameters = self.best_variable

        # Write final results to stdout
        sys.stdout.flush()
        sys.stdout.write(
            'Best parameters found: {}'.format(str(self.best_parameters)))
        sys.stdout.flush()
        sys.stdout.write('\nBest objective output = {}'.format(
            str(self.best_function)))
        sys.stdout.flush()
        if self.stop_mniwi == True:
            sys.stdout.write(
                '\nTerminating algorithm: Exceeded maximum iterations without improvement.')

    ##############################################################################

    def cross(self, x, y, crossover_type):

        var = self.var_names

        ofs1 = {i: x[i] for i in self.var_names}
        ofs2 = {i: y[i] for i in self.var_names}

        if crossover_type == 'one_point':
            ran = np.random.randint(0, self.dim)

            for i in range(0, ran):
                ofs1[var[i]] = y[var[i]]
                ofs2[var[i]] = x[var[i]]

        if crossover_type == 'two_point':
            ran1 = np.random.randint(0, self.dim)
            ran2 = np.random.randint(ran1, self.dim)

            for i in range(ran1, ran2):
                ofs1[var[i]] = y[var[i]]
                ofs2[var[i]] = x[var[i]]

        if crossover_type == 'uniform':
            for i in self.var_names:
                ran = np.random.random()

                if ran < 0.5:
                    ofs1[i] = y[i]
                    ofs2[i] = x[i]

        return [ofs1, ofs2]

    ###############################################################################

    def mut(self, x):
        var = list(x)

        for i in range(self.dim):
            ran = np.random.random()

            if self.var_type[i] == 'int':
                if ran < self.prob_mut:
                    x[var[i]] = np.random.randint(self.var_bound[i][0],
                                                  self.var_bound[i][1]+1)

            elif self.var_type[i][0] == 'float':
                if ran < self.prob_mut:
                    x[var[i]] = self.var_bound[i][0]+np.random.random() *\
                        (self.var_bound[i][1]-self.var_bound[i][0])

            elif self.var_type[i][0] == 'bool':
                if ran < self.prob_mut:
                    x[var[i]] = random.choice(self.var_bound[i])

            elif self.var_type[i][0] == 'cat':
                if ran < self.prob_mut:
                    x[var[i]] = random.choice(self.var_bound[i])

        return x

    ###############################################################################

    def mutmidle(self, x, p1, p2):

        var = list(x)

        for i in range(len(self.var_type)):
            ran = np.random.random()

            # Integer vars
            if self.var_type[i] == 'int':
                if ran < self.prob_mut:
                    if p1[var[i]] < p2[var[i]]:
                        x[var[i]] = np.random.randint(p1[var[i]], p2[var[i]])
                    elif p1[var[i]] > p2[var[i]]:
                        x[var[i]] = np.random.randint(p2[var[i]], p1[var[i]])
                    else:
                        x[var[i]] = np.random.randint(self.var_bound[i][0],
                                                      self.var_bound[i][1]+1)

            # Float vars
            elif self.var_type[i] == 'float':
                if ran < self.prob_mut:
                    if p1[var[i]] < p2[var[i]]:
                        x[var[i]] = p1[var[i]]+np.random.random() *\
                            (p2[var[i]]-p1[var[i]])
                    elif p1[var[i]] > p2[var[i]]:
                        x[var[i]] = p2[var[i]]+np.random.random() *\
                            (p1[var[i]]-p2[var[i]])
                    else:
                        x[var[i]] = self.var_bound[i][0]+np.random.random() *\
                            (self.var_bound[i][1]-self.var_bound[i][0])

            # Boolean vars
            elif self.var_type[i] == 'bool':
                if ran < self.prob_mut:
                    if p1[var[i]] < p2[var[i]]:
                        x[var[i]] = p1[var[i]]+np.random.random() *\
                            (p2[var[i]]-p1[var[i]])
                    elif p1[var[i]] > p2[var[i]]:
                        x[var[i]] = p2[var[i]]+np.random.random() *\
                            (p1[var[i]]-p2[var[i]])
                    else:
                        x[var[i]] = random.choice(self.var_bound[i])

            # Categorical vars
            elif self.var_type[i] == 'cat':
                if ran < self.prob_mut:
                    x[var[i]] = random.choice(self.var_bound[i])

        return x

    ###############################################################################

    def evaluate(self):
        return self.f(self.temp)

    ###############################################################################

    def sim(self, X):
        self.temp = X.copy()
        obj = None

        try:
            obj = func_timeout(self.funtimeout, self.evaluate)

        except FunctionTimedOut:
            print("given function is not applicable")

        assert (obj != None), "Objective function failed to provide output within {} seconds".format(
            str(self.funtimeout))

        return obj

###############################################################################
###############################################################################
###############################################################################
