// DEPENDENCIA
const fs = require("fs");

// CAPACIDADE DO VEICULO
let capacity;

// PONTOS LATITUDE E LONGITUDE DAS ENTREGAS
let points = [];

// IDS DAS ENTREGAS
let ids = [];

// DEMANDA DAS ENTREGAS
demand = [];

if (process.argv.length < 5) {
  console.log("Parametros incorretos\n");
  console.log("Primeiro parametro: arquivo json original\n");
  console.log("Segundo parametro: Arquivo.vrp.sol\n");
  console.log("Terceiro parametro: destino do arquivo solução gerado\n");
  process.exit(1);
}

// LÊ A INSTÂNCIA JSON ORIGINAL 
let json = fs.readFileSync(`${process.argv[2]}`);

// CONVERTE A INSTANCIA PARA JSON
let converted = JSON.parse(json);

capacity = converted.vehicle_capacity;

// LÊ OS VALORES DO ARQUIVO ORIGINAL
for (var i = 0; i < converted.deliveries.length; i++) {
  points.push(converted.deliveries[i].point);
  demand.push(converted.deliveries[i].size);
  ids.push(converted.deliveries[i].id);
}

// VARIAVEL JSON A SER ESCRITA NO ARQUIVO FINAL
let outputJson = {};

// VETOR DE VEÍCULOS
let vehicles = [];

// VETOR DE ENTREGAS
let deliveries = [];


outputJson["name"] = process.argv[2];

// LÊ O ARQUIVO SOLUÇÃO DO FILO E CONVERTE PARA STRING
let file = fs.readFileSync(`${process.argv[3]}`).toString();
jsonSol = JSON.stringify(file);


// PARSER PARA ARMAZENAR SOMENTE OS PONTOS DAS ROTAS
let lines = jsonSol.split("\\n");
for (var i = 0; i < lines.length; i++) {
  lines[i] = lines[i].replace(/[""]/g, "").split(":").slice(1);
}
for (var i = 0; i < lines.length; i++) {
  lines[i] = (lines[i] + "".split(" ")).split(" ").slice(1);
}

// remove último elemento do array pois está vazio
lines.splice(-1, 1);

// COMPARA AS ROTAS COM AS ENTREGAS DO ARQUIVO ORIGINAL E ARMAZENA OS VALORES CORRETOS NOS VETORES
for (var i = 0; i < lines.length; i++) {
  for (var j = 0; j < lines[i].length; j++) {
    deliveries.push({
      id: ids[Number(lines[i][j]-1)],
      point: {
        lng: points[Number(lines[i][j]-1)].lng,
        lat: points[Number(lines[i][j]-1)].lat,
      },
      size: demand[Number(lines[i][j]-1)],
    });
  }
  vehicles.push({
    origin: {
      lng: converted.origin.lng,
      lat: converted.origin.lat,
    },
    deliveries: deliveries,
  });
  deliveries = [];
}

outputJson["vehicles"] = vehicles;

// CONVERTE O JSON PARA STRING PARA SER ESCRITO NO ARQUIVO
const outputStream = JSON.stringify(outputJson);
fs.writeFileSync(process.argv[4], outputStream);
