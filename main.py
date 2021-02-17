from DynamicArray import DynamicArray

my_array = DynamicArray('I', (i * (2 * i + 13) for i in range(10)))
print(my_array)
my_array.insert(1, 3)
print(my_array)
