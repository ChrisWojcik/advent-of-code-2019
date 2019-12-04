const MIN = 136760;
const MAX = 595730;

let numValidPasswords = 0;

for (let i = MIN; i <= MAX; i++) {
  const password = i;

  if (isValidPassword(password)) {
    numValidPasswords += 1;
  }
}

console.log(numValidPasswords);

function isValidPassword(password) {
  let hasDouble = false;
  let neverDecreasing = true;
  const digits = getDigits(password);

  for (let i = 0; i < digits.length; i++) {
    if (typeof digits[i+1] !== 'undefined' && digits[i+1] === digits[i]) {
      hasDouble = true;
    }

    if (typeof digits[i+1] !== 'undefined' && digits[i+1] < digits[i]) {
      neverDecreasing = false;
    }
  }

  return hasDouble && neverDecreasing;
}

function getDigits(number) {
  return (number+'').split('').map(digit => parseInt(digit, 10));
}
