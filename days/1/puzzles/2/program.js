const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

let totalFuelRequired = 0;

rl.on('line', line => {
  if (line) {
    const mass = parseInt(line, 10);

    totalFuelRequired += getFuelRequiredForModuleMass(mass);
  }
});

rl.on('close', () => {
  console.log(totalFuelRequired);
});

function getFuelRequiredForModuleMass(mass) {
  const fuelRequired = Math.floor(mass / 3) - 2;

  if (fuelRequired <= 0) {
    return 0;
  } else {
    return fuelRequired + getFuelRequiredForModuleMass(fuelRequired);
  }
}
