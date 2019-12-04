let input = '';
const TARGET_OUTPUT = '19690720';

process.stdin.on('data', chunk => input += chunk);

process.stdin.on('end', () => {
  const memory = input.trim().split(',');
  console.log(findInputs(memory));
});

function findInputs(memory) {
  for (let noun = 0; noun < 100; noun++) {
    for (let verb = 0; verb < 100; verb++) {
      const output = runProgram(memory, noun + '', verb + '');

      if (output === TARGET_OUTPUT) {
        return (100 * noun + verb) + '';
      }
    }
  }

  throw new Error('Inputs not found.');
}

function runProgram(memory, noun, verb) {
  const program = memory.slice(0);
  program[1] = noun;
  program[2] = verb;

  for (let i = 0; i < program.length; i += 4) {
    const opCode = parseInt(program[i], 10);
    const input1Position = parseInt(program[i + 1], 10);
    const input2Position = parseInt(program[i + 2], 10);
    const resultPosition = parseInt(program[i + 3], 10);
    const input1 = parseInt(program[input1Position], 10);
    const input2 = parseInt(program[input2Position], 10);

    let result;

    if (opCode === 1) {
      result = input1 + input2;
    } else if (opCode === 2) {
      result = input1 * input2;
    } else if (opCode === 99) {
      return program[0];
    } else {
      throw new Error(`Unrecognized Op Code: ${opCode} at position: ${i}`);
    }

    if (!isNaN(resultPosition) && !isNaN(result)) {
      program[resultPosition] = result + '';
    } else {
      throw new Error(`Invalid inputs for Op Code at position ${i}.`);
    }
  }

  throw new Error('End of input reached with no halting instruction.');
}
