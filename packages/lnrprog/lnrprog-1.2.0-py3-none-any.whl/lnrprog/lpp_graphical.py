'''
created by: Ashish Kumar
created on: 26/08/2020


This package will help in solving Linear programming problem for n-number of constrains.
This package shows the graphical representation of the constrains and showing the optimal solution as requested by the 
user. By this we can optimize solution as maximization type and minimization type.

If you find any problem in this package feel free to add issue here:- https://github.com/Ashish2000L/linear_programing
'''

import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
style.use("ggplot")
colours=['r','g','c']

#only two type is there 'min' and 'max', default is max

class graphical_method:
    '''
    @:param
    number_of_constrains:int -> This is the number of constrains in the equation
    type:str -> This is type i.e max(Maximization) and min(Minimization)
    optimize_fn:list -> This is a list in which the coeff of optimize function is needed, since this is
                        a graphical method so coefficient of x,y is neede in the list only
    constrains:list -> This is a 2D list
                        i.e: If the constrains are 2x+3y<=5 and 3x+4y>=6
                            so the list should be [[2,3,'<=',5],[3,4,'>=',6]]
    '''
    def __init__(self,number_of_constrains:int,type:str,optimize_fn:list=['coeff-X','coeff-Y'],constrains:list=None):
        self.number_of_constrains=number_of_constrains
        self.equation=[]
        self.itr=0
        self.type=type
        self.max=0
        self.min=0
        self.opt_res=0
        self.optimize=optimize_fn
        self.at_x=0
        self.at_y=0
        self.constrains=constrains
        self.__equations()

    #this initiate the process and check if user input is as desired or not
    def __equations(self):
        if self.optimize[0]=='coeff-X' or self.optimize[1]=='coeff-Y':
            raise ValueError("null optimal function, provide appropriate optimal function ")
        if str(type(self.constrains))!="<class 'list'>" and str(type(self.constrains))!="<class 'NoneType'>":
            raise TypeError('Constrains must be list type only not {0} '.format(type(self.constrains)))
        if self.number_of_constrains>1:
            eq, rhs= self.__getcofficients(self.number_of_constrains)
            self.__setvalue(eq, rhs, self.number_of_constrains)
        else:
            raise ValueError("Number of constrains must be greater then 1 ")

    #this function plot the graph of the constrains and the feasible reagion respective to constrains
    def __represent(self,X, Y, max):
        coordinate=[]
        for i in range(self.number_of_constrains):
            coordinate.append([(X[i][j],Y[i][j]) for j in range(len(X[i]))])

        final=[]
        for i in range(self.number_of_constrains):
            for j in coordinate[i]:
                if j not in final:
                    final.append(j)

        for i in final:
            p='({0:.2f},{1:.2f})'.format(i[0],i[1])
            plt.annotate(p,(i[0],i[1]))


        d = np.linspace(self.min, self.max, 3000)
        x, y = np.meshgrid(d, d)
        eqs = []
        for eq in self.equation:
            if eq[2] == '<=':
                eqs.append(eq[0] * x + eq[1] * y <= eq[3])
            elif eq[2] == '>=':
                eqs.append(eq[0] * x + eq[1] * y >= eq[3])
            else:
               raise TypeError("only <= and >= are expected here ")

        if self.number_of_constrains == 2:
            plt.imshow((eqs[0] & eqs[1] & (x>=0) & (y>=0)).astype(int),
                       extent=(x.min(), x.max(), y.min(), y.max()), origin="higher", cmap="Blues", alpha=0.3)
        elif self.number_of_constrains == 3:
            plt.imshow((eqs[0] & eqs[1] & eqs[2] & (x>=0) & (y>=0)).astype(int),
                       extent=(x.min(), x.max(), y.min(), y.max()), origin="higher", cmap="Blues", alpha=0.3)
        elif self.number_of_constrains == 4:
            plt.imshow((eqs[0] & eqs[1] & eqs[2] & eqs[3] & (x>=0) & (y>=0)).astype(int),
                       extent=(x.min(), x.max(), y.min(), y.max()), origin="higher", cmap="Blues", alpha=0.3)
        elif self.number_of_constrains == 5:
            plt.imshow((eqs[0] & eqs[1] & eqs[2] & eqs[3] & eqs[4] & (x>=0) & (y>=0)).astype(int),
                       extent=(x.min(), x.max(), y.min(), y.max()), origin="higher", cmap="Blues", alpha=0.3)
        elif self.number_of_constrains == 6:
            plt.imshow((eqs[0] & eqs[1] & eqs[2] & eqs[3] & eqs[4] & eqs[5] & (x>=0) & (y>=0)).astype(int),
                       extent=(x.min(), x.max(), y.min(), y.max()), origin="higher", cmap="Blues", alpha=0.3)
        else:
            raise ValueError("Out of range number of constrains, max number of constrains should be upto 6 ")

        for i in range(max):
            plt.plot(X[i], Y[i], colours[i], label=f"equation {i + 1}", linewidth=2)

        plt.title('LPP Graphical Solution ')
        plt.xlabel('x-axis')
        plt.ylabel('y-axis')
        plt.legend()
        plt.grid(True, color='b')
        plt.show()

    #this function finds the axis intersection points
    def __setvalues(self,a, b, c):
        p = []
        q = []
        if a != 0:
            p.append(float(c) / float(a))
        else:
            p.append(0)
        q.append(0)

        if b != 0:
            q.append(float(c) / float(b))
        else:
            q.append(0)
        p.append(0)

        return p, q

    #this takes the constrains and process the constrains
    def __getcofficients(self,num_of_eq):
        equation_set = []
        rhs = []

        if self.constrains==None:
            print("Give proper spacing for the constrains i.e:\n\t 2x+3y<=5 should be writen as 2 3 <= 5\n")
            for i in range(num_of_eq):
                inpt=input("Enter Constrain {0}: ".format(i+1)).split(" ")

                a = int(inpt[0])
                b = int(inpt[1])
                d = inpt[2]
                c = int(inpt[3])
                equation_set.append([a, b])
                self.equation.append([a,b,d,c])
                rhs.append(c)
        elif len(self.constrains)>1:

            try:
                f=self.constrains[1][0]

                if f==None:
                    raise ValueError('Unexpected Null input found')
            except:
                raise ValueError('Minimum two constrains required for the optimal solution')

            if len(self.constrains) != self.number_of_constrains:
                raise ValueError('Number of constrains is not equal to the given constrains i.e:\n number of constrain({0}) != given constrain({1})'.format(
                    self.number_of_constrains, len(self.constrains)))

            for i in self.constrains:
                a=int(i[0])
                b=int(i[1])
                d=str(i[2])
                c=int(i[3])
                equation_set.append([a, b])
                self.equation.append([a, b, d, c])
                rhs.append(c)
        else:
            raise TypeError('Unexpected dimension of list given {0}, required list of dimension {1}X4 '.format(self.constrains,self.number_of_constrains))

        return equation_set, rhs

    def __minpoint(self,coordinates1,coordinates2):
        for i in coordinates1:
            if i < self.min:
                self.min=i

        for i in coordinates2:
            if i < self.min:
                self.min=i


    def __maxpoint(self,coordinates1,coordinates2):
        for i in coordinates1:
            if i >self.max:
                self.max=i
        for i in coordinates2:
            if i >self.max:
                self.max=i

    def __setvalue(self,eq, rhs, max_num):
        x = []
        y = []
        i = 0
        for j in eq:
            p, q = self.__setvalues(j[0], j[1], rhs[i])
            x.append([i for i in p])
            y.append([k for k in q])
            self.__maxpoint(p,q)
            self.__minpoint(p,q)
            i += 1

        i = 0
        sets = []
        while i < max_num:
            if i < max_num - 1:
                sets.append((i, i + 1))
            else:
                sets.append((max_num - 1, 0))
            i += 1

        i = 0
        for k in sets:
            setforeq = []
            setforrhs = []
            setforeq.append(eq[k[0]])
            setforeq.append(eq[k[1]])
            setforrhs.append(rhs[k[0]])
            setforrhs.append(rhs[k[1]])
            eq_arr = np.array(setforeq)
            rhs_arr = np.array(setforrhs)
            final_result = np.linalg.inv(eq_arr).dot(rhs_arr)
            x[i].append(float(final_result[0]))
            y[i].append(float(final_result[1]))
            if i < max_num - 1:
                x[i + 1].append(float(final_result[0]))
                y[i + 1].append(float(final_result[1]))
            else:
                x[0].append(float(final_result[0]))
                y[0].append(float(final_result[1]))
            i += 1
        self.__show_coordinates(x,y)
        self.__represent(x, y, max_num)

    def __show_coordinates(self,x,y):
        coordinates=[]

        for i in range(self.number_of_constrains):
            coordinates.append([(x[i][j],y[i][j]) for j in range(len(x[i]))])

        self.__finalresult(coordinates)

    def __satisfy(self,x,y):
        eqs=[]
        for eq in self.equation:
           if eq[2] == '<=':
               eqs.append((eq[0] * x + eq[1] * y) <= eq[3])
           elif eq[2] == '>=':
               eqs.append((eq[0] * x + eq[1] * y) >= eq[3])

        if False in eqs:
            #print ('fail: ({0:.2f},{1:.2f}) '.format(x,y),eqs)
            return False
        else :
            #print('({0:.2f},{1:.2f}) -> '.format(x, y),eqs)
            return True

    def __maximizeResult(self,res,x,y):

        if self.opt_res<res:
            self.opt_res=res
            self.at_x=x
            self.at_y=y

    def __minimizeResult(self,res,x,y):
        if self.itr!=0:
            if self.opt_res>res:
                self.opt_res=res
                self.at_x=x
                self.at_y=y
        else:
            if 10**6>res:
                self.opt_res=res
                self.at_x=x
                self.at_y=y
        self.itr+=1


    def __finalresult(self,coordi):
        if self.type!='min':
            if self.type!='max':
                raise TypeError("Unknown type found. Required 'min' or 'max', found {0}".format(self.type))
        finals= []
        for i in range(self.number_of_constrains):
            for j in coordi[i]:
                if j not in finals:
                    finals.append(j)

        finals.append((0,0))
        for i  in finals:
            k=self.optimize[0]*i[0]+self.optimize[1]*i[1]
            if self.__satisfy(i[0],i[1]):
                print("({0},{1}) -> {2:.2f}".format(i[0],i[1],k))
                if self.type=='max':
                    self.__maximizeResult(k,i[0],i[1])
                elif self.type=='min':
                    self.__minimizeResult(k,i[0],i[1])
            else:
                #print("k is ",k)
                continue

        print('\n\nOptimal Solution is: {0:.2f} at X={1:.2f} and Y={2:.2f} '.format(self.opt_res,self.at_x,self.at_y))

        def final_optimize():
            print('\n\nOptimal Solution is: {0:.2f} at X={1:.2f} and Y={2:.2f} '.format(self.opt_res, self.at_x,
                                                                                        self.at_y))