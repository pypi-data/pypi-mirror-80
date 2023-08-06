# Loci for dynamics epidemic model
#
# Copyright (C) 2017--2020 Simon Dobson
# 
# This file is part of epydemic, epidemic network simulations in Python.
#
# epydemic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# epydemic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with epydemic. If not, see <http://www.gnu.org/licenses/gpl.html>.

import random

class Locus(object):
    '''The locus of dynamics, where changes can happen. Loci
    are filled with nodes or edges from a network and represent some (possibly
    complete) sub-set of the elements, typically being populated and re-populated as
    a process over the network evolves. A locus is basically a set with
    some additional methods to allow or more complex behaviours, including
    customisable drawing random selection of elements.

    :param name: the locus name'''

    def __init__( self, name ):
        super(Locus, self).__init__()
        self._name = name
        self._elements = set()

    def name( self ):
        '''Returns the name of the locus.

        :returns: the locus' name'''
        return self._name

    def __len__( self ):
        '''Return the number of elements at the locus.

        :returns: the number of elements'''
        return len(self.elements())

    def elements( self ):
        '''Return the underlying elements of the locus.

        :returns: the elements'''
        return self._elements
    
    def draw(self):
        '''Draw a random element from the locus. The default performs a simple
        draw that is equiprobable across all the elements. The locus remains unchanged:
        drawing simply selects and returns an element at random.

        :returns: a random element at the locus'''
        if len(self) == 0:
            raise ValueError('Trying to draw element from empty locus {n}'.format(n = self.name()))
        e = random.choice(list(self.elements()))
        return e


    # ---------- Handlers ----------

    def addHandler(self, g, e):
        '''Handler called when an element is added to the network. This is used to indicate
        the the population of nodes or edges has changed.

        :param g: the network
        :param e: the element'''
        self._elements.add(e)

    def leaveHandler( self, g, e ):
        '''Handler for when an element leaves the locus due to changes in circumstances,
        not changes in population.

        :param g: the network
        :param e: the element'''
        self._elements.discard(e)

    def enterHandler( self, g, e ):
        '''Handler for when an element enters the locus due to changes in circumstances,
        not changes in population. 

        :param g: the network
        :param e: the element'''
        self._elements.add(e)

    def removeHandler(self, g, e):
        '''Handler called when an element is removed from the network.  This is used to indicate
        the the population of nodes or edges has changed.

        :param g: the network
        :param e: the element'''
        self._elements.discard(e)

