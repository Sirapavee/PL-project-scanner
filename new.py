import re
import keyword as kw

keywords = kw.kwlist
operators ={'+':'PLUS' ,'-':'MINUS','*':'STAR','**':'DOUBLESTAR','/':'SLASH','//':'DOUBLESLASH','%':'PERCENT','<<':'LEFTSHIFT','>>':'RIGHTSHIFT','&':'AMPER','|':'VBAR','^':'CIRCUMFLEX','~':'TILDE','<':'LESS','>':'GREATER','<=':'LESSEQUAL','>=':'GREATEREQUAL','==':'EQEQUAL','!=':'NOTEQUAL','<>':'NOTEQUAL'}
delimiters = {'(':'LPAR', ')':'RPAR', '[':'LSQB', ']':'RSQB', '{':'LBRACE', '}':'RBRACE', ',':'COMMA', ':':'COLON', '.':'DOT', '`':'BACKQUOTE', '=':'EQUAL', ';':'SEMI', '+=':'PLUSEQUAL', '-=':'MINEQUAL', '*=':'STAREQUAL', '/=':'SLASHEQUAL', '%=':'PERCENTEQUAL', '**=':'DOUBLESTAREQUAL', '&=':'AMPEREQUAL', '|=':'VBAREQUAL', '^=':'CIRCUMFLEXEQUAL', '>>=':'LEFTSHIFTEQUAL','<<=':'RIGHTSHIFTEQUAL'}

txt = open('test2.txt', 'r')
txt_read = txt.read()
#sp = re.findall(r'\S+|\n', tt)

txt_list = re.split(r'(\n)', txt_read)
#print(txt_list)

def resplit(txt):
    obj = re.split(r'([^a-zA-Z0-9_\"\'\#])', txt)

    if obj is not None:
        return obj

def checkKW(txt):
    for item in keywords:
        if item == txt:
            return True

def checkOp(txt):
    obj = re.split(r'([\+\-\*(\*\*)(\/)(\/\/)%(<<)(>>)&|^~<>(<=)(>=)(==)(!=)(<>)])', txt)
    
    if obj is not None:
        return obj
    
def checkDelim(txt):
    #obj = re.split(r'([\(\)\[\]\{\}:.`=;(+=)(-=)(*=)(/=)(%=)(**=)(&=)(|=)(^=)(>>=)(<<=)(,)])', txt)
    
    if obj is not None:
        return obj

def checkNAME(txt):
    f_name = re.findall('[a-zA-z | _]', txt)

    if(len(txt) == len(f_name)):
        return True

#def checkComment(txt):


#MAIN
for item in txt_list:
    tok_lst = item.split(' ')

    #check delimeter
    for i in range(len(tok_lst)):
        ckd = resplit(tok_lst[i])
        
        if ckd.count('') > 0:
            ckd = list(filter(lambda usl: usl != '', ckd)) #clear empty string
            tok_lst[i] = ckd
    
    #clear empty list
    tok_lst = list(filter(lambda use: len(use) != 0, tok_lst))

    sub_tok_lst = []
    #flatten the list
    for sublist in tok_lst:
        if isinstance(sublist, list):
            for i in sublist:
                sub_tok_lst.append(i)
        else:
            sub_tok_lst.append(sublist)
            
    print(sub_tok_lst)
