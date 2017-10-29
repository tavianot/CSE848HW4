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
import matplotlib.ticker as ticker
#r.seed(107)

#class for blocks within sudoku puzzle
class Block:
    def __init__(self,width):
        self.width = width
        self.total = pow(width,2)
        self.block = [x for x in range(1,self.total +1)]
        r.shuffle(self.block)
    def shuffle(self):
#        first = r.randint(0,self.width-1)
#        second = r.randint(0,self.width-1)
#        temp = c.deepcopy(self.block[first])
#        self.block[first]= c.deepcopy(self.block[second])
#        self.block[second]= temp
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
        b_start = col//self.blockwidth
        b_col = col %self.blockwidth
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
    def Shuffle(self):
        r.shuffle(self.blocks)

    def fitness(self):
        self.fit =0
        #calculate how many are wrong in each row and column
        for row in range(self.n):
            currentrow = self.getRow(row)
            if(len(set(currentrow))==len(currentrow)):
                self.fit -= 0
            else:
                self.fit += len(currentrow)-len(set(currentrow))
        for col in range(self.n):
            currentcol = self.getCol(col)

            if(len(set(currentcol))==len(currentcol)):
                self.fit -= 0
            else:
                self.fit += len(currentcol)-len(set(currentcol))
        
        return self.fit
    def __lt__(self,other):
        return self.fitness() > other.fitness()

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
def SelectParents(pop_list,pop_size):
    select_list = list()
    for each in range(pop_size):
        first =r.choice(pop_list)
        second = r.choice(pop_list)
        if(first.fitness()>= second.fitness()):
            select_list.append(c.deepcopy(first))
        else:
            select_list.append(c.deepcopy(second))
    return  select_list

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
    
def MutatePop(pop, mutation):
    for each in pop:
        if (r.random() <= mutation):
            each.Shuffle()
def test():
    pop_size= 600
    puz_width = 9
    crossov = .8
    mutat = .2
    num_generation =100
    population = GeneratePop(pop_size,puz_width)
    SortPop(population)
    par = SelectParents(population)
    print(par)

    
def main():
    pop_size= 50 
    puz_width = 9
    crossov = .2
    mutat = .8
    pop_mutat = .05
    num_generation =1000
    population = GeneratePop(pop_size,puz_width)
    SortPop(population)
    average_fitness = list()
    max_fitness = list()
    index_list = list()
    for gen in range(num_generation):

        SortPop(population)
        average_fitness.append(TotalFitness(population)/pop_size)
        max_fitness.append(population[pop_size-1].fit)  
        index_list.append(gen)
        if(population[pop_size-1].fit == 0):
            break

#        if(gen>=num_generation/10):
#             if(len(set(max_fitness[-1*num_generation//10:]))==1):
#                 population = GeneratePop(pop_size,puz_width)
#                 SortPop(population)

        par = SelectParents(population, pop_size)
        childs = MakeChildren(puz_width,pop_size,par,crossov,mutat)
        SortPop(childs)
        temp = c.deepcopy(population) +c.deepcopy(childs)
        SortPop(temp)
        MutatePop(temp,pop_mutat)
        population = c.deepcopy(temp)[-1*pop_size:]
    print(index_list)
    print(average_fitness)
    print(max_fitness)
    pp.plot(index_list,max_fitness, linewidth=2)
    pp.plot(index_list,average_fitness,linewidth =2)
    pp.legend(["best fitness","average fitness"], loc= 'lower left')
    pp.xlabel('Generation')
    pp.ylabel('Fitness')
    pp.title('GA runs with 9x9 puzzles')
    pp.xticks(index_list)
    axes = pp.gca()
    axes.yaxis.set_major_locator(ticker.MultipleLocator(5))
    #axes.xaxis.set_major_locator(ticker.MultipleLocator(num_generation/10))
    pp.grid(True)
    pp.xlim(0,index_list[-1])
    pp.ylim(0,max(max_fitness+average_fitness))
    pp.show()
    
    
    

    

#test()
main()
