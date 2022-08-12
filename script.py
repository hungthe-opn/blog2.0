with open('requirements.txt') as file:
    ls = list()
    for i in file:
        ls.append(i)
ls2 = list()
for i in ls:
    idx = i.find('=')
    ls2.append(i[:idx])
with open('requirements2.txt', 'w') as file:
    for i in ls2:
        file.writelines(i)
        file.writelines('\n')
