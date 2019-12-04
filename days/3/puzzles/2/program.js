const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

const wires = [];

rl.on('line', line => {
  if (line) {
    wires.push(line.split(','));
  }
});

rl.on('close', () => {
  console.log(findClosestIntersection(wires));
});

function findClosestIntersection(wires) {
  let currentPosition = [0,0];
  let steps = 0;
  const intersections = [];
  const grid = {};

  for (let i = 0; i < wires.length; i++) {
    currentPosition = [0,0];
    steps = 0;
    const wire = wires[i];

    for (let k = 0; k < wire.length; k++) {
      const instruction = wire[k];
      [currentPosition, steps] = followWire(currentPosition, steps, instruction, i, grid, intersections);
    }
  }

  let lowestSignalDelay = 0;

  for (let k = 0; k < intersections.length; k++) {
    const signalDelay = getCombinedSteps(intersections[k]);

    if (!lowestSignalDelay || signalDelay < lowestSignalDelay) {
      lowestSignalDelay = signalDelay;
    }
  }

  return lowestSignalDelay;
}

function followWire(startingPosition, steps, instruction, wire, grid, intersections) {
  const direction = instruction.slice(0, 1);
  const distance = parseInt(instruction.slice(1), 10);

  const x = startingPosition[0];
  const y = startingPosition[1];

  let currentPosition = [x, y];

  for (let i = 1; i <= distance; i++) {
    if (direction === 'U') {
      currentPosition = [x, y + i];
    } else if (direction === 'D') {
      currentPosition = [x, y - i];
    } else if (direction === 'R') {
      currentPosition = [x + i, y];
    } else if (direction === 'L') {
      currentPosition = [x - i, y];
    }

    steps += 1;

    addPositionToGrid(currentPosition, wire, steps, grid);

    const intersection = findIntersection(currentPosition, wire, grid);

    if (intersection) {
      intersections.push(intersection);
    }
  }

  return [currentPosition, steps];
}

function addPositionToGrid(position, wire, steps, grid) {
  const key = `${position[0]},${position[1]}`;

  grid[key] = grid[key] || {};
  grid[key][wire] = grid[key][wire] || steps;
}

function findIntersection(position, wire, grid) {
  const key = `${position[0]},${position[1]}`;
  const wiresAtPosition = Object.keys(grid[key]);

  for (let i = 0; i < wiresAtPosition.length; i++) {
    if (parseInt(wiresAtPosition[i], 10) !== wire) {
      return grid[key];
    }
  }

  return null;
}

function getCombinedSteps(intersection) {
  return Object.values(intersection).reduce((sum, steps) => sum + steps);
}
