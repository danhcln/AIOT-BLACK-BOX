with open('generate_final_sch.py', 'r', encoding='utf-8') as f:
    final_py = f.read()

with open('generate_a4_sch.py', 'r', encoding='utf-8') as f:
    a4_py = f.read()

# Let's check how lib_symbols was assembled in final_py
idx1 = final_py.find('all_lib_symbols')
idx2 = final_py.find('print(', idx1)
print("final_py all_lib_symbols:")
print(final_py[idx1:idx2])

idx1_a4 = a4_py.find('all_lib_symbols')
idx2_a4 = a4_py.find('print(', idx1_a4)
print("a4_py all_lib_symbols:")
print(a4_py[idx1_a4:idx2_a4])
