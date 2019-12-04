let input = '';

process.stdin.on('data', chunk => input += chunk);

process.stdin.on('end', () => {
  const program = input.trim().split(',');
  console.log(recoverFrom1202Alarm(program));
});

function recoverFrom1202Alarm(program) {
  program[1] = '12';
  program[2] = '2';

  return runProgram(program);
}

function runProgram(program) {
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
