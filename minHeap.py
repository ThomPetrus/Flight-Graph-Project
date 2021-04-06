# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 16:59:38 2021

A minheap to be used in our dijkstra based algorithm.
This is adapted from the MinHeap implementation found on:
https://www.geeksforgeeks.org/min-heap-in-python/

@author: tpvan
"""

import sys

class MinHeap:
    """
    A min heap implementation adapted to be used with algorithmOne or algorithmTwo.
    
    Attributes:
    --------------------------------------------------------------------------------
        max_size : int 
                The heap is initialized with a large enough list to hold all nodes.
        size : int
                The amount of elements currently in the min heap    
        heap : list
                The list used to implement the binary tree min heap.
        FRONT : int
                A pointer to the minimum element
    ---------------------------------------------------------------------------------
    """
    
    def __init__(self, max_size):
        """
        Constructs the necessary attributes for the min heap to run
        
        Parameters:
        ---------------------------------------------------------------------------------
            max_size : int
                Used to initialize the list to a sufficiently large size.
        ---------------------------------------------------------------------------------
        """
        self.max_size = max_size
        self.size = 0
        self.heap = [{'name':'', 'cost':sys.maxsize}] * (self.max_size * 5)
        self.heap[0] = {'name':'ROOT', 'cost': (-1 * sys.maxsize)}
        self.FRONT = 1
        
    def parent(self, pos):   
        """
        Get parent position for current node
        
        Parameters:
        ---------------------------------------------------------------------------------
            pos : int 
                position of current node
        ---------------------------------------------------------------------------------
        """
        return pos//2
    
    def left_child(self, pos):
        """
        Get left child position for current node
        
        Parameters:
        ---------------------------------------------------------------------------------
            pos : int 
                position of current node
        ---------------------------------------------------------------------------------
        """
        return 2 * pos
    
    def right_child(self, pos):
        """
        Get right child position for current node
        
        Parameters:
        ---------------------------------------------------------------------------------
            pos : int 
                position of current node
        ---------------------------------------------------------------------------------
        """
        return (2 * pos) + 1
    
    def is_leaf(self, pos):
        """
        Check whether a node is a leaf node
        
        Parameters:
        ---------------------------------------------------------------------------------
            pos : int 
                position of current node
        ---------------------------------------------------------------------------------
        """
        if (pos >= (self.size//2) and pos <= self.size): 
            return True
        return False
    
    def swap(self, fpos, spos):
        """
        Swap two nodes in the list
        
        Parameters:
        ---------------------------------------------------------------------------------
            fpos : int 
                position of first node
            spos : int 
                position of second node
        ---------------------------------------------------------------------------------
        """
        self.heap[fpos], self.heap[spos] = self.heap[spos], self.heap[fpos]
    
    def min_heapify(self, pos):
        """
        Check if a given node has to be moved elsewhere in the min heap based on its value
        and move it to maintain the min heap property.
        
        Parameters:
        ---------------------------------------------------------------------------------
            pos : int 
                position of current node
        ---------------------------------------------------------------------------------
        """
        try:
        
            # If the node is a non-leaf node and greater
            # than any of its child
            if not self.is_leaf(pos):
                if (self.heap[pos]['cost'] > self.heap[self.left_child(pos)]['cost'] or self.heap[pos]['cost'] > self.heap[self.right_child(pos)]['cost']):    
                    
                    # swap if greater than either child, then heapify child
                    if self.heap[self.left_child(pos)]['cost'] < self.heap[self.right_child(pos)]['cost']:
                        self.swap(pos, self.left_child(pos))
                        self.min_heapify(self.left_child(pos))
                    else:
                        self.swap(pos, self.right_child(pos))
                        self.min_heapify(self.right_child(pos))
        except IndexError:
            # may occur if heap is not large enough.
            print("Min Heap Index Error : pos => " + str(pos))
            
    def insert(self, node):
        """
        Insert into the heap
        
        Parameters:
        ---------------------------------------------------------------------------------
            node : dict
                A node containing the airport name and the cost associated with it.
        ---------------------------------------------------------------------------------
        """
        
        # return if full
        if self.size >= self.max_size:
            return
        
        self.size+=1
        self.heap[self.size] = node
    
        current = self.size
        
        # find appropriate spot in heap
        while self.heap[current]['cost'] < self.heap[self.parent(current)]['cost']:
            self.swap(current, self.parent(current))
            current = self.parent(current)
            
    def print(self):
        """
        Print out the heap
        """
        for i in range(1, (self.size//2)+1):
            print(" PARENT : "+ str(self.heap[i])+" LEFT CHILD : "+
                                str(self.heap[2 * i])+" RIGHT CHILD : "+
                                str(self.heap[2 * i + 1]))
 
    def min_heap(self):
        """
        Check all nodes and maintain min heap property.
        """
        for pos in range(self.size//2, 0, -1):
            self.min_heapify(pos)
            
    def remove(self):
        """
        Remove and return the minimum node in the heap and ensure min heap property is maintained afterwards
        """
        popped = self.heap[self.FRONT]
        self.heap[self.FRONT] = self.heap[self.size]
        self.size -= 1
        self.min_heapify(self.FRONT)
        return popped
            
def test():
    """
    Test Min Heap
    """
    heap = MinHeap(50);    
    heap.insert({"name":"LAX7", 'cost':7})
    heap.insert({"name":"LAX14", 'cost':14})
    heap.insert({"name":"LAX", 'cost':0})
    heap.insert({"name":"LAX5", 'cost':5})
    heap.insert({"name":"LAX12", 'cost':12})
    heap.insert({"name":"LAX1", 'cost':1})
    heap.insert({"name":"LAX3", 'cost':3})
    heap.insert({"name":"LAX9", 'cost':9})
    heap.insert({"name":"LAX2", 'cost':2})
    heap.insert({"name":"LAX4", 'cost':4})
    heap.insert({"name":"LAX8", 'cost':8})
    heap.insert({"name":"LAX11", 'cost':11})
    heap.insert({"name":"LAX10", 'cost':10})
    heap.insert({"name":"LAX13", 'cost':13})
    heap.insert({"name":"LAX6", 'cost':6})
    heap.print()
    
if __name__ == "__main__":
    test();

    
            
            
            
            
            
            
            
            