# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 13:43:30 2017

@author: Tim
"""
import math as m
import random as r
import copy as c

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
        temp = self.block[x]
        self.block[x] =self.block[y]
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
    def fitness(self):
        self.fit =0
        for row in range(self.n):
            currentrow = self.getRow(row)
            for num in range(1,self.n+1):
                self.fit += abs(currentrow.count(num)-1)
        for col in range(self.n):
            currentcol = self.getCol(col)
            for num in range(1,self.n+1):
                self.fit += abs(currentcol.count(num)-1)
        return self.fit
        
    