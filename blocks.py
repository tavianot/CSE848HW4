# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 13:43:30 2017

@author: Tim Taviano
"""
import math as m
import random as r
import copy as c
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as pp
r.seed(1)

#class for blocks within sudoku puzzle
class Block:
    def __init__(self,width):
        self.width = width
        self.total = pow(width,2)
        self.block = [x for x in range(1,self.total +1)]
        r.shuffle(self.block)
    def shuffle(self):
        r.shuffle(self.block)
    def __str__(self):
        return str(self.block)
    def __repr__(self):
        return str(self)
    def getCol(self,col):
        temp_list = list()
        for x in range(self.width):
            temp_list.append(self.block[x*self.width +col])
        return temp_list.copy()
    def getRow(self,row):
        temp_list = list()
        for x in range(self.width):
            temp_list.append(self.block[self.width*row+x])
        return temp_list.copy()
    def print(self):
        counter = 0
        for x in range(self.width):
            for y in range(self.width):
                print(self.block[counter], end= " ")
                counter +=1
            print()
    def swap(self, x,y):
        temp = c.deepcopy(self.block[x])
        self.block[x] =c.deepcopy(self.block[y])
        self.block[y] = temp

#class for nxn sudoku puzzle
class Puzzle:

    def __init__(self,n):
        self.n = n
        self.blockwidth = int(m.sqrt(n))
        self.blocks = list()
        self.fit =None
        for x in range(n):
            self.blocks.append(Block(int(m.sqrt(n))))

    def print(self):
        for each in range(self.n):
            print(self.getRow(each))

    def getCol(self,col):
        b_start = col//3
        b_col = col %3
        temp_col =list()
        for x in range(self.blockwidth):
            temp_col += self.blocks[(x*self.blockwidth)+b_start].getCol(b_col)
        return temp_col.copy()

    def getRow(self,row):
        b_start = (row// self.blockwidth) *self.blockwidth
        b_row = (row% self.blockwidth)
        temp_row = list()
        for x in range(self.blockwidth):
            temp_row += self.blocks[b_start+x].getRow(b_row)
        return temp_row.copy()
    def ChangeBlock(self,new_block,index):
        self.blocks[index] = c.deepcopy(new_block)

    def fitness(self):
        self.fit =0
        #calculate how many are wrong in each row and column
        for row in range(self.n):
            currentrow = self.getRow(row)
            for num in range(1,self.n+1):
                self.fit += abs(currentrow.count(num)-1)
        for col in range(self.n):
            currentcol = self.getCol(col)
            for num in range(1,self.n+1):
                self.fit += abs(currentcol.count(num)-1)
        #divide by 2 to cut cut away double counting errors.
        self.fit = (float(1) /(float(self.fit/2)+1.0))**2
        return self.fit
    def __lt__(self,other):
        if(self.fit != None and other.fit != None):
            return self.fit < other.fit
        else:
            return self.fitness() < other.fitness()

def GeneratePop(pop_size,n):
    population_list = list()
    for each in range(pop_size):
        population_list.append(Puzzle(n))
    return c.deepcopy(population_list)

def SortPop(pop_list):
    pop_list.sort()
def TotalFitness(pop_list):
    total =0
    for each in pop_list:
        total += each.fit
    return total
def SelectParents(pop_list):
    total = TotalFitness(pop_list)
    select_list = list()
    for each in pop_list:
        num = round(each.fit/total*100)
        for x in range(num):
            select_list.append(c.deepcopy(each))
    r.shuffle(select_list)
    return  c.deepcopy(select_list)

def MakeChildren(n,p,parents,crossover,mutation):
        children = list()
        for each in range(p):
                p1 = c.deepcopy(r.choice(parents))
                p2 = c.deepcopy(r.choice(parents))

                child1 = c.deepcopy(p1)
                child2 = c.deepcopy(p2)
                random1 = r.random()
                random2 = r.random()
                if(random1 <=crossover):
                        #do crossover
                        index1 = r.randint(0,n-1)
                        index2 = r.randint(0,n-1)
                        child1.ChangeBlock(c.deepcopy(p2.blocks[index2]),index1)
                elif (random1 <= crossover + mutation):
                        #do mutation
                        index = r.randint(0,n-1)
                        child1.blocks[index].shuffle()
                else:
                        pass
                        #child one is copy of parent1

                if(random2 <=crossover):
                        #do crossover
                        index1 = r.randint(0,n-1)
                        index2 = r.randint(0,n-1)
                        child2.ChangeBlock(c.deepcopy(p1.blocks[index1]),index2)

                elif (random2 <=crossover + mutation):
                        #do mutation
                        index = r.randint(0,n-1)
                        child2.blocks[index].shuffle()
                else:
                    pass
                children.append(c.deepcopy(child1))
                children.append(c.deepcopy(child2))
        return children
def test():
    l= GeneratePop(100,9)
    SortPop(l)
    print(l[0].fit)
    print(l[99].fit)
    p = SelectParents(l)
    print(len(p))
    p[0].print()
    c = MakeChildren(9,100,p,.4,.3)
    print(c)
    c[0].print()
    SortPop(c)
    print()
    c[0].print()
    print(c[199].fit)
    
def main():
    pop_size= 1000
    puz_width = 9
    num_generation =10000
    population = GeneratePop(num_generation,puz_width)
    SortPop(population)
    average_fitness = list()
    max_fitness = list()
    index_list()
    for gen in range(num_generation):
        SortPop(population)
        average_fitness.append(TotalFitness/pop_size)
        max_fitness.append(population[pop_size-1].fit)
        index_list.append(gen)



