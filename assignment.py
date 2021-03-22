import random
import datetime

# (1) Generate Random Number


def gen_random_int(*, start: int, end: int) -> int:
    return random.randint(start, end)


start = int(input('What is the start number? '))
end = int(input('What is the end number? '))

result = gen_random_int(start=start, end=end)
print('..--..' * 10)
print('Result is: {:^ }'.format(result))
print('..--..' * 10)

# (2) Use the datetime library together with the random number to generate a random, unique value.


def gen_random_unique_num(*, start: int, end: int) -> int:
    return datetime.datetime.now().microsecond * gen_random_int(start=start, end=end)

result_unqiue = gen_random_unique_num(start=start, end=end)
print('..--..' * 10)
print('Result is: {:^ }'.format(result_unqiue))
print('..--..' * 10)
