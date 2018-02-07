class Vector2D:
    '''Creates a 2D point that can work with mathimatical operations.'''

    def __init__(self, x, y):
        '''Initialize the x and y coordinates.'''
        self.x = x
        self.y = y
    
    def __repr__(self):
        '''Create the output for it Vector2D is put into print().'''
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def __setattr__(self, name, value):
        '''Validate user input for x and y coordinates.'''
        try:
            if isinstance(value, int):
                if name == 'x' or name == 'y':
                    super(Vector2D, self).__setattr__(name, value)
            else:
                raise TypeError
        except TypeError:
            print('Coordinates must be in integer format.')

    def __getattr__(self, name):
        '''Validates the name of an attribute the user tries to access.'''
        attr = None
        try:
            if name == 'x':
                attr = self.x
            elif name == 'y':
                attr = self.y
            else:
                raise AttributeError
        except AttributeError:
            print('No attribute {}. Valid attributes are x and y.'.format(name))
        return attr

    def __eq__(self, other):
        '''Confirm that other is a point and then return if they are equal.'''
        equal = False
        try:
            if isinstance(other, Vector2D):
                if self.x == other.x and self.y == other.y:
                    equal = True
            else:
                raise TypeError
        except TypeError:
            print('Can not compare Vector2D and {} for equality.'.format(type(other)))
        
        
        return equal

    def __add__(self, other):
        '''Confirm that other is a point and then create their sums.'''
        try:
            if isinstance(other, Vector2D):
                x = self.x + other.x
                y = self.y + other.y
            else:
                raise TypeError
        except:
            print('Cannot add {} to Vector2D. Must be another Vector2D'.format(type(other)))
        return Vector2D(x, y)

    __radd__ = __add__

    def __sub__(self, other):
        '''Confirm that other is a point.
    
        Then subtract with other on the right side.
        '''
        try:
            if isinstance(other, Vector2D):
                x = self.x - other.x
                y = self.y - other.y
            else:
                raise TypeError
        except:
            print('Cannot add {} to Vector2D. Must be another Vector2D'.format(type(other)))
        return Vector2D(x, y)

    def __rsub__(self, other):
        '''Confirm that other is a point.
        
        Then subtract with other on the left side.
        '''
        try:
            if isinstance(other, Vector2D):
                x = other.x - self.x
                y = other.y - self.y
            else:
                raise TypeError
        except:
            print('Cannot add {} to Vector2D. Must be another Vector2D'.format(type(other)))
        return Vector2D(x, y)
    
    def __mul__(self, other):
        '''Confirm that other is an integer and perform scalar multiplication.'''
        try:
            if isinstance(other, int):
                x = other * self.x
                y = other * self.y
            else:
                raise TypeError
        except:
            print('Can not multiple by {}. Must be int.'.format(type(other)))
        return Vector2D(x, y)

    __rmul__ = __mul__