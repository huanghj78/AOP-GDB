import gdb

v1=gdb.parse_and_eval("str")
v2=gdb.parse_and_eval("arr")
v3=gdb.parse_and_eval("buf")
print(v1.type)
# print(v1.value)
print(v2.type)
# print(v2.value)
print(v3.type)
# for f in v3.type.fields():
#     print(f.name, f.type)
# print(v3.value)
print(v1.string())
print(v3.string())


