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
  const intersections = [];
  const grid = {};

  for (let i = 0; i < wires.length; i++) {
    currentPosition = [0,0];
    const wire = wires[i];

    for (let k = 0; k < wire.length; k++) {
      const instruction = wire[k];
      currentPosition = followWire(currentPosition, instruction, i, grid, intersections);
    }
  }

  let shortestManhattanDistance = 0;

  for (let k = 0; k < intersections.length; k++) {
    const manhattanDistance = getManhattanDistance(intersections[k]);

    if (!shortestManhattanDistance || manhattanDistance < shortestManhattanDistance) {
      shortestManhattanDistance = manhattanDistance;
    }
  }

  return shortestManhattanDistance;
}

function followWire(startingPosition, instruction, wire, grid, intersections) {
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

    addPositionToGrid(currentPosition, wire, grid);

    if (hasIntersection(currentPosition, wire, grid)) {
      intersections.push(currentPosition);
    }
  }

  return currentPosition;
}

function addPositionToGrid(position, wire, grid) {
  const key = `${position[0]},${position[1]}`;

  grid[key] = grid[key] || [];
  grid[key].push(wire);
}

function hasIntersection(position, wire, grid) {
  const key = `${position[0]},${position[1]}`;

  for (let i = 0; i < grid[key].length; i++) {
    if (grid[key][i] !== wire) {
      return true;
    }
  }

  return false;
}

function getManhattanDistance(coordinate) {
  return Math.abs(coordinate[0]) + Math.abs(coordinate[1]);
}
