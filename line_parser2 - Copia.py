import re

predicates_chars_one = ['𝐴', '𝐵', '𝐶', '𝐷', '𝐸', '𝐹', '𝐺', '𝐻', '𝐼', '𝐽', '𝐾', '𝐿', '𝑀', '𝑁', '𝑂', '𝑃', '𝑄', '𝑅', '𝑆', '𝑇', '𝑈', '𝑉', '𝑊', '𝑋', '𝑌', '𝑍']
predicates_chars_two = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
latex = [fr"\wedge", fr"\vee", fr"\neg ", fr"\rightarrow", fr"\leftrightarrow", fr"\forall ", fr"\exists ", fr"\equiv "]
math = ["∧", "∨", "¬", "→", "↔", "∀", "∃", "≡"]
quantifiers = ["∀", "∃"]

# TODO:
# URGENT
# RECURSIVE!!!
# IT WILL TRY TO RESOLVE() EVERY TIME IT ENCOUNTERS AN []
# SO BASICALLY
# FOUND A "[", FIND TRY TO FIND THE OPERATOR.
# FOUND AN OPERATOR, TRY TO RESOLVE() EVERYTHING INSIDE.
# REPEAT IT UNTIL THE LAST ONE RETURNS SOMETHING.
# CONTINUE THE TRAIL!!!
# This will ensure everything is resolved in order.
# resolve should have many forms.
# Resolve will probably have resolve_imps_n_bimps,
# resolve_demorgan and resolve_distribution.


# (𝑃 ∧ 𝑄 <-> (𝑅 → (𝑃 → ¬𝑄))
line = fr"\forall (xyz) \exists x (P(x) \wedge Q( x,y, z) \leftrightarrow (R \rightarrow (P \rightarrow \neg Q)))"

def ensure_predicates_spaces(): pass
def subdivide(): pass
def replace_lates(): pass
def get_quantifiers(line): pass
def get_imps_n_bimps(): pass


def find_directionally(line, index, direction=1):

    resultant_string = ""
    open_counter : int = 0
    close_counter : int = 0
    char_counter: int  = 0
    start_writing : bool = False
    open_symbol = r'\)' if direction < 0 else r'\('
    close_symbol = r'\(' if direction < 0 else r'\)'

    #PROBLEMATIC LINE, IN SOME CASES IT DON'T RETURN
    # THE LAST CHHARACTER, IN SOME CASES IT DO?
    # 
    stop_at : int = 0 if direction < 0 else (len(line)-1)

    for char in range(index, stop_at, direction):
        c = line[char]
        # print(c, open_counter)
        if (bool(re.search(open_symbol, c)) or bool(re.search(r'\*', c)) 
            and not start_writing):
            
            if(bool(re.search(r'\*', c))): 
                close_symbol = r'\*'
                open_symbol = r'\*'

            open_counter += 1
            start_writing = True
            # print("1 if", c, open_counter)
            resultant_string += c
            continue
        
        if not start_writing: continue
        if bool(re.search(open_symbol, c)): open_counter += 1
        if bool(re.search(close_symbol, c)): close_counter += 1
        print(direction, open_counter, close_counter)
        
        resultant_string += c
        char_counter = char
        if close_counter == open_counter and open_counter != 0:
            # print("HELLO???", line[char-1], line[char], line[char+1], line[char] == '¬')
            print("aaaaaaa", line[char-1])
            if(direction < 0 and char-1 >= 0 and line[char-1] == '¬'):
                resultant_string += '¬'
            break    
    
        
    if direction < 0: resultant_string = resultant_string[::-1]

    return [resultant_string, char_counter]

def pop_parentheses(fragment):
    #pops the first (
    fragment = re.sub(r'\(', '', fragment, count=1)
    #pops the last )
    fragment = re.sub(r'\)(?=[^)]*$)', '', fragment, count=1)
    return fragment

def resolve_imps(line, index):

    resultant_string = ""
    A = []
    B = []
    for i in range(len(line)):
        
        if line[i] == "→":
            # resultant_string += ">found<"
            A = find_directionally(line, i, -1)
            A = resolve_imps(A[0], A[1])
            # A = pop_parentheses(A)
            # print(A)
            B = find_directionally(line, i, 1)
            B = resolve_imps(B[0], B[1])
            # B = pop_parentheses(B)
            # resultant_string = resolve_implication_n_demorgan(A, B)
            # print(resolve_implication_n_demorgan(A, B))
            return resolve_implication_n_demorgan(A, B)


        resultant_string += line[i] 
    # print(line, "\n", original_string_copy, "\n", _quantifiers, "\n", expression)
    return resultant_string

def resolve_bimps(line, index):

    resultant_string = ""
    A = []
    B = []
    for i in range(len(line)):
        
        if line[i] == "↔":
            resultant_string += ">found<"
            A = find_directionally(line, i, -1)
            print(A[0])
            A = resolve_imps(A[0], A[1])
            A = resolve_bimps(A, 0)
            # print(A)
            B = find_directionally(line, i, 1)
            print(B[0])
            B = resolve_imps(B[0], B[1])
            B = resolve_bimps(B, 0)
            # resultant_string = resolve_implication_n_demorgan(A, B)
            # print(resolve_implication_n_demorgan(A, B))
            print(A, B)
            # return resolve_implication_n_demorgan(A, B) + " ∨ " + resolve_implication_n_demorgan(B, A)


        resultant_string += line[i] 
    # print(line, "\n", original_string_copy, "\n", _quantifiers, "\n", expression)
    return resultant_string


def _switch_operator(fragment):
    operator = bool(re.search(r'∨', fragment))
    if(operator): return re.sub(r'∨', r'∧', fragment)
    else: return re.sub(r'∧', r'∨', fragment)


def negate_every_member(fragment):
    # TODO:
    # Also find every composed predicate - DONE 
    fragment = re.sub(r'([A-Z])\(([^)]*)\)', r'¬\1(\2)', fragment)
    fragment = re.sub(r'(?<![A-Z])\b([A-Z])\b(?! *\()', r'¬\1', fragment)
    return fragment

def de_negate_every_member(fragment):

    trimmed = fragment
    trimmed = trimmed.replace(" ", "")
    fragment = fragment

    if(trimmed.startswith("¬(")):

        # Removing any double negation
        fragment = re.sub(r'(¬{2,})', '', fragment)
        # print(fragment)

        # marking down every negated
        fragment = re.sub(r'¬\*(.*?)\*', r'¬&\1&', fragment)
        # print(fragment)

        # negating every positive (non-marked)
        fragment = re.sub(r'\*(.*?)\*', r'*¬\1*', fragment)
        # print(fragment)

        # de_negating every negated (marked down)
        fragment = re.sub(r'¬&([^&]*)&', r'*\1*', fragment)
        # print(fragment)


        # > ¬(P ^ ¬Q ^ ¬¬P) negate every double negated, 
        fragment = re.sub(r'¬¬\*(.*?)\*', r'¬*\1*', fragment)
        # because
        # every double negated, if there's any, is actually a triple
        # negated, so in this case ¬¬P = P, ¬( is negating it again,
        # therefore, P = ¬P

        # ugly: removing by brute-force the first negation
        fragment = re.sub(r'¬\(', r'(', fragment)

        fragment = re.sub(r'(¬{2,})', '', fragment)

        fragment = pop_parentheses(fragment)
        # print(fragment)
        return fragment

    else:
        fragment = re.sub(r'(¬{2,})', '', fragment)
        return fragment
    # find every ¬¬ and replace with nothing.
    # find every ¬(¬ ... ¬ ... ¬) and
    # replace with nothing (the hard one :p)
    # basically, if fragment startsWith('¬')
    # remove every '¬' (not that hard), but not
    # pairs of '¬'

    # WARNING!!!!!!!!!!!:
    # actually:
    # if starts with '¬('
    # every '¬' replace with nothing 
    # every '¬¬' replace for '¬'
    return fragment

def replyce(string, look_for, change_to):
    return string.replace(look_for, change_to)

def replyce_all_symmetrical(line, look_for, change_to):
    for case in range(len(look_for)):
        line = replyce(line, look_for=look_for[case], change_to=change_to[case])
    return line

def highlight(line):
    # find composed predicates
    # line = re.sub(r'([A-Z])\(([a-z]*)\)', r'*\1(\2)*', line) 
    line = re.sub(r'([A-Z])\(([^)]*)\)', r'*\1(\2)*', line)

    # find solo predicates
    line = re.sub(r'(?<![A-Z])\b([A-Z])\b(?! *\()', r'*\1*', line)

    # find composed quantifiers
    line = re.sub(r'([∀∃])\(([a-z]*)\)', r'@\1(\2)@', line)

    # find solo quantifiers
    line = re.sub(r'([∀∃][a-z]+)', r'@\1@', line)

    return line

def demorgan(fragment):
    fragment = de_negate_every_member(fragment)
    _fragment = ""
    for char in fragment:
        _char = _switch_operator(char)
        _fragment += _char
    return _fragment

def skolemization(quantifiers):
    # Temos dois niveis (N) em universais, isso significa
    # que toda f() terá 2 variáveis: f(N) (x e z nesse caso)

    # Temos dois níveis(k) de existenciais (n).
    # isso significa que o mais a esquerda recebe
    # os demais à direita.

    # No caso de um:
    # f(x, z)
    # 
    # No caso de dois:
    # g(x, z, f(x, z))
    # 
    # No caso de três:
    # h(x, z, g(x, z, f(x, z)))

    # Então, se tivermos y e w.
    # w é o mais à direita, então ele é:
    # f(x, z)
    # 
    # então qualquer w na fórmula será substituído por f(x,z)
    # 
    # y é o mais a esquerda, então ele tem 2 níveis de nesting.
    # 
    # logo: g(x, z, f(x, z))
    # 
    # Então, qualquer y na fórmula será substituído por ele.

    # TODO:
    # Achar o exemplo mais extremo possível de quantificadores.

    # Separá-los em ordem nas arrays. Para existenciais é
    # melhor fazer na ordem oposta, pois pode-se multiplicar
    # o nível de nesting num for-loop pelo index da variável.
    # Ex: Ey é o mais à esquerda, se invertermos, seu index é 1, não zero.
    # logo, se o _skolemize(n) onde n for (index + 1), podemos colocar num
    # loop para cada membro da array. Depois desinverte para aplicar na fórmula
    # em si.

    # Extrair variáveis de cada um

    As = ["Ax", "Az"]
    Es = ["Ey", "Ew"]
    Xs = ["x", "z"]
    output = [] # Array de strings de skolemizações, na ordem correta dos existenciais.

    Para_W_naFormula = _skolemize(1, ", ".join(Xs))
    print(Para_W_naFormula)
    Para_Y_naFormula = _skolemize(2, ", ".join(Xs))
    print(Para_Y_naFormula)

    return output

def _skolemize(nesting, input, output=""):
    if(nesting == 0):
        print(f"f({output})")
        return f"f({output})"
    if(output == ""):
        output = f"{input}"
    else:
        output = f"{input}, f({output})"
    nesting-=1
    _skolemize(nesting, input, output)


def resolve_implication_n_demorgan(A, B):
    return demorgan(f"¬({A})") + f" ∨ {B}"








# ++++++++++++++++++++++++++++++++++++++++

def splits(line):
    arroba = []

    for x in range(len(line)): 
        if line[x] == "@":
            arroba.append(x)

    cut = arroba[-1]
    _quantifiers = line[:cut + 1]
    expression = line[cut + 1:]

    # print(_quantifiers, "\n", expression)
    return _quantifiers, expression


def subdivide(line):

    original_string_copy = ''
    _quantifiers, expression = splits(line)

    for i in range(len(expression)):
        original_string_copy += expression[i] 
        if expression[i] == "→":
            print("osihdskhsd")

        

    # print(line, "\n", original_string_copy, "\n", _quantifiers, "\n", expression)
    return line

# ++++++++++++++++++++++++++++++++++++++++


# ESSE CARA EH O PIKA
def _process_(line):

    line = replyce_all_symmetrical(line, latex, math)
    line = highlight(line)
    # line = subdivide(line)
    
    return line


# skolemization([])

# string = "i am a text M( x, y, z)"
# string_after_regex = re.sub(r'([A-Z])\(([^)]*)\)', r'*\1(\2)*', string)
# print(string_after_regex)

# Example for ¬(𝑋 ∨ 𝑌(k) ) =>  (¬𝑋 ∧ ¬𝑌(k) )
# supposing the input was ¬(P ∨ Q(k))
# print(_switch_operator(negate_every_member("(*P* ∨ *Q(k)*)")))

# Now, what if it was ¬(¬𝑋 ∧ ¬𝑌(k)) ? 
# print(de_negate_every_member("¬(*¬P* ∨ *¬Q(k)*)"))

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# print(_process_(line))
# @∀(xyz)@ @∃x@ (*P(x)* ∧ *Q( x,y, z)* ↔ (*R* → (*P* → ¬*Q*)))


# string = "i am a text &¬*wow*& ¬yey "
# string_after_regex = re.sub(r'&(.+)&', r'\1', string)
# print(string_after_regex)

# distribute(string)

# print(_switch_operator(de_negate_every_member("¬((*X* ∨ ¬*Y*) ∧ (¬*X* ∨ *Y*))")))
# array = [¬(*X* ∨ ¬*Y*), ^, ¬(¬*X* ∨ *Y*)]
# print()

# TODO:
#  demorgs - FEYTO
#  resolve_imps - FEYTO
#  resolve_bimps - PENDING
#  distribas - COMYCO --
#  SPLIT - DONE
#  skolem - COMYCO - OPTIONAL (talves)
#  a, b - FEYTO
#  montage


# line = "¬((*X* ∨ ¬*Y*) ∧ (¬*X* ∨ *Y*))"
# line = distribute(line) # "(¬*X* ^ *Y*) v (*X* ^ ¬*Y*)"
# line = de_negate_every_member(line) # (*X* ^ ¬*Y*) v (¬*X* ^ *Y*)
# line = _switch_operator(line) # (*X* v ¬*Y*) ^ (¬*X* v *Y*)


# ~((X v ~Y) ^ (~X v Y))
# ¬((*X* v ¬*Y*) ^ (¬*X* v *Y*))
# (P ^ ¬Q ^ R(x))

line = "¬(*X* ∨ *Y*) ↔ (¬*X* ∨ (*Y* → *U*)) ↔ (*A* ∨ *B*)"
A = resolve_bimps(line, 0)
# A = resolve_implication_n_demorgan("*¬Y*", "(¬*X* ∨ *Y*)")
# A = find_directionally(line, 13, -1)
# B = find_directionally(line, 13, 1)
print(A)
