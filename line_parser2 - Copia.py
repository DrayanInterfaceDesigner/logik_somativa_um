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

def _concat_in_between(a, operator, b):
    """
    This function concatanates the given sides 
    A and B, with a given operator.

    Returns a string with the sides concataned.
    """
    return f"{a} {operator} {b}"

def enclosure(a):
    return f"({a})"

def splits(line):
    """
    This function splits an given equation into
    two groups. One with quantifiers, and the other 
    with the equation with its quantifiers extracted
    from it.

    Returns an array with two strings: quantifiers and equation.
    """
    # ++++++++++++Removes quantifiers from original string++++++++++++++
    # puts all quantifiers into array
    _quantifiers = re.findall(r'@.*?@', line)

    # removes quantifiers from original string
    output_string = re.sub(r'@.*?@', '', line)

    # ++++++++++++Orders quantifiers in array++++++++++++++
    # transforms array into string
    _quantifiers = " ".join(_quantifiers)

    # puts all \forall quantifiers into array
    _quantifiersA = re.findall(r'@∀.*?@', _quantifiers)

    # removes \forall quantifiers from new quantifiers string
    _quantifiersE = re.sub(r'@∀.*?@', '', _quantifiers)

    # formats quantifiers string
    _quantifiersOut = " ".join(_quantifiersA)
    _quantifiersOut += _quantifiersE

    # removes spaces
    output_string = re.sub(r'\s+', ' ', output_string)
    _quantifiersOut = re.sub(r'\s+', ' ', _quantifiersOut)

    result = [_quantifiersOut, output_string]

    # Print the result
    # print(_quantifiers + output_string)

    return result

def find_directionally(line, index, direction=1):
    """
    Given an equation, a starting index and a 
    direction (-1 is rtl, 1 is ltr, default is ltr),
    finds the A or B side (based on the direction) 
    of the given equation.

    Returns an array containing a string (the side),
    and the index it finished.
    """

    # puts a space at the begning and ending of the line
    line = re.sub(r'^', ' ', line)
    line = re.sub(r'$', ' ', line)

    resultant_string = ""
    open_counter : int = 0
    close_counter : int = 0
    char_counter: int  = 0
    start_writing : bool = False
    open_symbol = r'\)' if direction < 0 else r'\('
    close_symbol = r'\(' if direction < 0 else r'\)'
    is_star : bool = False

    #PROBLEMATIC LINE, IN SOME CASES IT DON'T RETURN
    # THE LAST CHHARACTER, IN SOME CASES IT DO?
    # 
    stop_at : int = 0 if direction < 0 else (len(line))

    for char in range(index, stop_at, direction):
        c = line[char]
        # print(c, open_counter)
        if ((bool(re.search(open_symbol, c)) or bool(re.search(r'\*', c)) )
            and not start_writing):
            
            if(bool(re.search(r'\*', c))): 
                close_symbol = r'\*'
                open_symbol = r'\*'
                is_star = True
                # print('IT WAS!!!',  line[char-2], line[char-1], c, line[char+1], open_symbol, close_symbol)
                # print(start_writing)

            open_counter += 1
            start_writing = True
            # print("1 if", c, open_counter)
            resultant_string += c
            continue
        
        if not start_writing: continue
        if(is_star):
            if bool(re.search(close_symbol, c)): close_counter += 1
        else:
            if bool(re.search(open_symbol, c)): open_counter += 1
            if bool(re.search(close_symbol, c)): close_counter += 1

        # print(direction, open_counter, close_counter, c, open_symbol, close_symbol, bool(re.search(open_symbol, c)))
        
        resultant_string += c
        char_counter = char
        if close_counter == open_counter and open_counter != 0:
            # print("HELLO???", line[char-1], line[char], line[char+1], line[char] == '¬')
            # print("aaaaaaa", line[char-1])
            if(direction < 0 and char-1 >= 0 and line[char-1] == '¬'):
                resultant_string += '¬'
            break    
    
        
    if direction < 0: resultant_string = resultant_string[::-1]
    print("----end-----")
    return [resultant_string, char_counter]

def pop_parentheses(fragment):
    """
    Removes the greater indented pair of parentheses
    it can find.

    Returns a string with less parentheses than before.
    """
    #pops the first (
    fragment = re.sub(r'\(', '', fragment, count=1)
    #pops the last )
    fragment = re.sub(r'\)(?=[^)]*$)', '', fragment, count=1)
    return fragment


def _switch_operator(fragment):
    """
    This function, given an expression, switches the
    first encountered ∨ or ∧ operator, and switches
    every occurrence of it to the opposite.

    Returns a string with occurrence of the first operator
    it finds, inverted.
    """
    operator = bool(re.search(r'∨', fragment))
    if(operator): return re.sub(r'∨', r'∧', fragment)
    else: return re.sub(r'∧', r'∨', fragment)


def negate_every_member(fragment):
    """
    This function, given an expression, negates every predicate
    it finds.

    Returns a string with every predicate negated.
    """
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

def replyce(string, look_for, change_to):
    """
    This function uses RegExpressions to find a given expression
    or character, and change it to an another given expresion
    or character.

    Returns a string with everything occurrence replaced.
    """
    return string.replace(look_for, change_to)

def replyce_all_symmetrical(line, look_for, change_to):
    """
    This function uses the replyce() function to symmetrically
    replace every character in look_for (param 1), to a 
    respective character in change_to (param 2).

    Returns a string with everything occurrence replaced.
    """
    for case in range(len(look_for)):
        line = replyce(line, look_for=look_for[case], change_to=change_to[case])
    return line

def highlight(line):
    """
    This function uses RegExpressions to find and
    highlight predicates and quantifiers given an
    proper equation (does not support Latex).

    Returns a string with highlighted predicates and quantifiers.
    """
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
    """
    This function applies demorgan rules to a given
    part of an equation.

    Returns a string with the equation resolved.
    """
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

def resolve_implication(A, B):
    """
    This function applies conditional rules
    to a given pair of A and B parts of an
    equation.

    Returns an array with the first equation negated,
    the or operator, and the B.
    """
    
    return (demorgan(f"¬({A})") + f" ∨ {B}")

def resolve_bimplication(A, B):
    """
    This function uses the resolve_implication()
    function to apply biconditional rules to a given
    pair of A and B of an equation.

    Returns a string with the equation resolved.
    """
    _a = resolve_implication(A, B)
    _b = resolve_implication(B, A)

    return _concat_in_between(enclosure(_a), "∧", enclosure(_b))


def find_char_in_line(line, char):
    """
    This function looks for a char inside a given line,
    and returns the index of the first it can find.
    
    Returns None if it doesn't exists, or else the index 
    of where the character was found.
    """
    search = re.search(char, line)
    return None if not search else search.start()

def is_char_in_line(line, char):
    """
    This function looks for a char inside a given line,
    and returns a boolean.
    
    Returns a boolean.
    """
    return bool(re.search(char, line))

# def distributiva_disj(line):
#     char_pos = find_char_in_line(line, r'\)(.*?)\(')
#     if char_pos is not None:
        
#         if v in A:
#             Get(Aa, Ab)
#             line = (B ^ Aa) v (B ^ Ab)
#         elif v in B:
#             Get(Ba, Bb)
#             line = (A ^ Ba) v (A ^ Bb)
#     return line



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

    """
    This function applies all necessary rules and
    checkers to resolve an given equation.

    Returns a string with the equation resolved.
    """

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
#  resolve_imps - PENDING
#  resolve_bimps - PENDING
#  distribas - PENDING
#  SPLIT - DONE
#  skolem - COMYCO - OPTIONAL (talves)
#  a, b - FEYTO
#  montage - PENDING


# line = "¬((*X* ∨ ¬*Y*) ∧ (¬*X* ∨ *Y*))"
# line = distribute(line) # "(¬*X* ^ *Y*) v (*X* ^ ¬*Y*)"
# line = de_negate_every_member(line) # (*X* ^ ¬*Y*) v (¬*X* ^ *Y*)
# line = _switch_operator(line) # (*X* v ¬*Y*) ^ (¬*X* v *Y*)


# ~((X v ~Y) ^ (~X v Y))
# ¬((*X* v ¬*Y*) ^ (¬*X* v *Y*))
# (P ^ ¬Q ^ R(x))

# line = "¬(*X* ∨ *Y*) ↔ (¬*X* ∨ (*Y* → *U*)) ↔ (*A* ∨ *B*)"
# *A* ↔ ( (*B* ∨ *C*) → (*D* ∧ *F*) ) ∨ ( (*G* ↔ *H*) ∧ *I* ↔ ( *J* → *K* ) ) 
line = "(*A* ∧ *P*) ↔ (*C* ∧ *E*)"
A = find_directionally(line, 13, -1)
B = find_directionally(line, 13, 1)
x = resolve_bimplication(A[0], B[0])
# x = _concat_in_between(A, x[1], x[2])
print(x)

# print(find_char_in_line(line, "∧"))

# line = " (*(P v Q*) v (*G* ^ U))) v (*A* ^ B )"
# char_pos = find_char_in_line(line, r'\)(.*?)\(')
# print(char_pos)