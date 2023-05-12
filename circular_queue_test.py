#!/usr/bin/python3
from circular_queue import CircularQueue

if __name__ == "__main__":
    circle = CircularQueue(size=10)
    for i in circle:
        print(i)
    for i in range(25):
        circle.enqueue(i)
    
    print("Print Circle")
    for i in circle:
        print(i, end=" ")
    print()
    for i in range(25):
        circle.dequeue()
    print("Empty Queue")
    for i in circle:
        print(i, end=" ")
    print()
    for i in range(4):
        circle.enqueue(i)
    print("Queue 4")
    for i in circle:
        print(i, end=" ")
    print(circle)