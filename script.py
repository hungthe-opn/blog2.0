with open('requirements.txt') as file:
    ls = list()
    for i in file:
        ls.append(i)
print(ls)
ls2 = list()
for i in ls:
    idx = i.find('=')
    # end_line = i.find('\n')
    ls2.append(i[:idx])
with open('requirements2.txt', 'w') as file:
    for i in ls2:
        file.writelines(i)
        file.writelines('\n')
print(ls2)
