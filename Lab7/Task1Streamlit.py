#import statements
import streamlit as st
import streamlit.components.v1 as components
from src.CSPclass import CSP
from src.utils import parse_neighbors
from src.algorithms import *
from pyvis.network import Network

#CSP interpretation
variables = ["Seat_1", "Seat_2", "Seat_3", "Seat_4", "Seat_5", "Seat_6"] #putting this here otherwise the CSP considers the seats as the variables
domain = { 'Seat_1': ["A", "B", "C", "D", "E", "empty"],
           'Seat_2': ["A", "B", "C", "D", "E", "empty"],
           'Seat_3': ["A", "B", "C", "D", "E", "empty"],
           'Seat_4': ["A", "B", "C", "D", "E", "empty"],
           'Seat_5': ["A", "B", "C", "D", "E", "empty"],
           'Seat_6': ["A", "B", "C", "D", "E", "empty"]}
seats = 'Seat_1: Seat_2; Seat_2: Seat_3; Seat_3: Seat_4; Seat_4: Seat_5; Seat_5: Seat_6; Seat_6: Seat_1'
neighbors = parse_neighbors(seats)
#big constraint portion to make sure that the neighboring seats to B can only be empty or D (since problems with A, C, and E)
def seat_constraint(X, x, Y, y):
    notOK = {("A", "B"), ("C", "B"), ("E", "B"), ("B", "A"), ("B", "C"), ("B", "E")}
    return (x, y) not in notOK
constraint = seat_constraint
#making the actual CSP thing
lab7CSP = CSP(variables, domains=domain, neighbors=neighbors, constraints=constraint)
AC3(lab7CSP)

#streamlit initialization for AC3
#net_lab7.show("Lab7_Seating_CSP.html", notebook=False)

def buildGraph(CSP, backTrackColor = None):
    net_lab7 = Network(heading = "Lab 7 Task 1",
                   bgcolor ="#1C1919",
                   font_color = "white",
                   height = "750px",
                   width = "100%",
                   directed= False)
    nodeColors = { #we making this rainbow because why not (easiest way for 6 different colors imo)
        "Seat_1": "red",
        "Seat_2": "orange",
        "Seat_3": "orange",
        "Seat_4": "yellow",
        "Seat_5": "orange",
        "Seat_6": "orange"
    }
    nodes=CSP.variables
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
        for j in CSP.domains[node]:
            seats_domain += " " + str(j)
        net_lab7.add_node(node, color=nodeColors[node], title=seats_domain, size=sizes[i], x=x_coords[i], y=y_coords[i])

    for nodeFrom in CSP.neighbors.keys():
        for nodeTo in CSP.neighbors[nodeFrom]:
            net_lab7.add_edge(nodeFrom, nodeTo, color="white")

    net_lab7.toggle_physics(False)


    net_lab7.save_graph('Lab7Task1.html')
    HtmlFile = open(f'Lab7Task1.html', 'r', encoding='utf-8')
    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height = 800,width=1500)


if 'CSP' not in st.session_state:
    CSP = lab7CSP
    st.session_state.CSP = CSP
else:
    CSP = st.session_state.CSP


st.set_page_config(layout="wide")
st.title("Lab 7 Task 1")


placeholder = st.empty()

run_full = st.button("Run Full Solution")
reset_clicked = st.button("Reset")

if run_full:
    placeholder.empty()
    result = backtracking_search(CSP)
    with placeholder:
        buildGraph(result)

elif reset_clicked:
    placeholder.empty()
    with placeholder:
        buildGraph(CSP)

else:
    # initial render
    with placeholder:
        buildGraph(CSP)