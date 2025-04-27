import random
import sys
import numpy as np
import matplotlib.pyplot as plt

#------------------------------Constantes---------------------------------------------------
"""

s = "m" #La estrategia utilizada: m (martingala), d (D’Alambert), f (Fibonacci) y o (Suicida)
a = "f" #El tipo de capital: i (infinito), f (finito).
YYY=100
XXX=100

cfi = 100  #Cafital finito inicial
ci = "Auto" #Color inicial "R" (Rojo), "V" (Verde), "N" (Negro), "Auto" (Automatico)
"""

# Solicitar al usuario que ingrese la estrategia utilizada
s = input("Ingrese la estrategia utilizada (m para Martingala, d para D’Alambert, f para Fibonacci, o para Suicida): ").lower()

# Verificar si la estrategia ingresada es válida
while s not in ['m', 'd', 'f', 'o']:
    print("La estrategia ingresada no es válida. Por favor, ingrese m para Martingala, d para D’Alambert, f para Fibonacci, o para Suicida.")
    s = input("Ingrese la estrategia utilizada (m para Martingala, d para D’Alambert, f para Fibonacci, o para Suicida): ").lower()

# Solicitar al usuario que ingrese el tipo de capital
a = input("Ingrese el tipo de capital (i para Infinito, f para Finito): ").lower()

# Verificar si el tipo de capital ingresado es válido
while a not in ['i', 'f']:
    print("El tipo de capital ingresado no es válido. Por favor, ingrese i para Infinito, f para Finito.")
    a = input("Ingrese el tipo de capital (i para Infinito, f para Finito): ").lower()

# Solicitar al usuario que ingrese YYY
YYY = int(input("Ingrese el número de corridas (YYY): "))

# Solicitar al usuario que ingrese XXX
XXX = int(input("Ingrese el número de tiradas por corrida (XXX): "))

# Solicitar al usuario que ingrese cfi
cfi = int(input("Ingrese el capital finito inicial (cfi): "))

# Solicitar al usuario que ingrese ci
ci = input("Ingrese el color inicial (R para Rojo, V para Verde, N para Negro, Auto para Automático): ").capitalize()

# Verificar si el color inicial ingresado es válido
while ci not in ['R', 'V', 'N', 'Auto']:
    print("El color inicial ingresado no es válido. Por favor, ingrese R para Rojo, V para Verde, N para Negro, Auto para Automático.")
    ci = input("Ingrese el color inicial (R para Rojo, V para Verde, N para Negro, Auto para Automático): ").capitalize()

# Mostrar las constantes ingresadas por el usuario
print("\nConstantes ingresadas:")
print(f"Estrategia utilizada: {s}")
print(f"Tipo de capital: {a}")
print(f"Número de corridas (YYY): {YYY}")
print(f"Número de tiradas por corrida (XXX): {XXX}")
print(f"Capital finito inicial (cfi): {cfi}")
print(f"Color inicial: {ci}")



#-------------------------------------------------------------------------------------------

capital_money=[]
total_capital_money = []
chosen_colors=[]


def tipocapital(a):
    if(a=="i"):
        return float('inf')
    else:
        global cfi
        return cfi


def jugar(n): #Estrategia por color
    
    na = random.randint(0, 36)
    color_na = ""
    color_n = ""
    if (1 <= na <= 10) or (19 <= na <= 28):
        color_na = "R"
    elif na == 0:
        color_na = "V"
    else:
        color_na = "N"
    chosen_colors.append(color_na)
    

  
    global ci #Color inicial
    if(ci=="R"):
        color_n = "R"
    elif(ci=="V"):
        color_n = "V"
    elif(ci=="N"):
        color_n = "N"
    else:
        if chosen_colors:
            counts = {color: chosen_colors.count(color) for color in {"R", "V", "N"}}
            color_n = max(counts, key=counts.get)
        else:
            color_n = "R"
    return color_n == color_na

  #Siempre al doble y si ganas vuelves a empezar
def martingala(): 
    
    
    p = tipocapital(a)   # Presupuesto inicial
    apuesta = 1    # Apuesta inicial
    global XXX
    r=0
    while p >= apuesta and XXX != r:
        r +=1
        capital_money.append(p)
        resultado = jugar(apuesta)
        #print(f"Presupuesto: {p}, Apuesta: {apuesta}, Resultado: {'Gana' if resultado else 'Pierde'}")
        
        if resultado: 
            p += apuesta
            apuesta = 1  # Si ganas, reinicias la apuesta
        else: 
            p -= apuesta
            apuesta *= 2  # Si pierdes, duplicas la apuesta
    

def dalambert(): #Monto base y si pierde aumenta en uno, si gana reduce en uno
      
      
      p = tipocapital(a)# Presupuesto inicial
      apuesta_inicial = 1
      apuesta = apuesta_inicial    # Apuesta inicial
      global XXX
      r=0
      while p >= apuesta and XXX != r:
        r +=1
        capital_money.append(p)
        resultado = jugar(apuesta)
        #print(f"Presupuesto: {p}, Apuesta: {apuesta}, Resultado: {'Gana' if resultado else 'Pierde'}")
        
        if resultado: 
            p += apuesta
            apuesta = apuesta-1  # Si ganas, reinicias la apuesta
        else: 
            p -= apuesta
            apuesta = apuesta+1  # Si pierdes, duplicas la apuesta
        
        if apuesta<=0:
            apuesta = apuesta_inicial

def fibonacci():#1,1,2,3,5 el siguiente numero es la suma de los dos anteriores 
      
      
      p = tipocapital(a) # Presupuesto inicial
      apuesta = 1    # Apuesta inicial
      a1 =0 #apuesta anterior del anteior
      a2 =1 #apuesta anterior
      global XXX
      r=0
      while p >= apuesta and XXX != r:
        r +=1
        capital_money.append(p)
        resultado = jugar(apuesta)
        #print(f"Presupuesto: {p}, Apuesta: {apuesta}, Resultado: {'Gana' if resultado else 'Pierde'}")
        if resultado: 
            p += apuesta
        else: 
            p -= apuesta
        sa = apuesta+a1
        a1 = apuesta
        apuesta = sa
    

def suicida(): #juego el 65% de lo que tengo, si pierdo apuesto el 100% de lo que tengo, si gano apuesto el 65% de lo que tengo
      
      
      p = tipocapital(a)# Presupuesto inicial
      apuesta = p*0.65    # Apuesta inicial
      global XXX
      r=0
      while p >= apuesta and XXX != r:
        r +=1
        capital_money.append(p)
        resultado = jugar(apuesta)
        #print(f"Presupuesto: {p}, Apuesta: {apuesta}, Resultado: {'Gana' if resultado else 'Pierde'}")
        
        if resultado: 
            p += apuesta
            apuesta = p*0.65
        else: 
            p -= apuesta
            if(p!=0):
                apuesta=p
                
            
            
def strategy(l):
    global title
    if(l=="m"): title="Martingala"

    elif(l=="d"): title="Dalambert"

    elif(l=="f"): title="Fibonacci"

    elif(l=="o"): title="Suicida"

    else: title="Error"

    print(f"------------{title}------------")


    for i in range(YYY):
     capital_money.clear()
     if(l=="m"): martingala()

     elif(l=="d"): dalambert()

     elif(l=="f"): fibonacci()

     elif(l=="o"): suicida()
     
     total_capital_money.append(capital_money[:])

     
     
      
    

 

if(s in ("m", "d", "f", "o")):
    strategy(s)
    #Calculo de frecuencias relativas
    fv = chosen_colors.count('V')/len(chosen_colors)
    fr = chosen_colors.count('R')/len(chosen_colors)
    fn = chosen_colors.count('N')/len(chosen_colors)
    #----Graficar------

    fix, axs = plt.subplots(2)
    #Grafica de frecuencias


    categorias=['Rojo', 'Negro', 'Verde']
    axs[0].bar(categorias, [fr, fn, fv], color=['red', 'black', 'green'])
    axs[0].set_xlabel('Color')
    axs[0].set_ylabel('Frecuencia')
    axs[0].set_title('Frecuencia relativa')


    #Grafica de capital
    promedio = np.mean(total_capital_money[0])
    axs[1].plot(total_capital_money[0])
    axs[1].axhline(y=promedio, color='red', linestyle='-', label='Promedio')
    axs[1].set_xlabel('n (numero de tiradas)')
    axs[1].set_ylabel('cc (cantidad de capital)')
    axs[1].set_title(f"Gráfico de la primer tirada de la estrategia {title}")
    
 
    
    plt.legend()
    plt.tight_layout()
    plt.show()
else: print(f"La estrategia elegida {s} no existe por favor intente nuevamente, estrategias m (martingala), d (D’Alambert), f (Fibonacci) y o (Suicida)")






prom_list = []


for i in total_capital_money:
    
    plt.plot(range(len(i)), i, linestyle='-', )
    prom = np.mean(i)
    prom_list.append(prom)


plt.axhline(y=np.mean(prom_list), color='r', linestyle='-')

plt.xlabel('n (numero de tiradas)')
plt.ylabel('cc (cantidad de capital)')
plt.title('Gráfico general de todas las corridas')
plt.tight_layout()
plt.show()

