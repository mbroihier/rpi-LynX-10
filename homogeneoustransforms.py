import numpy as np

class transforms:
    def __init__ (self, matrix):
        self.transformationMatrix = matrix
        self.inverseTransformationMatrix = matrix.I
    def __str__ (self):
        print self.transformationMatrix
        return ('')
    def __mul__(self,other):
        if other.__class__.__name__ == 'vector':
            otherVector = np.matrix(([other.x],[other.y],[other.z],[other.t]))
            newVector = self.transformationMatrix * otherVector
            return(vector(newVector[0,0],newVector[1,0],newVector[2,0]))
        if self.__class__.__name__ == 'vector':
            otherVector = np.matrix((self.x,self.y,self.z,1))
            newVector = otherVector * other.transformationMatrix
            return(vector(newVector[0,0],newVector[0,1],newVector[0,2]))
        if ('rotate' in other.__class__.__name__) or ('translate' in other.__class__.__name__) or ('transforms' in other.__class__.__name__) :
            newMatrix = self.transformationMatrix * other.transformationMatrix
            return (transforms(newMatrix))
        print 'Error in type passed to matrix multiply'
        
class vector(transforms):
    def __init__ (self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.t = 1.0

    def __str__(self):
        return ('x= %s, y=%s, z=%s' % (self.x, self.y,self.z))

    def __add__ (self,other):
        return vector(self.x+other.x,self.y+other.y,self.z+other.z)

    def __sub__ (self,other):
        return vector(self.x-other.x,self.y-other.y,self.z-other.z)

    def dot (self,second):
        return self.x * second.x + self.y * second.y + self.z * second.z + self.t * second.t
    
class rotateX(transforms):
    def __init__ (self, theta):
        transforms.__init__ (self,np.matrix ( ((1, 0, 0, 0),
                                 (0,np.cos(theta), -np.sin(theta), 0),
                                 (0,np.sin(theta), np.cos(theta), 0),
                                            (0,0,0,1))))

class rotateY(transforms):
    def __init__ (self, theta):
        transforms.__init__ (self,np.matrix (
            ((np.cos(theta), 0, np.sin(theta), 0),
             (0,1, 0, 0),
             (-np.sin(theta), 0, np.cos(theta), 0),
             (0,0,0,1))))
    

class rotateZ(transforms):
    def __init__ (self, theta):
        transforms.__init__ (self,np.matrix (
            ((np.cos(theta), -np.sin(theta), 0, 0),
             (np.sin(theta), np.cos(theta), 0, 0),
             (0,0,1,0),
             (0,0,0,1))))

class translateX(transforms):
    def __init__ (self, distance):
        transforms.__init__ (self,np.matrix ( ((1,0,0,distance),
                                 (0,1,0, 0),
                                 (0,0,1, 0),
                                 (0,0,0,1))))

class translateY(transforms):
    def __init__ (self, distance):
        transforms.__init__ (self,np.matrix ( ((1,0,0,0),
                                 (0,1,0, distance),
                                 (0,0,1, 0),
                                 (0,0,0,1))))
    

class translateZ(transforms):
    def __init__ (self, distance):
        transforms.__init__ (self,np.matrix ( ((1,0,0,0),
                                 (0,1,0, 0),
                                 (0,0,1, distance),
                                 (0,0,0,1))))
