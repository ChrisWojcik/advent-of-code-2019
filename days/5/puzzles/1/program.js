const POSITION_MODE = 0;
const IMMEDIATE_MODE = 1;
const DEFAULT_MODE = 0;
const ADDITION_OP = 1;
const MULTIPLY_OP = 2;
const INPUT_OP = 3;
const OUTPUT_OP = 4;
const HALT_OP = 99;

let input = '';

process.stdin.on('data', chunk => input += chunk);

process.stdin.on('end', () => {
  const memory = input.trim().split(',');
  runProgram(memory, '1');
});

function runProgram(memory, ...inputs) {
  let i = 0;

  while (i < memory.length) {
    const instruction = memory[i];
    const opCode = Number(instruction.slice(-2));
    const paramModes = instruction.slice(0, -2).split('').reverse().join('');
    const param1Mode = Number(paramModes[0]) || DEFAULT_MODE;
    const param2Mode = Number(paramModes[1]) || DEFAULT_MODE;

    if (opCode === ADDITION_OP) {
      const param1 = getParameter(param1Mode, i + 1, memory);
      const param2 = getParameter(param2Mode, i + 2, memory);

      memory[Number(memory[i + 3])] = (param1 + param2) + '';

      i += 4;
    } else if (opCode === MULTIPLY_OP) {
      const param1 = getParameter(param1Mode, i + 1, memory);
      const param2 = getParameter(param2Mode, i + 2, memory);

      memory[Number(memory[i + 3])] = (param1 * param2) + '';

      i += 4;
    } else if (opCode === INPUT_OP) {
      const input = inputs.shift();
      const param1 = Number(memory[i + 1]);

      memory[param1] = input;

      i += 2;
    } else if (opCode === OUTPUT_OP) {
      const param1 = getParameter(param1Mode, i + 1, memory);

      console.log(param1 + '');

      i += 2;
    } else if (opCode === HALT_OP) {
      return;
    }
  }
}

function getParameter(mode, pointer, memory) {
  if (mode === POSITION_MODE) {
    const position = Number(memory[pointer]);
    return Number(memory[position]);
  } else if (mode === IMMEDIATE_MODE) {
    return Number(memory[pointer]);
  }
}
