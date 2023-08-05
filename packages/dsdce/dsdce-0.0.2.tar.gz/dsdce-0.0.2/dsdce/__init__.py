def ex1a():
    print('''
    ### Read n number of values in an array and display it in reverse order ###

    from numpy import *
    n=int(input("Size of array:"))
    li=[]
    for i in range(0,n):
        val=int(input("Enter the "+str(i+1)+" value: "))
        li.append(val)
    a=array(li)
    print("Array Values\\n",a)
    print("Reversed order")
    for i in range(len(a)-1,-1,-1):
        print(a[i],end=" ")''')

def ex1b():
    print('''
    ### Program to merge two arrays of same size ###

    from numpy import *
    a=array([3,4,5])
    b=array([6,7,8])
    if(len(a)==len(b)):
        c=concatenate((a,b))
        print("Merge of two arrays:")
        print(c)
    else:
        print("Arrays are not in same size")
    ''')


def ex2():
    print('''
    ### Linked List ###

    linked_list=[]

    ###Add at End Function###
    def add(node_val):
        linked_list.append([node_val,len(linked_list)+1])

    add(5)
    add(7)
    add(9)

    ###Traverse Function###
    def traverse():
        for i in linked_list:
            if(len(linked_list)>i[1]):
                print("Value:"+str(i[0])+", Next:"+str(i[1]))
            else:
                print("Value:"+str(i[0])+", Next:none")
                
    print("Linked List")
    traverse()

    ###Insert Function###
    def append(pos,val):
        if(pos<=len(linked_list)):
            address=pos+1
            val=[val,address]
            linked_list.insert(pos,val)
            for i in range(address,len(linked_list)):
                linked_list[i][1]+=1
        else:
            print("\\n\\nPlease enter the value below "+str(len(linked_list)+1))

    append(2,55)
    print("\\nLinked List")
    traverse()

    ###Delete Function###
    def delete(pos):
        if(pos<len(linked_list)):
            del linked_list[pos]
            if(len(linked_list)>=pos):
                for i in range(pos,len(linked_list)):
                    linked_list[i][1]-=1
        else:
            print("\\n\\nPlease enter the value below "+str(len(linked_list)))
    delete(2)
    print("\\nLinked List")
    traverse()   
    ''')

def ex3():
    print('''
    ### Stack implementation using Linked list ###

    stack=[]
    stack_storage=10
    def push(value):
        if(len(stack)>=stack_storage):
            print("Stack Overflow")
        else:
            stack.append(value)
    def pop():
        if(len(stack)>0):
            stack.pop()
        else:
            print("Stack Underflow:")
    def display():
        print("Elements in Stack:")
        for i in stack:
            print(i)
    push(5)
    push(6)
    display()
    push(7)
    display()
    pop()
    display()

    ''')

def ex4a():
    print('''
    ### Program to reverse a string ###

    stack=[]
    def reverse(string):
        print("Reversed String: ")
        for i in range(len(string)-1,-1,-1):
            print(string[i],end='')
    def display(string):
        print("Elements in Stack: ")
        for i in string:
            print(i)

    string=list(input("Enter a string:"))
    display(string)
    reverse(string)
    ''')

def ex4b():
    print('''
    ### Evaluate the Postfix Expression: ###

    s='456*+'
    #s=input("Enter the Potfix Expression:")
    s=list(s)
    o=[]
    n=''
    operators=['+','-','*','/']
    for i in s:
        if i in operators:
            if len(o)>1:
                first=o.pop()
                second=o.pop()
                n+=first+i+second
            else:
                first=o.pop()
                n+=i+first
        else:
            o.append(i)
    print(eval(n))
    ''')

def ex5():
    print('''
    ### Queue implementation using Linked List ###

    queue=[]
    queue_storage=10
    def push(value):
        if(len(queue)>=queue_storage):
            print("Queue is Full")
        else:
            queue.append(value)
    def pop():
        if(len(queue)>0):
            queue.pop(0)
        else:
            print("No elements in Queue")
    def display():
        print("Elements in queue:")
        for i in queue:
            print(i)
    push(5)
    push(6)
    display()
    push(7)
    display()
    pop()
    display()
    ''')

def ex6():
    print('''
    ### Round Robin Algorithm ###

    name=['first','second','third']
    time=[10,5,8]
    wait=[0,0,0]
    copied_time=time.copy()
    val=name[0]
    q=2
    m=list(range(len(name)))
    while(any(time)):
        deduct=q
        for i in m:
            if(name[i]==val):
                if(time[i]>q):
                time[i]=time[i]-q
                deduct=q
                else:
                deduct=time[i]
                time[i]=0
            else:
                if(time[i]!=0):
                wait[i]=wait[i]+deduct
        if(val==name[len(name)-1]):
            val=name[0]
        else:
            val=name[name.index(val)+1]     
        n=m.pop(0)
        m.append(n)
    print("Process - Burst Time - Waiting Time - Turn Around Time")
    for i in range(len(name)):
        print(str(name[i])+" - "+str(copied_time[i])+" - "+str(wait[i])+" - "+str(copied_time[i]+wait[i]))
    print("Average Waiting Time:"+str(sum(wait)/len(wait)))
    sum_value=sum(copied_time)+sum(wait)
    divide=len(wait)
    print("Average Turn Around Time:"+str(sum_value/divide))
    ''')

def ex7():
    print('''
    # Python program to demonstrate insert operation in binary search tree  
    
    # A utility class that represents an individual node in a BST  
    class Node:  
        def __init__(self,key):  
            self.left = None
            self.right = None
            self.val = key  
    
    # A utility function to insert a new node with the given key  
    def insert(root,key):  
        if root is None:  
            return Node(key)  
        else: 
            if root.val == key: 
                return root 
            elif root.val < key:  
                root.right = insert(root.right, key)  
            else: 
                root.left = insert(root.left, key) 
        return root 
    
    # A utility function to do inorder tree traversal  
    def inorder(root):  
        if root:  
            inorder(root.left)  
            print(root.val)  
            inorder(root.right)  
    
    
    # Driver program to test the above functions  
    # Let us create the following BST  
    #    50  
    #  /     \  
    # 30     70  
    #  / \ / \  
    # 20 40 60 80  
    
    r = Node(50)  
    r = insert(r, 30)  
    r = insert(r, 20)  
    r = insert(r, 40)  
    r = insert(r, 70)  
    r = insert(r, 60)  
    r = insert(r, 80)  
    
    # Print inoder traversal of the BST  
    inorder(r) 
    ''')

def ex8a():
    print('''
    # Python program for implementation of Insertion Sort 
  
    # Function to do insertion sort 
    def insertionSort(arr): 
    
        # Traverse through 1 to len(arr) 
        for i in range(1, len(arr)): 
    
            key = arr[i] 
    
            # Move elements of arr[0..i-1], that are 
            # greater than key, to one position ahead 
            # of their current position 
            j = i-1
            while j >=0 and key < arr[j] : 
                    arr[j+1] = arr[j] 
                    j -= 1
            arr[j+1] = key 
    
    
    # Driver code to test above 
    arr = [12, 11, 13, 5, 6] 
    insertionSort(arr) 
    print ("Sorted array is:") 
    for i in range(len(arr)): 
        print (arr[i]) 
    ''')

def ex8b():
    print('''
    ### Selection Sort ###

    A = [64, 25, 12, 22, 11] 
  
    # Traverse through all array elements 
    for i in range(len(A)): 
        
        # Find the minimum element in remaining  
        # unsorted array 
        min_idx = i 
        for j in range(i+1, len(A)): 
            if A[min_idx] > A[j]: 
                min_idx = j 
                
        # Swap the found minimum element with  
        # the first element         
        A[i], A[min_idx] = A[min_idx], A[i] 
    
    # Driver code to test above 
    print ("Sorted array") 
    for i in range(len(A)): 
        print(A[i]),  
    ''')

def ex9a():
    print('''
    ### Linear Search ###

    li=[3,6,2,8,4]
    search=int(input("Search:"))
    for i in range(0,len(li)):
        if(search==li[i]):
            print("Found at "+str(i+1)+" position")
    ''')

def ex9b():
    print('''
    # Python3 Program for recursive binary search. 
  
    # Returns index of x in arr if present, else -1 
    def binarySearch (arr, l, r, x): 
    
        # Check base case 
        if r >= l: 
    
            mid = l + (r - l) // 2
    
            # If element is present at the middle itself 
            if arr[mid] == x: 
                return mid 
            
            # If element is smaller than mid, then it  
            # can only be present in left subarray 
            elif arr[mid] > x: 
                return binarySearch(arr, l, mid-1, x) 
    
            # Else the element can only be present  
            # in right subarray 
            else: 
                return binarySearch(arr, mid + 1, r, x) 
    
        else: 
            # Element is not present in the array 
            return -1
    
    # Driver Code 
    arr = [ 2, 3, 4, 10, 40 ] 
    x = 10
    
    # Function call 
    result = binarySearch(arr, 0, len(arr)-1, x) 
    
    if result != -1: 
        print ("Element is present at index ", result) 
    else: 
        print ("Element is not present in array")
    ''')

def ex10():
    print('''
    ### Implementation of hashing function: ###

    hash_table=dict()
    values=[5,10,15,17,6,8,3,16,27,45]
    for i in values:
        k=int(i%10)
        if k in hash_table.keys():
            li=hash_table[k]
            li.append(i)
            hash_table[k]=li
        else:
            li=[]
            li.append(i)
            hash_table[k]=li
    for i,j in hash_table.items():
        print(i," -> ",j)
    ''')
