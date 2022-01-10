import json 
from treelib import Node, Tree
import jsonpath
import sys
class Employee:
  def __init__(self,id,first_name,manager,salary):
    # according to the input file, each Employee has the following 4 properties
      self.id=id
      self.first_name=first_name
      self.manager=manager
      self.salary=salary

  def to_string(self):
      return {"id":self.id,
              "first_name":self.first_name,
              "manager":self.manager,
              "salary":self.salary}

class Manager(Employee):
    def __init__(self,id,first_name,manager,salary,list_followers):
        super().__init__(id,first_name,manager,salary)
    # manager inherits the properties of employee with one additional property, list of followers
        self.list_followers=list_followers
    def print_manager(self):
        print(self.first_name," has ",len(self.list_followers),"direct followers")

gint_total_salary=0

# -----------------------------------------------------------------------------------------------------------------
# Description: the function generates a dictionary which contains information of all employees
# Input: read json data
# output: 
#           {
#              "2":Manager("Jeff")
#              "1":Manager("Dave")
#              "3":Employee("Andy")
#                     :
#           }
#           b1. each item/key in the dictionary represents ID of given employee  
#           b1. if a given member has direct followers, then his/her information is encapsulated as Manager object, 
#               otherwises are encapsulated as Employee object. 
# -----------------------------------------------------------------------------------------------------------------
def genEmployeesDict(data): 
    dict_company={}
    int_root_id=0
    for i in range(0,len(data)):
        str_id=str(data[i]['id'])
        list_followers=[]
        if data[i]['manager']==None:
            # find the id of boss/root
            int_root_id=data[i]['id']
        for j in range(0,len(data)):
            # collect followers of given manager
            if data[i]['id']==data[j]['manager']:
                list_followers.append(Employee(data[j]['id'],data[j]['first_name'],data[j]['manager'],data[j]['salary']))
        if len(list_followers)!=0:
            # save property of given manager as an object of Manager
            dict_company[str_id]=Manager(data[i]['id'],data[i]['first_name'],data[i]['manager'],data[i]['salary'],list_followers)
        else:
            # save property of given employee, who has no followers, as an object of Employee
            dict_company[str_id]=Employee(data[i]['id'],data[i]['first_name'],data[i]['manager'],data[i]['salary'])
    return [dict_company,int_root_id]

# -----------------------------------------------------------------------------------------------------------------
# Description: The function recursively disaply tree type by the given dictionary instance
# Input: 
#   a.bool_sort: The flag determines the result (tree) is sorted or unsorted
#   b.str_space: The space size 
#   c.dict_company: the output generated by function genEmployeesDict
#   d.int_started_id: the starting point (id of employee) for recursive display
# output: 
#   the tree structure displays in the console
# -----------------------------------------------------------------------------------------------------------------
def showTree(bool_sort,str_space,dict_company,int_started_id):
    print(str_space,dict_company[str(int_started_id)].first_name)
    list_followers=[]
    if isinstance(dict_company[str(int_started_id)],Manager)==True:
        list_followers=dict_company[str(int_started_id)].list_followers        
    salary=dict_company[str(int_started_id)].salary
    global gint_total_salary
    gint_total_salary+=salary
    # if the given member has followers, recursively display the followers
    if len(list_followers)!=0:
        print(str_space,"Employees of:",dict_company[str(int_started_id)].first_name)
        str_space+="         "
    if bool_sort==True:     
        list_followers.sort(key=lambda x:x.first_name)    
    for i in range(0,len(list_followers)):
        started_id=str(list_followers[i].id)
        # recursively display the tree
        showTree(bool_sort,str_space,dict_company,started_id)

# -----------------------------------------------------------------------------------------------------------------
# Description: the function recursively disaply tree type by the given dictionary instance and treelib
# Input: 
#   a.tree: the tree node of treelib 
#   b.bool_sort: The flag determines the result (tree) is sorted or unsorted
#   c.str_space: The space size 
#   d.dict_company: the output generated by function genEmployeesDict
#   e.int_started_id: the starting point (id of employee) for recursive display
# output: 
#   the tree structure of treelib displays in the console
# -----------------------------------------------------------------------------------------------------------------
def showByTreelib(tree, bool_sort,str_space,dict_company,int_started_id):
    list_followers=[]
    if isinstance(dict_company[str(int_started_id)],Manager)==True:
        list_followers=dict_company[str(int_started_id)].list_followers     
    if len(list_followers)!=0:
        str_parent_name=dict_company[str(int_started_id)].first_name
        str_space+="         "
    if bool_sort==True:     
        list_followers.sort(key=lambda x:x.first_name)    
    for i in range(0,len(list_followers)):
        started_id=str(list_followers[i].id)
        str_child_name=str(list_followers[i].first_name)
        # recursively build the tree of Treelib
        tree.create_node(str_child_name,str_child_name,str_parent_name)
        showByTreelib(tree,bool_sort,str_space,dict_company,started_id)
  
# -----------------------------------------------------------------------------------------------------------------
# Description: the function shows how many followers each manager have
# Input: the dictionary generated by function genEmployeesDict
# output: how many followers each manager have
# -----------------------------------------------------------------------------------------------------------------
def showManager(dict_company):
    print(">------------------------------------<")
    print(">        manager information         <")
    print(">------------------------------------<")
    for key in dict_company:
        if isinstance(dict_company[key], Manager)==True:
            dict_company[key].print_manager()
    print("")

# -----------------------------------------------------------------------------------------------------------------
# Description: the function checks the integrity and correctness of input JSON data
# Input: the JSON data read from file
# output: incorrectness found in the data if any
# -----------------------------------------------------------------------------------------------------------------
def checkInputDataIntegrity(data):
    list_error_msg=[]
    # id's integrity/correctness check
    list_id=jsonpath.jsonpath(data, '$..*.id')
    str_error=""
    for i in range(0,len(list_id)):
        if isinstance(list_id[i],int)==False:
            str_error="id is not an integer: obj#"+str(i)
            list_error_msg.append(str_error)
    # check if employees share the same id
    set_id=set(list_id)
    if len(list_id)!=len(set_id):
        list_error_msg.append("employees share the same id")

    # integrity/correctness check for first_name, salary, manager
    for i in range(0,len(data)):
        if isinstance(data[i]["first_name"],str)==False:
            str_error="first_name is not a string: obj#"+str(i)
            list_error_msg.append(str_error)
        if isinstance(data[i]["manager"],int) and data[i]["manager"]<0:
            str_error="manager is a negative number: obj#"+str(i)
            list_error_msg.append(str_error)
        if isinstance(data[i]["salary"],int)==False:
            str_error="salary is not an integer: obj#"+str(i)
            list_error_msg.append(str_error)
        else:
            if data[i]["salary"]<0:
                str_error="salary is a negative number: obj#"+str(i)
                list_error_msg.append(str_error)
    return list_error_msg

def main(file_name):
    try:
        with open(file_name) as f:
            try:
                data = json.load(f)
            except ValueError:
                print('Decoding JSON has failed. Please check if input file has correct JSON format')
                sys.exit()
    except OSError:
        print("Could not open/read file",file_name," Please double check the file name")
        sys.exit()

    list_error_msg=checkInputDataIntegrity(data)
    if len(list_error_msg)!=0:
        print("Data integrity/correctness check failed because of:")
        for i in range(0,len(list_error_msg)):
            print(i+1,":",list_error_msg[i])
        sys.exit()
    int_data_salary=0
    for i in range(0,len(data)):
        int_data_salary+=data[i]['salary']
    dict_company,int_root_id=genEmployeesDict(data)
    space=""
    global gint_total_salary
    gint_total_salary=0
    # Print unsorted tree structure

    print("**************************************")
    print("*        unsorted tree type          *")
    print("**************************************")
    showTree(False,space,dict_company,int_root_id)
    print("Total salary:",gint_total_salary)
    print("")

    print("**************************************")
    print("*        sorted tree type            *")
    print("**************************************")
    gint_total_salary=0
    # Print alphabetically sorted tree structure
    showTree(True,space,dict_company,int_root_id)
    print("Total salary:",gint_total_salary)
    print("")

    print("**************************************")
    print("*       sorted tree by treelib       *")
    print("**************************************")
    tree = Tree()
    tree.create_node(dict_company[str(int_root_id)].first_name, dict_company[str(int_root_id)].first_name)  # No parent means its the root node
    showByTreelib(tree,True,space,dict_company,int_root_id)
    tree.show(line_type="ascii-em")
    print("")
    showManager(dict_company)
    return [gint_total_salary,dict_company,int_root_id,int_data_salary]
    
def unit_tests(file_name):    
    [gint_total_salary,dict_company,int_root_id,int_data_salary]=main(file_name)
    assert isinstance(int_root_id, int)
    assert int_root_id>=0
    assert isinstance(gint_total_salary, int)
    assert gint_total_salary>0
    #check if the two total salary numbers calucated by two different methods are the same or not 
    assert gint_total_salary==int_data_salary
    assert isinstance(dict_company,dict)
    for ele in jsonpath.jsonpath(dict_company, '$..*'):
        # check if all values in company's dictionary are either Manager or Employee object
        assert isinstance(ele, Manager) or isinstance(ele, Employee) 
        # check if id of each object is an integer, not None, and not 0 
        assert ele.id!=None and ele.id!=0 and isinstance(ele.id,int)
        # check if first_name of each object is a string, not None, and not "" 
        assert ele.first_name!=None and ele.first_name!="" and isinstance(ele.first_name,str)
        # check if salary of each object is an integer, not None, and not 0 
        assert ele.salary!=None and ele.salary!=0 and isinstance(ele.salary,int)
        if ele.manager!=None:
            # check if manager of each object is integer, and not 0 
            assert ele.manager!=0 and isinstance(ele.manager,int)
        if isinstance(ele, Manager):
            # if the object is a Manager, check if list_followers is a list, not None, and length of list is not 0
            assert ele.list_followers!=None and isinstance(ele.list_followers, list) and len(ele.list_followers)!=0
            
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print(">       test with employee1.json started      >")
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
unit_tests('employee1.json')

print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print(">       test with employee2.json started      >")
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
unit_tests('employee2.json')

print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print(">       test with employee3.json started      >")
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
unit_tests('employee3.json')

print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print(">       test with employee4.json (with problems) started      >")
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
unit_tests('employee4.json')



