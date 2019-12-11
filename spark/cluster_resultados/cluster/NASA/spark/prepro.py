import string

#Lee las cabeceras de un archivo lbl
def read_headers(pathe , comp = "NAME"):
    lb = open(pathe , "r");
    cab = [];
    for i in lb:
       cont = 0; 
       for value in i.split():
           if( (cont == 0) & (value == "NAME")):
                cont += 1; 
           elif ( cont == 1) :
                cont += 1; 
           elif ( cont == 2) :
                cab.append(value);
    return cab
