

import re
# second try at this with iteration
data_file = 'data_file.txt'
num_items = 0 #counter
# check if file exists
try:
    #with open(data_file) as file_object:
        #print('file is there')
    i = 0
    q_list = []
    #line = []
    f = open(data_file, "r")
    print('got the file')    
    while True:
        line = f.readline()
        if not line:
            break
        # now make it into a list object to add
        addme = [line]
        q_list.append(addme)
        i = i + 1
        num_items = i
except:
    print('make a new file')
    q_list = [["first qestion", "correct answer 1", "wrong 1", "wrong 1a"], 
    ["second question", "correct answer 2", "wrong 2", "wrong 2a"], 
    ["third question", "correct answer 3", "wrong 3", "wrong 3a"],
    ["fourth question", "correct answer 4", "wrong 4", "wrong 4a"]
    ]    
    for quest  in range(0, len(q_list)):
        # save the file line by line
        with open(data_file, 'a') as outfile:
            #outfile.write('\n' + str(q_list[quest]))
            outfile.write(str(q_list[quest]) + '\n')
# 
temp1 =  str(q_list[2])
print('final temp1 ' +temp1)
temp2 = re.sub('\]|\[|\(|\)', '', temp1)
print('final temp2 ' +temp2)
print(' see if we get anything ' + str(q_list[0][0]))
print(str(num_items))
#back to a list
fnllist = str(q_list[0][0]).split()
print(fnllist)