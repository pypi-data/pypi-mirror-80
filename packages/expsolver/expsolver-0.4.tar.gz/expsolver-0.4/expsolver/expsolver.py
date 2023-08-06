class Solver:
    """ 
        ***Purpose: Solve "exp = 0"***

        Inputs:
            a. exp: expression to be solved e.g. 2*x**2+3*x-100=0
        Solve:
            a. solve(): solves for "exp = 0"
        Outputs:
            a. get_order(): Integer order of equation "exp=0"
            b. get_root(): List of roots for "exp=0"
            c. get_delta(): List of "0-exp(root)"
            d. get_minima(): List of local minima
            e. get_maxima(): List of local maxima


        Determining order of equation:
            a. IF "**" in expression, find the highest value following the "**" as order
            b. Else if "*x" in expression, order is 1
            c. Else if "x" in expression, order is 1
            d. Else order is zero
            e. If any execption occurs in steps "a" through "d"
                   If "x" in expresssion, order= 10
                   else order = 0
            Order of expression is used to calculate the tolerance (xtol and ytol),since for higher orders,
            small changes in "x" can result in significant changes in expression value

        Determining roots of equation:
            a. Find a semi-random starting "x" value as a function of order
            b. create a list of "x" values (xlist) as [x, x+tol, x, x-tol]
            c. Evaluate exp for xlist to obtain ylist
            d. If ylist has a zero, append the x value to roots list
            e. If ylist[0]*ylist[1] < 0 indicating the root lies between xlist[0] and xlist[1]
               add the arithmetic mean of xlist[0] and xlist[1] to roots
            f. If ylist[2]*ylist[3] < 0 indicating the root lies between xlist[2] and xlist[3]
               add the arithmetic mean of xlist[2] and xlist[3] to roots
            g. Else make xlist as [x=x+tol, x+tol=x+2*tol, x=x-tol, x-tol=x-2*tol]
            h. Repeat steps a through f for a certain number of times (a large value, based on xtol)
            i. Change xtol = xtol / order and repeat step h till exp(roots) is within ytol around zero

         Determining maxima and minima:
             a. If the difference in ylist[0] and ylist[1] from ylist goes from negative to positive,
                add xlist[0] to minima 
             b. If the difference in ylist[0] and ylist[1] from ylist goes from positive to negative,
                add xlist[0] to maxima 
             b. If the difference in ylist[2] and ylist[3] from ylist goes from negative to positive,
                add xlist[2] to minima 
             b. If the difference in ylist[2] and ylist[3] from ylist goes from positive to negative,
                add xlist[2] to maxima            

    """
    
    def __init__(self, exp):
        ### Create expression variable ###
        self.exp=exp
        
    def solve(self):
        ### Determine order of expression ###
        ind=[0]
        try:
            if '**' in self.exp:
                while '**' in self.exp[ind[-1]:len(self.exp)+1] and ind[-1]+2<len(self.exp)-1:
                    ind.append(self.exp.find('**',ind[-1],len(self.exp))+2)
                order=0
                for i in ind:
                    if i>order:
                        order=int(self.exp[i])
            elif '*x' in self.exp:
                order=1
            elif 'x' in self.exp:
                order=1
            else:
                order=0
        except:
            if 'x' in self.exp:
                order=10
            else:
                order=0
        print('order='+str(order))
        ######################################
        
        ### Get roots ###
        xtol=0.1/order
        ytol=0.1*order
        min_abs_y=10**5
        i=0
        try:
            while min_abs_y>ytol:
                # Initialize values
                x1=order*2.1+1.5
                x2=x1+xtol
                x3=x1
                x4=x3-xtol
                xlist=[x1,x2,x3,x4]
                roots=[]
                minima=[]
                maxima=[]
                j=0
                while j<10**4/(xtol):
                    # Evaluate ylist
                    ylist=[eval(self.exp) for x in xlist]
                    
                    # Calculate roots
                    for y_ind in range(0,len(ylist)):
                        if ylist[y_ind]==0:
                            roots.append(xlist[y_ind])
                    if ylist[0]*ylist[1]<0:
                        roots.append((xlist[0]+xlist[1])/2)
                    if ylist[2]*ylist[3]<0:
                        roots.append((xlist[2]+xlist[3])/2)
                        
                    # Determine if minima or maxima
                    y_diff_1=ylist[1]-ylist[0]
                    y_diff_2=ylist[3]-ylist[2]
                    
                    if j>1:
                        if y_diff_1_old<0 and y_diff_1>0:
                            minima.append(xlist[0])
                        elif y_diff_1_old>0 and y_diff_1<0:
                            maxima.append(xlist[0])
                        if y_diff_2_old<0 and y_diff_2>0:
                            minima.append(xlist[2])
                        elif  y_diff_2_old>0 and y_diff_2<0:
                            maxima.append(xlist[2])
                        
                    y_diff_1_old=y_diff_1
                    y_diff_2_old=y_diff_2
                    
                    # Move X brackets
                    xlist[0]=xlist[1]
                    xlist[1]=xlist[0]+xtol
                    xlist[2]=xlist[3]
                    xlist[3]=xlist[2]-xtol
                    
                    # Update count
                    j=j+1
                i=i+1
                
                # Check for roots within ytol of zero
                y=[eval(self.exp) for x in roots]
                abs_y=[-1*x if x<0 else x for x in y]
                min_abs_y=abs_y[0]
                for k in range(1,len(abs_y)):
                    if abs_y[k]<min_abs_y:
                        min_abs_y=abs_y[k]
                xtol=xtol/order
        except Exception as err:
            print(err)
            print("Exception at iteration = {}".format(j))
            print("Exception at xlist = {}".format(xlist))
            print("Exception at ylist = {}".format(ylist))            
        ######################################
        
        ### Check Delta ###
        delta=[0-eval(self.exp) for x in roots]
        ######################################
        
        ### print ###
        self.order=order
        self.roots=roots
        self.delta=delta
        self.minima=minima
        self.maxima=maxima
        ######################################
        
    def get_order(self):
        return self.order
    def get_roots(self):
        return self.roots
    def get_delta(self):
        return self.delta
    def get_minima(self):
        return self.minima
    def get_maxima(self):
        return self.maxima