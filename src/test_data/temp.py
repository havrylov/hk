with open('expenses.txt', 'r') as input_file:
    current_names = input_file.readlines()
input_file.close()
current_names = [x.strip('\n') for x in current_names]
print current_names