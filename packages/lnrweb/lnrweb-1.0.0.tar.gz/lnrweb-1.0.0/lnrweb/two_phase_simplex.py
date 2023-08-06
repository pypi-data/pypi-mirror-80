import numpy as np
'''
created by:Ashish Kumar
created on:15/09/20


User can solve any lpp question that can be solved by the simplex, it shows the simplex table and 
user itself as to find the relevent solution or details from the table.

@:exception
Solution in this package having error of approx +-0.010 value in the solution, so take round the final answer
with in this range.

If you find any problem in this package feel free to add issue here:- https://github.com/Ashish2000L/linear_programing
'''
class TPsimplex:
    '''
    @:param
    No_of_constrains:int->  This is the number of equations in the problem
    Number_of_costCoeff_in_equation:int->   This is the number of variables in total, i.e number of variable in the optimized function
    Optimize_type:str-> This is the type of solution user want i.e 'min'(Minimization) or 'max'(Maximation)
    equation:list->  This is the quation in the format [coeffs of cost cofficients,Inequality(string),rhs of the string], must be a multidimensional string.
                If the coefficient of any cost coefficient is 0 in any equation, mention it in the same order
    Optimize_equation:list-> This is you optimize equation
    '''

    def __init__(self,No_of_constrains:int,Number_of_costCoeff_in_equation:int,Optimize_type:str,equation:list,optimize_equation:list):
        self.number_of_constrains=No_of_constrains
        self.equation=equation
        self.optimize_fn=optimize_equation
        self.number_of_variables=Number_of_costCoeff_in_equation
        self.coeff_of_var=[]
        self.additional_var=[]
        self.coeff_of_rhs=[]
        self.basic_var=[]
        self.variable=[]
        self.optimize_final=[]
        self.main_matrix=[]
        self.artificial_var=[]
        self.entering_indx=0
        self.leaving_indx=0
        self.itr=0
        self.optimize_type=Optimize_type
        self.__check_equation()


    def __check_equation(self):

        if self.number_of_constrains!=len(self.equation):
            raise ValueError("Number of Constrains does not match with given number of equations ")
        elif self.optimize_fn is None:
            raise AssertionError("Optimize_equation cannot be null")
        elif len(self.optimize_fn)!=self.number_of_variables:
            raise ValueError('Length of coefficient in optimize function must be equal to number of variables\n'
                             'i.e if any coefficient having 0 coefficient, mention it as 0 instead of leaving that '
                             'blank in proper order')
        elif str(type(self.optimize_type))!="<class 'str'>":
            raise TypeError("Optimize_type must me string, given {0}".format(type(self.optimize_type)))
        elif (self.optimize_type!='max') and (self.optimize_type!='min'):
            raise ValueError("Optimize_type must be either 'max'(Maximation) or 'min'(Minimization) type only")

        for i in self.equation:
            if str(type(i))!="<class 'list'>":
                raise TypeError('List required, found {0}'.format(str(type(i))))
            elif len(i)==0:
                raise AssertionError('Coefficient of equation cannot be null')
            elif len(i)!=self.number_of_variables+2:
                raise ValueError('Inappropriate Equation found, please provide the equation in the given format \n'
                                 'i.e [Coefficient_of_variables,"Inequality",RHS_Coefficient_of_equation]')
            elif str(type(i[self.number_of_variables]))!="<class 'str'>":
                raise ValueError('Inequality must be string in given equation found {0}'.format(str(type(i[self.number_of_variables+1]))))
            elif i[self.number_of_variables] not in ['<=','>=','=']:
                raise ValueError("Only '<=','>=','=' type of inequality is allowed found {0}".format(i[self.number_of_variables]))

        self.__make_new_variables()


    def __make_new_variables(self):

        coeff_variable=[]
        additional_varialbe=[]
        rhs_of_equation=[0]
        basic_variable=['a ']
        opti_F=[0 for i in range(self.number_of_variables)]

        variabls=['X'+str(i+1) for i in range(self.number_of_variables)]

        k=0
        for i in range(self.number_of_constrains):
            additional_varialbe.append([])
            for j in range(self.number_of_constrains):
                additional_varialbe[k].append(0)
            k+=1

        k=0
        for i in self.equation:
            coeff_variable.append([])
            var = 1

            for j in i:

                if j=='<=':
                    additional_varialbe[k].pop(k-1)
                    additional_varialbe[k].insert(k, 1)
                    variabls.append('S'+str(k+1))
                    basic_variable.append('S' + str(k + 1))
                    opti_F.append(0)
                elif j=='>=':
                    #for l in range(k):
                        #coeff_variable[k].append(0)
                    coeff_variable[k].append(-1)
                    opti_F.insert(k,0)
                    opti_F.append(-1)
                    additional_varialbe[k].pop(k)
                    additional_varialbe[k].insert(k, 1)
                    variabls.insert(self.number_of_variables,'S'+str(k+1))
                    variabls.append('A'+str(k+1))
                    basic_variable.append('A' + str(k + 1))
                    self.artificial_var.append('A' + str(k + 1))
                elif j=='=':
                    additional_varialbe[k].pop(k - 1)
                    additional_varialbe[k].insert(k, 1)
                    variabls.append('A' + str(k+1))
                    basic_variable.append('A' + str(k + 1))
                    self.artificial_var.append('A' + str(k + 1))
                    opti_F.append(-1)

                if var==self.number_of_variables+2:
                    rhs_of_equation.append(j)

                if var<=self.number_of_variables:
                    coeff_variable[k].append(j)

                var += 1
            k+=1


        for i in coeff_variable:
            if len(i)!=self.number_of_variables:
                coeff_variable = self.__make_proper_matrix(coeff_variable)


        variabls.append('Sol')
        variabls.insert(0, 'BV')
        self.variable = variabls
        self.basic_var = basic_variable
        self.coeff_of_var=coeff_variable
        self.additional_var=additional_varialbe
        self.coeff_of_rhs=rhs_of_equation
        self.optimize_final=opti_F

        print("\n\nSTARTING SIMPLEX TABLE\n")
        self.__print_start_matrix()
        self.__make_initial_table()


    def __print_start_matrix(self):

        whole_matrix = [['a ']]

        main_whole_matrix=[]

        for i in self.optimize_final:
            whole_matrix[0].append(i)
        main_whole_matrix.append(self.optimize_final)

        p = 1
        for i in self.coeff_of_var:
            whole_matrix.append([])
            main_whole_matrix.append([])
            whole_matrix[p].append(self.basic_var[p])
            for j in i:
                whole_matrix[p].append(j)
                main_whole_matrix[p].append(j)
            p += 1

        p = 1
        for i in self.additional_var:

            for j in i:
                whole_matrix[p].append(j)
                main_whole_matrix[p].append(j)
            p += 1

        p = 0
        for i in self.coeff_of_rhs:
            whole_matrix[p].append(i)
            main_whole_matrix[p].append(i)
            p += 1

            self.main_matrix=main_whole_matrix

        for i in self.variable:
            print(i, end=' ')
        print('\r')
        for i in whole_matrix:
            for j in i:
                print(j, end='  ')
            print('\r')


    def __make_proper_matrix(self,coeff_var)->list:
        max=0
        for i in coeff_var:
            if len(i)>max:
                max=len(i)

        p=0
        for i in coeff_var:
            var=len(i)
            for j in range(max-var):
                coeff_var[p].append(0)
            p+=1

        return coeff_var


    def __make_initial_table(self):
        negatives=[]
        for index,value in enumerate(self.optimize_final):

            if value<0:
                negatives.append(index)

        vals = len(self.coeff_of_var[0])-1
        for i,v in enumerate(self.main_matrix):
            if i+vals in negatives:
                for j,k in enumerate(v):
                    self.main_matrix[0][j]=self.main_matrix[0][j]+k

        print('\n\nINITIAL SIMPLEX TABLE\n')
        self.__print_matrix()
        self.__process_simplex_phase_1()


    def __print_matrix(self):
        for i in self.variable:
            print(i,end=' ')
        print()
        p=0
        for i in self.main_matrix:
            print(self.basic_var[p],end='  ')
            for j in i:
                if j>=0:
                    print(j,end='  ')
                elif j<0:
                    print(j,end='  ')
            p+=1
            print()


    def __process_simplex_phase_1(self):
        print('\n\nPHASE-1\n')
        while not self.__check_for_optimal_table():
            self.__find_entry_indx()
            self.__find_leaving_indx()
            self.__set_enter_and_leave_val()
        print('\n\nPHASE-2\n')
        self.__process_simplex_phase_2()


    def __check_for_optimal_table(self,type='1_phase')->bool:
        if type=='1_phase':
            f=[self.main_matrix[0][i]  for i in range(len(self.main_matrix[0])-1)]

            for i in f:
                if i>0:
                    return False
            return True
        elif type=='min':
            f = [self.main_matrix[0][i] for i in range(len(self.main_matrix[0]) - 1)]

            for i in f:
                if i >0:
                    return False
            return True
        elif type=='max':
            f = [self.main_matrix[0][i] for i in range(len(self.main_matrix[0]) - 1)]

            for i in f:
                if i<0:
                    return False
            return True


    def __find_entry_indx(self,type='1_phase'):
        matrix=self.optimize_final

        f=[]
        self.entering_indx=None
        if type=='1_phase':
            max = 0
            for i,v in enumerate(matrix):
                if i<len(self.coeff_of_var[0]):
                    f.append(v)

            for i,v in enumerate(f):
                if v >max:
                    max=v
                    self.entering_indx=i
        elif type=='max':
            min=0
            for i, v in enumerate(self.main_matrix[0]):
                if i < len(self.main_matrix[0]) - 1:
                    f.append(v)

            for i, v in enumerate(f):
                if v < min:
                    min = v
                    self.entering_indx = i

        elif type=='min':
            max=0
            for i, v in enumerate(self.main_matrix[0]):
                if i < len(self.main_matrix[0]) - 1:
                    f.append(v)

            for i, v in enumerate(f):
                if v > max:
                    max = v
                    self.entering_indx = i


    def __check_for_other_alternative(self,min:int):

        ln=len(self.main_matrix[0])-1
        for i,v in enumerate(self.basic_var):
            b = self.main_matrix[i][ln]
            x = self.main_matrix[i][self.entering_indx]
            if v in self.artificial_var:
                if (float(b/x)==min):
                    self.leaving_indx=i


    def __find_leaving_indx(self, type='1_phase'):

        x=[]
        b=[]
        min = 10000
        self.leaving_indx=None
        if type=='1_phase':
            min = 10000
            l=len(self.optimize_final)-1
            for k in self.main_matrix:
                x.append(k[self.entering_indx])
                b.append(k[l])

            x.pop(0)
            b.pop(0)
            for i in range(len(x)):
                if x[i]>0 :
                    m=float(b[i]/x[i])
                    if m<min:
                        min=m
                        self.leaving_indx=i+1

            self.__check_for_other_alternative(min)

        elif type=='max':

            l = len(self.main_matrix[0])-1
            for k in self.main_matrix:
                x.append(k[self.entering_indx])
                b.append(k[l])

            x.pop(0)
            b.pop(0)

            for i in range(len(x)):
                if x[i] > 0:
                    m = float(b[i] / x[i])
                    if m < min:
                        min = m
                        self.leaving_indx = i+1

        elif type=='min':

            l = len(self.main_matrix[0]) - 1
            for k in self.main_matrix:
                x.append(k[self.entering_indx])
                b.append(k[l])

            x.pop(0)
            b.pop(0)

            for i in range(len(x)):
                if x[i] > 0:
                    m = float(b[i] / x[i])
                    if m < min:
                        min = m
                        self.leaving_indx = i + 1


    def __set_enter_and_leave_val(self):

        temp_index=0
        temp_list1=[]
        temp_list2=[]

        enter=self.variable[self.entering_indx+1]
        leave=self.basic_var[self.leaving_indx]
        self.basic_var.pop(self.leaving_indx)
        self.basic_var.insert(self.leaving_indx,enter)
        for i,v in enumerate(self.variable):
            if v==leave:
                temp_index=i-1

        for i in self.main_matrix:
            temp_list1.append(i[temp_index])
            temp_list2.append(i[self.entering_indx])

        for i in range(len(self.main_matrix)):
            self.main_matrix[i][self.entering_indx]=temp_list1[i]


        k=temp_list2[self.leaving_indx]


        for i,v in enumerate(self.main_matrix[self.leaving_indx]):
            if i!=self.entering_indx:
                self.main_matrix[self.leaving_indx][i]=round(float(v/k),3)

        temp_leav_val_list=self.main_matrix[self.leaving_indx]

        for i,v in enumerate(self.main_matrix):
            if i!=self.leaving_indx:
                m=temp_list2[i]*-1
                for k,j in enumerate(v):
                    if k !=self.entering_indx:
                        self.main_matrix[i][k]=float(format(j+(m*temp_leav_val_list[k]),'.3f'))

        self.itr+=1
        print('\n\nITERATION {0}\n'.format(self.itr))
        self.__print_matrix()


    def __process_simplex_phase_2(self):
        pop_indx=[]
        F=[]
        length=len(self.variable)-1
        while length>=0:
            for j in self.artificial_var:
                if j==self.variable[length]:
                    pop_indx.append(length-1)
                    self.variable.pop(length)
            length-=1



        for i,v in enumerate(self.main_matrix):
            for j in pop_indx:
                v.pop(j)
            self.main_matrix[i]=v

        l=len(self.main_matrix[0])

        for i in self.optimize_fn:
            F.append(float(i*-1))

        for i in range(l-len(F)):
            F.append(float(0))

        self.main_matrix.pop(0)
        self.basic_var.pop(0)
        self.basic_var.insert(0,'F ')
        self.main_matrix.insert(0,F)


        self.__print_matrix()

        temp_indx=[]
        z=[]
        for i in self.basic_var:
            for j,v in enumerate(self.variable):
                if i==v:
                    temp_indx.append((j-1,v))
                    z.append(j-1)

        k=[]

        for i,v in enumerate(self.main_matrix[0]):
            if i in z:
                if v !=0:
                    for j in temp_indx:
                        if j[0]==i:
                            k.append(j)

        temp_indx.clear()
        for i in k:
            for j,v in enumerate(self.basic_var):
                if i[1]==v:
                    temp_indx.append((i[0],j))

        F=self.main_matrix[0]
        for i in temp_indx:
            for j,v in enumerate(self.main_matrix):
                if j==i[1]:
                    k=F[i[0]]*-1
                    for x,y in enumerate(v):
                        F[x]=round(F[x]+(y*k),3)

        self.main_matrix[0]=F

        print('\n\nINITIAL SIMPLEX TABLE\n')
        self.__print_matrix()
        self.__process_simplex_final_phase()


    def __process_simplex_final_phase(self):
        while not self.__check_for_optimal_table(type=self.optimize_type):
            self.__find_entry_indx(type=self.optimize_type)
            self.__find_leaving_indx(type=self.optimize_type)
            self.__set_enter_and_leave_val()


    def Optimal_Solution(self)-> "numpy array":

        ln=len(self.main_matrix[0])-1
        if self.main_matrix[0][ln]>0:
            print("\n\n\nSOLUTION:\n")
            self.__print_matrix()
            final_solution=[['F',self.main_matrix[0][ln]]]

            cost_coeff_var=['X'+str(i+1) for i in range(self.number_of_variables)]
            for i,v in enumerate(self.basic_var):
                if v in cost_coeff_var:
                    final_solution.append([v,self.main_matrix[i][ln]])

            return np.asarray(final_solution)
        else:
            raise Exception("\n\nEither the equation have not fisible solution or an error occured.\n Please staceback to look for the issue, if you find this solution wrong you can create an issue here: \n https://github.com/Ashish2000L/linear_programing")
