const fs = require("fs");

let capacity;
let points = [];
demand = [];

if (process.argv.length < 4) {
  console.log("Parametros incorretos\n");
  console.log("Primeiro parametro: arquivo a ser convertido\n");
  console.log("Destino do arquivo convertido\n");
  process.exit(1);
}

let json = fs.readFileSync(`${process.argv[2]}`);
let converted = JSON.parse(json);
capacity = converted.vehicle_capacity;
let originPoint = {
  lng: converted.origin.lng,
  lat: converted.origin.lat,
};
points.push(originPoint);
demand.push(0);

for (var i = 0; i < converted.deliveries.length; i++) {
  points.push(converted.deliveries[i].point);
  demand.push(converted.deliveries[i].size);
}

var logger = fs.createWriteStream(`${process.argv[3]}.txt`);
const R = 6371;

let originalFileName = process.argv[2].split("/");
originalFileName = originalFileName[originalFileName.length - 1].split(".");

logger.write(`NAME : ${originalFileName[0]} \n`);
logger.write(`COMMENT : \n`);
logger.write(`TYPE : 	CVRP \n`);
logger.write(`DIMENSION: ${converted.deliveries.length + 1} \n`);
logger.write(`EDGE_WEIGHT_TYPE : 	EUC_2D \n`);
logger.write(`CAPACITY : 	${capacity}\n`);
logger.write(`NODE_COORD_SECTION\n`);
for (var i = 0; i < points.length; i++) {
  logger.write(`${i + 1} ${points[i].lng} ${points[i].lat}\n`);
}
logger.write(`DEMAND_SECTION\n`);
for (var i = 0; i < demand.length; i++) {
  logger.write(`${i + 1}   ${demand[i]}\n`);
}
logger.write(`DEPOT_SECTION\n`);
logger.write(`${converted.origin.lng}\n`);
logger.write(`${converted.origin.lat}\n`);
logger.write(`EOF`);
