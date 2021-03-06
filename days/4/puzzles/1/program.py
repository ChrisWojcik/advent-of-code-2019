MIN = 136760
MAX = 595730

def is_valid_password(password):
  has_double = False
  never_decreasing = True
  digits = [int(d) for d in str(password)]

  for n, nth_digit in enumerate(digits):
    if n + 1 < len(digits):
      if digits[n+1] == nth_digit:
        has_double = True

      if digits[n+1] < nth_digit:
        never_decreasing = False

  return (has_double and never_decreasing)

num_valid_passwords = 0

for i in range(MIN, MAX + 1):
  if is_valid_password(i):
    num_valid_passwords += 1

print(num_valid_passwords)
