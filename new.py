import re
import keyword as kw

keywords = kw.kwlist
operators ={'+':'PLUS' ,'-':'MINUS','*':'STAR','**':'DOUBLESTAR','/':'SLASH','//':'DOUBLESLASH','%':'PERCENT','<<':'LEFTSHIFT','>>':'RIGHTSHIFT','&':'AMPER','|':'VBAR','^':'CIRCUMFLEX','~':'TILDE','<':'LESS','>':'GREATER','<=':'LESSEQUAL','>=':'GREATEREQUAL','==':'EQEQUAL','!=':'NOTEQUAL','<>':'NOTEQUAL'}
delimiters = {'(':'LPAR', ')':'RPAR', '[':'LSQB', ']':'RSQB', '{':'LBRACE', '}':'RBRACE', ',':'COMMA', ':':'COLON', '.':'DOT', '`':'BACKQUOTE', '=':'EQUAL', ';':'SEMI', '+=':'PLUSEQUAL', '-=':'MINEQUAL', '*=':'STAREQUAL', '/=':'SLASHEQUAL', '%=':'PERCENTEQUAL', '**=':'DOUBLESTAREQUAL', '&=':'AMPEREQUAL', '|=':'VBAREQUAL', '^=':'CIRCUMFLEXEQUAL', '>>=':'LEFTSHIFTEQUAL','<<=':'RIGHTSHIFTEQUAL'}

val = []
val_type = []

txt = open('test2.txt', 'r')
txt_read = txt.read()

txt_list = re.split(r'(\n)', txt_read)

def resplit(txt):
    obj = re.split(r'([^a-zA-Z_\"\'\#\!])', txt)

    if obj is not None:
        return obj

def checkNAME(txt):
    if re.findall(r'[a-zA-Z_\!]+', txt):
        return True

def checkStr(txt):
    if re.findall(r'^\'', txt):
        if re.findall(r'\'$', txt):
            return 'full'
        return 'wait end'
    
    elif re.findall(r'^\"', txt):
        if re.findall(r'\"$', txt):
            return 'full'
        return 'wait end'

    elif re.findall(r'\'$', txt):
        return 'complete'

    elif re.findall(r'\"$', txt):
        return 'complete'

    else:
        return 'continue'

def checkComment(txt):
    if re.findall(r'#', txt):
        return 'hashtag'

    elif re.findall(r'^(\'{3})', txt):
        if re.findall(r'(\'{3})$', txt):
            return 'full'
        return 'wait end'

    elif re.findall(r'^(\"{3})', txt):
        if re.findall(r'(\"{3})$', txt):
            return 'full'
        return 'wait end'

    elif re.findall(r'(\'{3})$', txt):
        return 'complete'

    elif re.findall(r'(\"{3})$', txt):
        return 'complete'
    
    else:
        return 'continue'

def checkOpDlim(txt):
    if re.findall(r'[^a-zA-Z0-9_!\"\'\n#]', txt):
        return True

def extraOpDlim(txt):
    if re.findall(r'[=<>*/]', txt):
        return True

def checkNum(txt):
    if re.findall(r'[0-9]+', txt):
        return True

#preprocessing
all_tok = []
for item in txt_list:
    tok_lst = item.split(' ')

    for i in range(len(tok_lst)):
        ckd = resplit(tok_lst[i])
        
        if ckd.count('') > 0:
            ckd = list(filter(lambda usl: usl != '', ckd)) #clear empty string
            tok_lst[i] = ckd
    
    #clear empty list
    tok_lst = list(filter(lambda use: len(use) != 0, tok_lst))

    flat_tok_lst = []
    #flatten the list
    for sublist in tok_lst:
        if isinstance(sublist, list):
            for i in sublist:
                flat_tok_lst.append(i)
        else:
            flat_tok_lst.append(sublist)
    
    all_tok.append(flat_tok_lst)

#flatten again
flat_all_tok = []
for subitem in all_tok:
    for item in subitem:
        flat_all_tok.append(item)

#classify token
temp = []
temp2 = []
i = 0
while i < len(flat_all_tok):
    #-------assemble comment--------
    if checkComment(flat_all_tok[i]) == 'hashtag' or checkComment(flat_all_tok[i]) == 'full':
        val.append(flat_all_tok[i])
        val_type.append('COMMENT')

    elif checkComment(flat_all_tok[i]) == 'wait end':
        while checkComment(flat_all_tok[i]) != 'complete':
            temp.append(flat_all_tok[i])
            temp2.append(flat_all_tok[i])
            i+=1
        
        temp.append(flat_all_tok[i])
        cmnt = ' '.join(temp)
        val.append(cmnt)
        val_type.append('COMMENT')
        temp.clear()
    #------------------------------

    #----------assemble string-----------------
    if checkNAME(flat_all_tok[i]):
        if checkStr(flat_all_tok[i]) == 'full':
            val.append(flat_all_tok[i])
            val_type.append('STRING')

        elif checkStr(flat_all_tok[i]) == 'wait end':
            while checkStr(flat_all_tok[i]) != 'complete':
                temp.append(flat_all_tok[i])
                temp2.append(flat_all_tok[i])
                i+=1
            
            temp.append(flat_all_tok[i])
            string = ' '.join(temp)
            val.append(string)
            val_type.append('STRING')
            temp.clear()
            
        elif checkStr(flat_all_tok[i]) == 'continue' and temp2.count(flat_all_tok[i]) < 1:
            val.append(flat_all_tok[i])
            val_type.append('NAME')
    #------------------------------------------
    
    #--------catch newline--------
    if re.findall('\n', flat_all_tok[i]):
        val.append(flat_all_tok[i])
        val_type.append('NEWLINE')
        flat_all_tok.remove(flat_all_tok[i])
    #-----------------------------

    #----------catch number---------
    if checkNum(flat_all_tok[i]):
        val.append(flat_all_tok[i])
        val_type.append('NUMBER')
    #-------------------------------

    #-----classify operators, delimiter-----
    if checkOpDlim(flat_all_tok[i]):
        temp.append(flat_all_tok[i])

        i+=1
        while i<len(flat_all_tok) and extraOpDlim(flat_all_tok[i]):
            temp.append(flat_all_tok[i])
            i+=1

        i-=1
        opDlim = ''.join(temp)
        temp.clear()
        val.append(opDlim)
        if opDlim in operators:
            val_type.append(operators[opDlim])
        elif opDlim in delimiters:
            val_type.append(delimiters[opDlim])
    #---------------------------------------
    
    i+=1

val = list(filter(lambda use: len(use) != 0, val))
print(val)
print(val_type)