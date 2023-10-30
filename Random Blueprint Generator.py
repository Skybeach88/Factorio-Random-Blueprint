import random, copy

#------------------------------------------------------------------------------------------------------------------------------------------------
#{"blueprint":{"icons":[{"signal":{"type":"item","name":"fast-transport-belt"},"index":1}],"entities":[{"entity_number":1,"name":"fast-transport-belt","position":{"x":116.5,"y":-79.5},"direction":2},{"entity_number":2,"name":"fast-transport-belt","position":{"x":119.5,"y":-79.5},"direction":4}],"item":"blueprint","version":281479277641728}}
#{"blueprint":{"icons":[{"signal":{"type":"item","name":"steel-chest"},"index":1}],"entities":[{"entity_number":1,"name":"fast-splitter","position":{"x":-3,"y":-4},"direction":8},{"entity_number":2,"name":"express-splitter","position":{"x":5,"y":5},"direction":4}],"item":"blueprint","label":"Random Blueprint Gen 1","version":281479277641728}}

#Variable declarations
blueprintHeader = '{"blueprint":{"icons":[{"signal":{"type":"virtual","name":"signal-dot"},"index":1}],"entities":['
blueprintFooter = '],"item":"blueprint","label":"Random Blueprint Gen 1","version":281479277641728}}' #see if i can get the version number to auto generate with lua once i implement this as a mod


sizeOfArray = 11 # this is the height and width of the blueprint to create
entityNum = 1 # this initializes the program to have the first item added be item number 1

newString = blueprintHeader

#------------------------------------------------------------------------------------------------------------------------------------------------
# Data for building
#This is the inital data strutcure holding the needed information about each item that cn be chosen, eventually I want this to pull automatically from data.raw

items = [{'item':'Transport Belt', 'item-name' : 'transport-belt','height':1,'width':1,'rotate':True},
    {'item':'Fast Transport Belt', 'item-name' : 'fast-transport-belt','height':1,'width':1,'rotate':True},
    {'item':'Express Transport Belt', 'item-name' : 'express-transport-belt','height':1,'width':1,'rotate':True},
    {'item':'Underground Belt', 'item-name' : 'underground-belt','height':1,'width':1,'rotate':True},
    {'item':'Fast Underground Belt', 'item-name' : 'fast-underground-belt','height':1,'width':1,'rotate':True},
    {'item':'Express Underground Belt', 'item-name' : 'express-underground-belt','height':1,'width':1,'rotate':True},
    {'item':'Splitter', 'item-name' : 'splitter','height':1,'width':2,'rotate':True},
    {'item':'Fast Splitter', 'item-name' : 'fast-splitter','height':1,'width':2,'rotate':True},
    {'item':'Express Splitter', 'item-name' : 'express-splitter','height':1,'width':2,'rotate':True},
    {'item':'Assembling Machines', 'item-name' : 'assembling-machine-1','height':3,'width':3,'rotate':True} ]

#------------------------------------------------------------------------------------------------------------------------------------------------
#Needed functions

#This creates the array and fills it with the coordinates of each tile with respect to the center of the blueprint
def create_matrix(matrixSize):
    if matrixSize % 2 == 0:
        matrixSize = matrixSize - 1
    i = int((-1)*(matrixSize-1)/2)
    x=i
    y=i
    matrix=[]
    row=[]
    location=[0,0,0]

        #Create a blank matrix of the size given
    for n in range(matrixSize):
        row.append(location.copy())
    for m in range(matrixSize):
        tempRow = copy.deepcopy(row)
        matrix.append(tempRow)

        #populates the array with x,y coordinates and a value for if the location is occupied, the format for each entity is [ x-coord , y-coord , Occupied where 1 is true ]
    for n in range(len(matrix)):
            while x<=-i:
                for m in range(len(row)):
                    matrix[n][m][0] = x
                    matrix[n][m][1] = y
                    x+=1
                y+=1
            x=i

    return(matrix)
#End of the create_matrix function


#This code selects a random item from the items array and populates a string with the correct values for the item-name, (x,y) position, and rotation direction
def item_String(Num,n,m,randItem,direction):
    addItemString = '{"entity_number":'+ str(Num) +',"name":"' + randItem['item-name'] + '","position":{"x":' + str(bpArray[n][m][0]) + ',"y":' + str(bpArray[n][m][1]) + '},'
    if randItem['rotate'] == True:
        addItemString += '"direction":' + str(direction) + '},'
    return(addItemString)
#End of the item_select function

#------------------------------------------------------------------------------------------------------------------------------------------------

bpArray = create_matrix(sizeOfArray+4) #This is the array representing the tiles for the blueprint

#------------------------------------------------------------------------------------------------------------------------------------------------
#Scans the surrounding tile to determine if there is space for the entity
def tileScan(n,m,direction,itemChoice):
    #-----Rotation options
    horizontalRotation = (1,4,5,8)
    verticalRotation = (2,3,6,7)
    #------Dimensions of chosen entity
    height = itemChoice['height']
    width = itemChoice['width']

    #------ This is for an nxn object
    if height == width:
        if height % 2 != 0:
            heightScan = height // 2
            widthScan = width // 2

            for scanY in range(height):  #Scans along the x axis for
                for scanX in range(width):
                    if bpArray[n-heightScan+scanY][m-widthScan+scanX][2] == 1:
                        return True # returns True the moment it finds a tile that IS occupied
        else:
            heightScan = height - 1
            widthScan = width - 1

            for scanY in range(height):  #Scans along the x axis for
                for scanX in range(width):
                    if bpArray[n-heightScan+scanY][m-widthScan+scanX][2] == 1:
                        return True # returns True the moment it finds a tile that IS occupied

   #------- this if for a nxm object
    if height != width:
        #----- for a horizontally rotated object
        if direction in horizontalRotation:
            if (height % 2 != 0) and (width %2 !=0):
                heightScan = height // 2
                widthScan = width // 2
            elif (height % 2 == 0) and (width %2 !=0):
                heightScan = height - 1
                widthScan = width // 2
            elif (height % 2 != 0) and (width %2 ==0):
                heightScan = height // 2
                widthScan = width - 1
            for scanY in range(height):
                for scanX in range(width):
                    if bpArray[n-heightScan+scanY][m-widthScan+scanX][2] == 1:
                        return True # returns True the moment it finds a tile that IS occupied
        #----- For a veritcally rotated object
        if direction in verticalRotation:
            if (height % 2 != 0) and (width %2 !=0):
                heightScan = width // 2
                widthScan = height // 2
            elif (height % 2 == 0) and (width %2 !=0):
                heightScan = width // 2
                widthScan = height - 1
            elif (height % 2 != 0) and (width %2 ==0):
                heightScan = width - 1
                widthScan = height // 2
            for scanY in range(height):
                for scanX in range(width):
                    if bpArray[n-heightScan+scanY][m-widthScan+scanX][2] == 1:
                        return True # returns True the moment it finds a tile that IS occupied

#------------------------------------------------------------------------------------------------------------------------------------------------
#Here I need to define a function that will change change the occupied variable in the array to account for an item being placed
#It will use the same format as the scan function only instead of reading the value in the array variable, it will write it to a 1 to assign that tile.

def assignTile(n,m,direction,itemChoice):
    #-----Rotation options
    horizontalRotation = (1,4,5,8)
    verticalRotation = (2,3,6,7)
    #------Dimensions of chosen entity
    height = itemChoice['height']
    width = itemChoice['width']

    #------ This is for an nxn object
    if height == width:
        if height % 2 != 0:
            heightScan = height // 2
            widthScan = width // 2

            for scanY in range(height):  #Scans along the x axis for
                for scanX in range(width):
                    bpArray[n-heightScan+scanY][m-widthScan+scanX][2] = 1

        else:
            heightScan = height - 1
            widthScan = width - 1

            for scanY in range(height):  #Scans along the x axis for
                for scanX in range(width):
                    bpArray[n-heightScan+scanY][m-widthScan+scanX][2] = 1

   #------- this if for a nxm object
    if height != width:
        #----- for a horizontally rotated object
        if direction in horizontalRotation:
            if (height % 2 != 0) and (width %2 !=0):
                heightScan = height // 2
                widthScan = width // 2
            elif (height % 2 == 0) and (width %2 !=0):
                heightScan = height - 1
                widthScan = width // 2
            elif (height % 2 != 0) and (width %2 ==0):
                heightScan = height // 2
                widthScan = width - 1
            for scanY in range(height):
                for scanX in range(width):
                    bpArray[n-heightScan+scanY][m-widthScan+scanX][2] = 1
        #----- For a veritcally rotated object
        if direction in verticalRotation:
            if (height % 2 != 0) and (width %2 !=0):
                heightScan = width // 2
                widthScan = height // 2
            elif (height % 2 == 0) and (width %2 !=0):
                heightScan = width // 2
                widthScan = height - 1
            elif (height % 2 != 0) and (width %2 ==0):
                heightScan = width - 1
                widthScan = height // 2
            for scanY in range(height):
                for scanX in range(width):
                    bpArray[n-heightScan+scanY][m-widthScan+scanX][2] = 1

#------------------------------------------------------------------------------------------------------------------------------------------------
#add items to the item string
def add_Item(n,m,entityNum):
    tempItem = random.choice(items) #selects a random item and stores it for the funtion to reference
    direction = random.randint(1,8) #Chooses the direction of the item
    if tileScan(n,m,direction,tempItem) != True: #determine if the array has space for the item or not
       itemString = item_String(entityNum,n,m,tempItem,direction)
       assignTile(n,m,direction,tempItem)
    else:
        itemString=('')
    return(itemString)




#------------------------------------------------------------------------------------------------------------------------------------------------

# cyce through the array and decide if the tile gets an item or not, I figure a 25% likelyhood of getting some object should be good for now
#I think I will neeed to change the way that this is adding information to the string

for n in range(len(bpArray)):
    for m in range(len(bpArray[0])):
        if (n > 1) and (n < len(bpArray)-2) and (m>1) and (m < len(bpArray)-2):
            if random.randint(1,4) == 1:  #This determines if a particular tile will get an entity or not. currently 25% chance I wonder if there is an easeier way of doing this
                    #Call function to add Items to the string
                newString += add_Item(n,m,entityNum)
                # newString += item_string(entityNum,bpArray[n][m][0],bpArray[n][m][1])
                entityNum += 1

newString = newString[:len(newString)-1] + blueprintFooter

#------------------------------------------------------------------------------------------------------------------------------------------------


print(newString)
