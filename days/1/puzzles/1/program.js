const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

let fuelRequired = 0;

rl.on('line', line => {
  if (line) {
    const mass = parseInt(line, 10);
    fuelRequired += Math.floor(mass / 3) - 2;
  }
});

rl.on('close', () => {
  console.log(fuelRequired);
});
