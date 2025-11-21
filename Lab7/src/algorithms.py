from queue import Queue

from src.utils import first

from pyvis.network import Network

def AC3(csp):
  queue = Queue()
  
  print(f"Initial queue:")
  for Xi in csp.variables:
    for Xk in csp.neighbors[Xi]:
      queue.put((Xi, Xk))
      print((Xi, Xk), end=" ")
    print()
   
  csp.support_pruning()
  checks = 0
  while list(queue.queue):
    (Xi, Xj) = queue.get()
    #print(f'Arc {(Xi, Xj)} is cheking')
    revised, checks = revise(csp, Xi, Xj, checks)
    if revised:
      if not csp.curr_domains[Xi]:
        return False, checks  # CSP is inconsistent
      for Xk in csp.neighbors[Xi]:
        if Xk != Xj:
          queue.put((Xk, Xi))
    print(f"Queue: {list(queue.queue)}")

    '''print(f'Arc {(Xj, Xi)} is cheking')
    revised, checks1 = back_revise(csp, Xi, Xj, checks)
    if revised:
      if not csp.curr_domains[Xj]:
        return False, checks  # CSP is inconsistent
      for Xk in csp.neighbors[Xj]:
        if Xk != Xi:
          queue.add((Xk, Xj))'''

      
  return True, checks  # CSP is satisfiable


def revise(csp, Xi, Xj, checks=0):
    """Return true if we remove a value."""
    revised = False
    print(f'Arc {(Xi, Xj)} is cheking')
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
        conflict = True
        #print(csp.curr_domains[Xj])
        for y in csp.curr_domains[Xj]:
            if csp.constraints(Xi, x, Xj, y):
                conflict = False
            checks += 1
            if not conflict:
                break
        if conflict:
            csp.prune(Xi, x)
            print(f'The val {x} was deleted from {Xi} domain')
            revised = True
    return revised, checks


def back_revise(csp, Xi, Xj, checks=0):
    """Return true if we remove a value."""
    revised = False
    for x in csp.curr_domains[Xi][:]:
        conflict = False
        for y in csp.curr_domains[Xj]:
            conflict = False
            #print(y)
            if csp.constraints(Xi, x, Xj, y)==False:
              #print(x,y)
              conflict = True
            checks +=1
            '''if not conflict:
                break'''
            if conflict:
              csp.prune(Xj, y)
              print(f'The val {y} was deleted from {Xj} domain')
              #print(y)
              revised = True
    return revised, checks


# CSP Backtracking Search Section
# Variable ordering
def first_unassigned_variable(assignment, csp):
    """The default variable order."""
    return first([var for var in csp.variables if var not in assignment])


# Value ordering
def unordered_domain_values(var, assignment, csp):
    """The default value order."""
    return csp.choices(var)

#old version of backtracking search (for reference)
# def backtracking_search(csp, select_unassigned_variable=first_unassigned_variable, order_domain_values=unordered_domain_values):
    
#     def backtrack(assignment):
#         if len(assignment) == len(csp.variables):
#             return assignment

#         var = select_unassigned_variable(assignment, csp)
#         for value in order_domain_values(var, assignment, csp):
#             if csp.nconflicts(var, value, assignment)==0:
#                 csp.assign(var, value, assignment)
#                 result = backtrack(assignment)
#                 if result is not None:
#                   return result
                
#             csp.unassign(var, assignment)
#         return None

#     result = backtrack({})
#     return result

def buildGraph(csp):
  net_backtrack = Network(heading = "Lab 7 Task 1",
                   bgcolor ="#1C1919",
                   font_color = "white",
                   height = "750px",
                   width = "100%",
                   directed= False)
  nodeColors = { 
        "Seat_1": "red",
        "Seat_2": "orange",
        "Seat_3": "orange",
        "Seat_4": "yellow",
        "Seat_5": "orange",
        "Seat_6": "orange"
    }
  nodes=csp.variables
  sizes=[10]*len(nodes)

  x_coords = []
  y_coords = []
  for node in nodes:
        if node.lower()=="seat_1":
            x_coords.append(0)
            y_coords.append(0)
        elif node.lower()=="seat_2":
            x_coords.append(50)
            y_coords.append(50)
        elif node.lower()=="seat_3":
            x_coords.append(50)
            y_coords.append(125)
        elif node.lower()=="seat_4":
            x_coords.append(0)
            y_coords.append(175)
        elif node.lower()=="seat_5":
            x_coords.append(-50)
            y_coords.append(125)
        elif node.lower()=="seat_6":
            x_coords.append(-50)
            y_coords.append(50)

  for i, node in enumerate(nodes):
        seats_domain = ""
        for j in csp.domains[node]:
            seats_domain += " " + str(j)
        net_backtrack.add_node(node, color=nodeColors[node], title=seats_domain, size=sizes[i], x=x_coords[i], y=y_coords[i])

  for nodeFrom in csp.neighbors.keys():
        for nodeTo in csp.neighbors[nodeFrom]:
            net_backtrack.add_edge(nodeFrom, nodeTo, color="white")

  net_backtrack.toggle_physics(False)
  net_backtrack.show("Lab 7 Backtracking.html", notebook=False)

def backtracking_search(csp, select_unassigned_variable=first_unassigned_variable, order_domain_values=unordered_domain_values):
    used = []
    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment

        var = select_unassigned_variable(assignment, csp)
        print("\n")
        print("var = ",var)
        for value in order_domain_values(var, assignment, csp):
            print("value = ",value)
            if csp.nconflicts(var, value, assignment)==0:
                print("value can sit beside eachother")
                if value not in used:
                  print("value ", value, " accepted")
                  csp.assign(var, value, assignment)
                  used.append(value)
                  result = backtrack(assignment)
                  if result is not None:
                    return result
                else: print("value is already used")
            else: print("value conflicts with a neighbor")
            csp.unassign(var, assignment)

        return None
    result = backtrack({})
    return result
