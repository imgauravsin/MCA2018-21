import pickle, os
import random



N = 1000
blocksize = 10

class Record :
    '''
    DESCRIPTON : To create an object of type 'Record'
    ATTRIBUTES : key, nonkey
    '''

    def __init__(self, key, nonkey):
        '''
        OBJECTIVE : To initialize an Record object
        INPUT PARAMETERS :
                self : (Implicit) Record object
                key : key value of the object Record
                nonkey : value corresponding to that key
        OUTPUT :
                None
        '''

        #Appoach: key = key  & nonkey = nonkey

        self.key = key 
        self.nonkey = nonkey

    def get_key(self):

        '''
        OBJECTIVE: To get key value of the Record object
        INPUT PARAMETERS:
                 self: (Implicit) Record Object
        OUTPUT :
                 None
        '''

        return self.key


    def __str__(self):
        '''
        OBJECTIVE: To return a string of the values of the object Record
        INPUT PARAMETERS :
                self : (Implicit) Record object
        OUTPUT : 
                a string representing the Record object
        '''

        return "Key: "+str(self.key) + "\nnonkey: " + str(self.nonkey)


def writeRecord():

    '''
    OBJECTIVE :  To write records in file1
    INPUT PARAMETERS :
            None
    OUTPUT :
            None
    '''

    #Approach: Dump Record object in file.txt 

    f = open("file1.txt", "wb")
    keyList = []
    i = 1
    
    while i <= N:
        key = random.randint(1000000, 2000000)
        if key not in keyList:
            keyList.append(key)
            val = str(key) * 100#random.randint(100,200)
            i = i+1
            ob = Record(key, val)
            pickle.dump(ob, f)

    f.close()
    

def display():

    '''
    OBJECTIVE :  To display records in file1
    INPUT PARAMETERS :
            None
    OUTPUT :
            None
    '''

    f = open("file1.txt", "rb")
    i = 1

    while i <= N:
        ob = pickle.load(f)
        print(str(i) + " file1")
        print(ob)
        i+=1
        
    f.close()

def sortMerge():

    '''
    OBJECTIVE :  To sort records of file1 and store them in f1.txt file
    INPUT PARAMETERS :
            None
    OUTPUT :
            None
    '''

    #APPROACH: sort and merge records of f1 & f2 in a group of blocksize and repeat until f2 is empty

    global blocksize

    f = open("file1.txt", "rb")
    f1 = open("f1.txt", "wb")
    f2 = open("f2.txt", "wb")

    keepLooping = True
    while keepLooping:
        f1s = []
        f2s = []
        for i in range (0, blocksize):
            try :
                ob = pickle.load(f)
                f1s.append(ob)
            except EOFError :
                keepLooping = False
            
        f1s.sort(key = lambda Record : Record.get_key())
        for el in f1s :
            pickle.dump(el, f1)

        for i in range (0, blocksize):
            try :
                ob = pickle.load(f)
                f2s.append(ob)
            except EOFError :
                keepLooping = False 
    
        f2s.sort(key = lambda Record : Record.get_key())
        for el in f2s :
            pickle.dump(el, f2)
                
    f.close()
    f1.close()
    f2.close()

    while True:
        
        merge()

        if os.path.getsize("f2.txt") == 0:  # check if f2.txt is empty
            break
        
        blocksize *= 2

              
def display2() :

    '''
    OBJECTIVE :  To display records of f1 and f2 files
    INPUT PARAMETERS :
            None
    OUTPUT :
            None
    '''

    f1 = open("f1.txt", "rb")
    f2 = open("f2.txt", "rb")

    i = 1
    while True:
        try:
            ob = pickle.load(f1)
            print(str(i) + " f1")
            print(ob)
            i+=1
        except EOFError:
            break
    i=1
    while True:
        try:
            ob = pickle.load(f2)
            print(str(i) + " f2")
            print(ob)
            i+=1
        except EOFError:
            break

    f1.close()
    f2.close()

    

def display_sortRe(lower,upper):

    '''
    OBJECTIVE :  To display records of sorted file "f1.txt" given lower and upper range
    INPUT PARAMETERS :
            lower: lower limit for the range to display records
            upper: upper limit for the range to display records
    OUTPUT :
            None
    '''

    f1 = open("f1.txt", "rb")

    ob = pickle.load(f1)

    size = f1.tell()

    i = lower

    f1.seek( size * (lower-1) )

    print("Sorted:")
    
    while i <= upper:
        ob = pickle.load(f1)
        print("\nRecord Number: " + str(i) + ":")
        print(ob)
        i += 1

    f1.close()
   
    

def merge():

    '''
    OBJECTIVE :  To sort and merge records of f1.txt and f2.txt
    INPUT PARAMETERS :
            None
    OUTPUT :
            None
    '''

    f1 = open("f1.txt", "rb")
    f2 = open("f2.txt", "rb")
    f3 = open("f3.txt", "wb")
    f4 = open("f4.txt", "wb")

    flag = True
    keepLooping = True
    
    while keepLooping:
        if flag == True:
            fil = f3
            flag = False
        else:
            fil = f4
            flag = True

        f1s = []
        f2s = []
        
        for i in range (0, blocksize):
            try :
                ob = pickle.load(f1)
                f1s.append(ob)
            except EOFError :
                keepLooping = False
                
        for i in range (0, blocksize):
            try :
                ob = pickle.load(f2)
                f2s.append(ob)
            except EOFError :
                keepLooping = False 

        i, j = 0, 0

        while i < len(f1s) and j < len(f2s):
            if f1s[i].get_key() <= f2s[j].get_key():
                el = f1s[i]
                i += 1
            else:
                el = f2s[j]
                j += 1
                
            pickle.dump(el, fil)

        while i < len(f1s):
            pickle.dump(f1s[i], fil)
            i += 1

        while j < len(f2s):
            pickle.dump(f2s[j], fil)
            j += 1

    try:
        f1.close()
        f2.close()
        f3.close()
        f4.close()
    except :
       print("Closing Error")

    try:
        os.remove("f1.txt")
        os.remove("f2.txt")
        os.rename("f3.txt", "f1.txt")
        os.rename("f4.txt", "f2.txt")
    except :
        print("Error")

def main() :

    writeRecord()
    sortMerge()

    l = input("Enter lower limit: ")
    u = input("Enter Upper limit: ")
    display_sortRe(int(l), int(u))


main()










