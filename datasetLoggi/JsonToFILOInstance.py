import json
import sys

if len(sys.argv) < 3:
    print("Parametros incorretos\n")
    print("Primeiro parametro: arquivo a ser convertido\n")
    print("Destino do arquivo convertido\n")
    sys.exit()

filePath = sys.argv[1]

# ABRE ARQUIVO LIDO DOS ARGUMENTOS
with open(filePath, "r") as data_file:
    json_data = data_file.read() 

data = json.loads(json_data)

# NOME DA INSTANCIA
nome = data["name"]

# CAPACIDADE DO VEICULO
capacidade = data["vehicle_capacity"]

# DADOS DAS ENTREGAS
deliveries = data["deliveries"]

# COORDENADAS DEPOSITO
originlng = data["origin"]["lng"]
originlat = data["origin"]["lat"]

# CABECARIO DO ARQUIVO DE SAIDA
output = open(sys.argv[2] + ".txt", "w")
output.write(f"NAME : {nome} \n")
output.write(f"COMMENT : \n")
output.write(f"TYPE : CVRP \n")
output.write(f"DIMENSION : {len(deliveries)+1}\n")
output.write(f"EDGE_WEIGHT_TYPE : EUC_2D \n")
output.write(f"CAPACITY : {capacidade} \n")
output.write(f"NODE_COORD_SECTION \n")
output.write(f"1 {originlng} {originlat}\n")

# COORDENADAS DAS ENTREGAS
counter = 2
for delivery in deliveries:
    output.write(f"{counter} {delivery['point']['lng']} {delivery['point']['lat']} \n")
    counter += 1

# SEÇÃO DE DEMANDA
output.write(f"DEMAND_SECTION\n")
output.write(f"1 0\n")
counter = 2
for delivery in deliveries:
    output.write(f"{counter} {delivery['size']} \n")
    counter += 1

# DEPOT SECTION E FINAL DO ARQUIVO
output.write(f"DEPOT_SECTION\n")
output.write(f"1\n-1\nEOF")
