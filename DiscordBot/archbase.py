labels = {}
number = {}


def d2b(n):
    result = ''
    final = ''
    m = abs(int(n))
    n = int(n)
    if n==0:
        return '00000000000000000000000000000000'
    while m>0:
        result+= str(m%2)
        m//=2
    if n<0:
        flag = True
        for c in result:
            if flag==True:
                if c=='1':
                    final+='1'
                    flag = False
                else:
                    final+= '0'
            else:
                if c=='1':
                    final+='0'
                else:
                    final+='1'
    else:
        final = result
    if len(result)<32:
        sign = '0' if n>0 else '1'
        for i in range(len(result),32):
            final+=sign
    #final = final[::-1]
    return final


def d2bu(n):
    result = ''
    final = ''
    m = abs(int(n))
    n = int(n)
    if n==0:
        return '00000000000000000000000000000000'
    while m>0:
        result+= str(m%2)
        m//=2
    if n<0:
        flag = True
        for c in result:
            if flag==True:
                if c=='1':
                    final+='1'
                    flag = False
                else:
                    final+= '0'
            else:
                if c=='1':
                    final+='0'
                else:
                    final+='1'
    else:
        final = result
    if len(result)<32:
        for i in range(len(result),32):
            final+='0'
    #final = final[::-1]
    return final


def b2h(n):
    if(len(n)<32):
        return n
    type = {}
    type['0000'] = '0'
    type['0001'] = '1'
    type['0010'] = '2'
    type['0011'] = '3'
    type['0100'] = '4'
    type['0101'] = '5'
    type['0110'] = '6'
    type['0111'] = '7'
    type['1000'] = '8'
    type['1001'] = '9'
    type['1010'] = 'a'
    type['1011'] = 'b'
    type['1100'] = 'c'
    type['1101'] = 'd'
    type['1110'] = 'e'
    type['1111'] = 'f'
    temp = n.replace('_','')
    result = ''
    for i in range(8):
        result+= type[temp[i*4:(i*4)+4]]
        if i%2==1:
            result+=' '
    return result

def check_r(r):
    r = r.replace('o','0')
    r = r.replace('O','0')
    if len(r)<2:
        return '-1-1'
    if r[0].isnumeric():
        return '-1-1'
    if not r[1:].isnumeric():
        return '-1-1'
    if int(r[1:]) < 0 or int(r[1:]) >= 32:
        return '-1-1'
    r = d2b(r[1:])
    r = r[:5]
    r = r[::-1]
    return r


def check_n(n):
    n = n.replace('o','0')
    n = n.replace('O','0')
    if len(n)<1:
        return '-1-1'
    if n[0]=='-':
        if not n[1:].isnumeric():
            return '-1-1'
        if len(n)<2:
            return '-1-1'
    else:
        if not n.isnumeric():
            return '-1-1'
    return (d2b(n))

def check_n_wrong(n):
    n = n.replace('o','0')
    n = n.replace('O','0')
    if len(n)<1:
        return '-1-1'
    if n[0]=='-':
        if not n[1:].isnumeric():
            return '-1-1'
        if len(n)<2:
            return '-1-1'
    else:
        if not n.isnumeric():
            return '-1-1'
    return (d2b(n))


def check_ls(n):
    if n.find(')')!=len(n)-1:
        return '-1-1'
    if n.find('(') == -1:
        return '-1-1'
    n1 = check_n(n[:n.find('(')])
    if n1 == '-1-1':
        return '-1-1'
    r = check_r(n[n.find('(')+1:n.find(')')])
    if r == '-1-1':
        return '-1-1'
    r = r[0:5][::-1]
    return (r+n1)


def branch(inst,myindex):
    type = {'beq': '000', 'bne': '001', 'blt': '100', 'bge': '101', 'bltu': '110', 'bgeu': '111'}
    result = ''
    if len(inst) != 4:
        return "Invalid format!"
    rs1 = check_r(inst[1])
    if rs1 == '-1-1':
        return "Invalid rd"
    rs2 = check_r(inst[2])
    if rs2 == '-1-1':
        return "Invalid rs1"
    imm = check_n(inst[3])
    if imm == '-1-1':
        if(inst[3] in labels):
            imm = d2b(labels[inst[3]] - myindex)
        else:
            return 'Invalid immediate'
    result += imm[12]+ '_' + imm[5:11][::-1]+ '_' + rs2+ '_' + rs1+ '_' + type[inst[0]]+ '_' + imm[1:5][::-1] + '_' + imm[11] + '_'
    result += '1100011'
    return result


def load(inst):
    type = {'lb': '000', 'lh': '001', 'lw': '010', 'lbu': '100', 'lhu': '101'}
    result = ''
    if len(inst) != 3:
        return "Invalid format!"
    rd = check_r(inst[1])
    if rd == '-1-1':
        return "Invalid rd"
    r_n = check_ls(inst[2])
    if r_n == '-1-1':
        return "Invalid rs1/immediate"
    rs1 = r_n[:5]
    imm = r_n[5:]
    result+= imm[:12][::-1]+ '_' + rs1+ '_' + type[inst[0]]+ '_' + rd+ '_'
    result += '0000011'
    return result


def store(inst):
    type = {'sb': '000', 'sh': '001', 'sw': '010'}
    result = ''
    if len(inst) != 3:
        return "Invalid format!"
    rs2 = check_r(inst[1])
    if rs2 == '-1-1':
        return "Invalid rd"
    r_n = check_ls(inst[2])
    if r_n == '-1-1':
        return "Invalid rs1/immediate"
    rs1 = r_n[:5]
    imm = r_n[5:]
    result += imm[5:12][::-1]+ '_' + rs2+ '_' + rs1+ '_' + type[inst[0]]+ '_' + imm[0:5][::-1]+ '_'
    result += '0100011'
    return result


def I(inst):
    type = {'addi': '000', 'slti': '010', 'sltiu': '011', 'xori': '100', 'ori': '110', 'andi': '111'}
    result = ''
    if len(inst) != 4:
        return "Invalid format!"
    rd = check_r(inst[1])
    if rd == '-1-1':
        return "Invalid rd"
    rs1 = check_r(inst[2])
    if rs1 == '-1-1':
        return "Invalid rs1"
    imm = check_n(inst[3])
    if imm == '-1-1':
        if(check_r(inst[3])!='-1-1'):
            inst[0] = inst[0][0:len(inst[0])-1]
            return R(inst)
        else:
            return "Invalid immediate"
    result += imm[:12][::-1]+ '_' + rs1+ '_' + type[inst[0]]+ '_' + rd+ '_'
    result += '0010011'
    return result


def shifti(inst):
    type = {'slli': '001', 'srli': '101', 'srai': '101'}

    type2 = {'slli': '0000000', 'srli': '0000000', 'srai': '0100000'}
    result = ''
    if len(inst) != 4:
        return "Invalid format!"
    rd = check_r(inst[1])
    if rd == '-1-1':
        return "Invalid rd"
    rs1 = check_r(inst[2])
    if rs1 == '-1-1':
        return "Invalid rs1"
    imm = check_n(inst[3])
    if imm == '-1-1':
        if(check_r(inst[3])!='-1-1'):
            inst[0] = inst[0][0:len(inst[0])-1]
            return R(inst)
        else:
            return "Invalid immediate"
    result += type2[inst[0]]+ '_' + imm[:5][::-1]+ '_' + rs1+ '_' + type[inst[0]]+ '_' + rd+ '_'
    result += '0010011'
    return result


def R(inst):
    type = {}
    type['add'] = type['sub'] = '000'
    type['sll'] = '001'
    type['slt'] = '010'
    type['sltu'] = '011'
    type['xor'] = '100'
    type['srl'] = '101'
    type['sra'] = '101'
    type['or'] = '110'
    type['and'] = '111'
    type2 = {'sub': '0100000', 'sra': '0100000', 'add': '0000000', 'sll': '0000000', 'slt': '0000000', 'sltu': '0000000',
             'xor': '0000000', 'srl': '0000000', 'or': '0000000', 'and': '0000000'}
    result = ''
    if len(inst) != 4:
        return "Invalid format!"
    rd = check_r(inst[1])
    if rd == '-1-1':
        return "Invalid rd"
    rs1 = check_r(inst[2])
    if rs1 == '-1-1':
        return "Invalid rs1"
    rs2 = check_r(inst[3])
    if rs2 == '-1-1':
        if check_n(inst[3])!='-1-1':
            inst[0] = inst[0]+ 'i'
            return I(inst)
        else:
            return "Invalid rs2"
    result += type2[inst[0]]+ '_' + rs2+ '_' + rs1+ '_' + type[inst[0]]+ '_' + rd+ '_'
    result += '0110011'
    return result


def process(inst,myindex):
    inst = inst.lower()
    inst = inst.replace(',', ' ')
    inst = inst.split()
    print(inst)
    result = ''
    if(len(inst)<3):
        return 'Invalid Instruction'
    if inst[0] == 'lui':
        if len(inst) != 3:
            return "Invalid format!"
        rd = check_r(inst[1])
        if rd=='-1-1':
            return "Invalid rd"
        imm = check_n(inst[2])
        if imm=='-1-1':
            return 'Invalid immediate'

        imm = imm[12:]
        imm = imm[::-1]
        result+=imm+ '_'
        result+=rd+ '_'
        result+='0110111'
        return result
    elif inst[0] == 'auipc':
        if len(inst) != 3:
            return "Invalid format!"
        rd = check_r(inst[1])
        if rd=='-1-1':
            return "Invalid rd"
        imm = check_n(inst[2])
        if imm=='-1-1':
            return 'Invalid immediate'
        imm = imm[12:]
        imm = imm[::-1]
        result+=imm+ '_'
        result+=rd+ '_'
        result+='0010111'
        return result
    elif inst[0] == 'jal':
        if len(inst) != 3:
            return "Invalid format!"
        rd = check_r(inst[1])
        if rd == '-1-1':
            return "Invalid rd"
        imm = check_n(inst[2])
        if imm=='-1-1':
            if(inst[2] in labels):
                imm = d2b(labels[inst[2]] - myindex)
            else:
                return 'Invalid immediate'
        result += imm[20]+ '_' + imm[1:11][::-1]+ '_' + imm[11]+ '_' + imm[12:20][::-1]+ '_'
        result += rd+ '_'
        result += '1101111'
        return result
    elif inst[0] == 'jalr':
        if len(inst) != 4:
            return "Invalid format!"
        rd = check_r(inst[1])
        if rd == '-1-1':
            return "Invalid rd"
        rs1 = check_r(inst[2])
        if rs1 == '-1-1':
            return "Invalid rs1"
        imm = check_n(inst[3])
        if imm=='-1-1':
            if(inst[3] in labels):
                imm = d2b(labels[inst[3]] - myindex)
            else:
                return 'Invalid immediate'
        result += imm[:12][::-1]+ '_'
        result += rs1+ '_' + '000'+ '_' + rd+ '_'
        result += '1100111'
        return result
    elif inst[0] == 'beq' or inst[0] == 'bne' or inst[0] == 'blt' or inst[0] == 'bge' or inst[0] == 'bltu' or inst[0] == 'bgeu':
        return branch(inst,myindex)
    elif inst[0] == 'lw' or inst[0] == 'lh' or inst[0] == 'lb' or inst[0] == 'lhu' or inst[0] == 'lbu':
        return load(inst)
    elif inst[0] == 'sw' or inst[0] == 'sh' or inst[0] == 'sb':
        return store(inst)
    elif inst[0] == 'addi' or inst[0] == 'slti' or inst[0] == 'sltiu' or inst[0] == 'xori' or inst[0] == 'ori' or inst[0] == 'andi':
        return I(inst)
    elif inst[0] == 'slli' or inst[0] == 'srli' or inst[0] == 'srai':
        return shifti(inst)
    elif inst[0] == 'add' or inst[0] == 'sub' or inst[0] == 'sll' or inst[0] == 'slt' or inst[0] == 'sltu' or inst[0] == 'xor' or inst[0] == 'srl' or inst[0] == 'sra' or inst[0] == 'or' or inst[0] == 'and':
        return R(inst)
    elif inst[0] == 'ecall':
        return '000000000000_00000_000_00000_1110011'
    elif inst[0] == 'ebreak':
        return '000000000001_00000_000_00000_1110011'
    else:
        return 'Invalid instruction'

def handle(inst,type):
    count2 = inst.count('\n')
    inst = inst.split('\n')
    length = len(inst)
    while '' in inst:
        inst.remove('')

    for i in range(len(inst)):
        if(inst[i].find('//')!=-1):
            inst[i] = inst[i][:inst[i].find('//')]
    count  = 0
    i = 0 
    while i < len(inst):
        if(inst[i].find(':')!=-1):
            if(len(inst[i])==inst[i].find(':')+1):
                number[i+1] = count
                labels[inst[i][:inst[i].find(':')]] = count
                inst[i] = ''
                i+=1
                count+=1
            else:
                number[i] = count
                count+=1
                labels[inst[i][:inst[i].find(':')]] = count
                inst[i] = inst[i][inst[i].find(':')+1:]
        else:
            number[i] = count
            count+=1
        i+=1
    result = ''
    if len(inst)>1:
        for i in range(len(inst)):
            temp = inst[i].split()
            if(len(temp)<3):
                continue
            else:
                if len(inst[i])>3:
                    if(type == 'b'):
                        result += process(inst[i],number[i])
                    elif (type=='h'):
                        result += b2h(process(inst[i],number[i]))
                        print(b2h(process(inst[i],number[i])))
                    if i!=count:
                        result+= '\n'
    else:
        inst2 = ''
        inst2+=inst[0]
        if(type=='b'):
            result = process(inst[0],0)
        elif (type=='h'):
            result = b2h(process(inst[0],0))
    return result 