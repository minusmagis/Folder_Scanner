

Test_List = ['aa1','bbb1','cccc1','aa2','bbb2','cccc2','aa3','bbb3','cccc3']
hash_by_file_size = {}

for index,filename in enumerate(Test_List):

    current_file_size = len(filename)
    #print(current_file_size)

    duplicate = hash_by_file_size.get(current_file_size)
    # print(duplicate)

    if duplicate is not None:
        hash_by_file_size[current_file_size].append(filename)
    else:
        hash_by_file_size[current_file_size] = []
        hash_by_file_size[current_file_size].append(filename)

print(hash_by_file_size)

