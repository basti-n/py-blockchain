# (1) Create a Food class with a “name” and a “kind” attribute as well as a “describe()”
# method (which prints “name” and “kind” in a sentence).

class Food:
    def __init__(self, *, name='Food', kind='Kind'):
        self.name = name
        self.kind = kind

    def describe(self):
        """ Print class attributes to the console """
        print(f'The chosen food {self.kind} has a name of: {self.name}')


Food(name='Margherita', kind='Pizza').describe()
Food().describe()

print('\n' + 20 * '--' + '\n')

# (2) Try turning describe()  from an instance method into a class and a static method.
# Change it back to an instance method thereafter.


class FoodClassMethod():
    name = 'Calzone'
    kind = 'Pizza'

    @classmethod
    def describe(cls):
        """ Print class attributes to the console """
        print(f'The chosen food {cls.kind} has a name of: {cls.name}')


FoodClassMethod.describe()
print('\n' + 20 * '--' + '\n')


class FoodStaticMethod():
    @staticmethod
    def describe(*, name='Food', kind='Kind'):
        """ Print class attributes to the console """
        print(f'The chosen food {kind} has a name of: {name}')


FoodStaticMethod.describe(name='Truffle', kind='Pizza')

# (3) Create a  “Meat” and a “Fruit” class – both should inherit from “Food”.
# Add a “cook() ” method to “Meat” and “clean() ” to “Fruit”.


class Meat(Food):
    def __init__(self, *, name: str):
        super().__init__(name=name, kind='Meat')

    def cook(self) -> None:
        print(f'Meat is cooking: {self.kind} | {self.name}')


class Fruit(Food):
    def __init__(self, *, name: str):
        super().__init__(name=name, kind='Fruit')

    def cook(self) -> None:
        print(f'Fruit is is cleaning: {self.kind} | {self.name}')


Meat(name='Sirloin').cook()
Fruit(name='Apple').cook()
print('\n' + 20 * '--' + '\n')

# (4) Overwrite a “dunder” method to be able to print your “Food” class.


class PrintableFood(Food):
    def __repr__(self) -> str:
        return f'Printable Food: \nKind: {self.kind} \nFood: {self.name}'


foodPrintable = PrintableFood(name='Printable', kind='Pizza')
foodPrintable.describe()
print(foodPrintable)

print('\n' + 20 * '--' + '\n')
