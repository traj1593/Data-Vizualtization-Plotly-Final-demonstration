'''
Program: Final Project
Filename: finalProject-tRaj-00.py
Author: Tushar Raj
Description: Importing the CSV file and filtering the record as per need and then drawing the graph using the plotly
Revisions: No revisions made
'''

import csv #imprting to read from csv
from datetime import datetime #to handle datetime data from excel
import plotly.offline as plty # importing plotly to draw graphs
import plotly.graph_objs as pg

#There are no literal constraint
#There are no class defined

def average(a):
    '''
    Parameters
    ----------
    a : list
    takes price value from list to calculate the average.

    Returns
    -------
    flaat type
    returns the average of the price.

    '''
    length=len(a)
    return 0 if length == 0 else float(sum(a)/length) #returns average

print("**** Final project ****\n\n")

file = csv.reader(open('produce_csv.csv','r')) #Opening the produce csv and reading it
data = [i for i in file] #iterating each line and storing it as list

modList = [] #creating the empty list to store modified list
for i in data: #iterating through the the list
    changedList=list()
    for j in i:
        if "$" in j:
            changedList.append(float(j.replace("$",""))) # replacing the $ sign with null vlaue
        elif "/" in j: 
            changedList.append(datetime.strptime(j,'%m/%d/%Y')) #changing the sting format of date into date format
        else:
            changedList.append(j)  
    modList.append(changedList) # appending the changed list into master list

locations = modList.pop(0)[2:] #removing the header
records = [] # creating an empty list
for row in modList: 
    newRow = row[:2] #storing the first 2 row in new variable
    for loc,price in zip(locations,row[2:]): # location and prices and appended with the first first two rows
        records.append(newRow + [loc,price]) # new data is added to record

try: #catching the index exception when user enetr out of bound index
    city=sorted(locations) #sorting the city in file
    comodity = sorted(set([i[0] for i in modList])) #retrieving and sorting the the product
    dates=sorted(set([ i[1] for i in modList ])) # retreving and sorting the dates
    
    ### Dispalying and accepting user input for city
    [print(f"<{i+1}> {j}") for i,j in enumerate(city)]
    a=input("Enter location numbers separated by spaces:  ").split()
    city_value=[city[int(i)-1] for i in a]
    city_value_print=city_value
    print("\n")
    
    ### Dispalying and accepting user input for Product
    [print(f"<{i+1}> {j}") for i,j in enumerate(comodity)]
    b=input("Enter product numbers separated by spaces:  ").split()
    comodity_name=[comodity[int(i)-1] for i in b]
    print("\n")
    
    ### Dispalying and accepting user input for Dates
    [print(f"<{i+1}> {str(j).split()[0]}") for i,j in enumerate(dates)]
    print(f"Earliest available date is: {min(dates)}")
    print(f"Latest available date is: {max(dates)}")
    c=input("Enter start/end date numbers separated by a space:  ").split()
    dates_value=[dates[int(i)-1] for i in c]
    print("\n")
    
    #Creating the final list based for user selected condition
    final_list_graph = [i for i in records if((i[0] in comodity_name) and (min(dates_value) <= i[1] <= max(dates_value)) and (i[2] in city_value_print))]
    # Creating Graph
    final_list_graph_dict = {i:[] for i in city_value} # creating dictonary where location is the key as it is the filtering condition of graph
    for i in final_list_graph_dict:
            for j in comodity_name:
                final_list_graph_dict[i].append(average([k[3] for k in final_list_graph if k[0] == j and k[2] == i]))       # creating dictonary where location is the key as it is the filtering condition of graph and appending average and other  
    
    graph_value = []
    for city_value,average in final_list_graph_dict.items():
         graph_value.append(pg.Bar(x=comodity_name,y=average,name=city_value))
    
    ### Print the values for which graph is being generated
    print("Values for which graph will be generated:\n")     
    print("Selected City :") ### Print the city for which graph is being generated
    [print(i) for i in city_value_print]
    print("\nSelected Product :") ### Print the Product for which graph is being generated
    [print(i) for i in comodity_name]  
    print(f"\nSelected dates range: {min(dates_value)} - {max(dates_value)}\n") ### Print the dates for which graph is being generated
    
    print(f'{len(final_list_graph)} records have been selected.\n')
    print("RECORDS SELECTED  ....\n")
    [print(f"<{i}> {j}") for i,j in enumerate(final_list_graph)]

    my_dict={} # creating a empty dictonary
    for loc in final_list_graph: 
        if(loc[0]+"-"+loc[2] in my_dict): #creating procduct and place as one unit and storing as key
            my_dict[loc[0]+"-"+loc[2]] = my_dict[loc[0]+"-"+loc[2]] +1 # incrementing the count if its there
        elif(loc[0]+"-"+loc[2] not in my_dict):
            my_dict[loc[0]+"-"+loc[2]] = 1 #assigning the value as one if its not there and encountered as 1
    
    for loc in my_dict:
        print(f"{str(my_dict[loc])} prices for {loc.split('-')[0]} in {loc.split('-')[1]}") #printing the result
 
    
    graph_header = 'Produce Prices from '+datetime.strftime(min(dates_value),"%Y-%m-%d")+' through '+datetime.strftime(max(dates_value),"%Y-%m-%d")
    graph_layout = pg.Layout(barmode='group',
                       title=dict(text='<b>'+graph_header+'</b>', x=0.50, xanchor="center"), #formating title
                       xaxis=dict(title='Product'), #formating x axis
                       yaxis=dict(title='Average Price',tickprefix="$",tickformat=".2f"), #formating y axis
                       font=dict(family="sans-serif",size=20,color="#FF0000"), #fomrating fond
                       paper_bgcolor='rgb(255,255,255)', # putting screen background color
                       plot_bgcolor='rgba(0,0,0)' #putting graph background color
                       )
        
    #Plot the graph and saving it in a html format
    fig = pg.Figure(data=graph_value, layout=graph_layout)
    plty.plot(fig, filename='tushar_final_project.html')
    
    print("\n\n**** Final Project Ended****\n\n")

except IndexError: # catching the Index exception
    print("Entered index value is not in list. Please Try again !")