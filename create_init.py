json_file = open('src/test_data/fixtures/initial_data.json', 'w')
json_file.write('[\n')
privat_key = 1
with open('names.txt', 'r') as input_file:
    current_names = input_file.readlines()
input_file.close()
current_names = [x.strip('\n') for x in current_names]
for name in current_names:
    output_data = " {\"pk\": %s,\n  \"model\": \"test_data.initialnames\",\n  \"fields\": {\n    \"first_name\": \"%s\",\n    \"last_name\": \"%s\"\n      }\n },\n" % (privat_key, name.split(" ")[0], name.split(" ")[1])
    json_file.write(output_data)
    privat_key = privat_key + 1
json_file.write(']')
json_file.close()
