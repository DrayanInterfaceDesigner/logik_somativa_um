import re

predicates_chars_one = ['𝐴', '𝐵', '𝐶', '𝐷', '𝐸', '𝐹', '𝐺', '𝐻', '𝐼', '𝐽', '𝐾', '𝐿', '𝑀', '𝑁', '𝑂', '𝑃', '𝑄', '𝑅', '𝑆', '𝑇', '𝑈', '𝑉', '𝑊', '𝑋', '𝑌', '𝑍']
predicates_chars_two = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
latex = [fr"\wedge", fr"\vee", fr"\neg ", fr"\rightarrow", fr"\leftrightarrow", fr"\forall ", fr"\exists ", fr"\equiv "]
math = ["∧", "∨", "¬", "→", "↔", "∀", "∃", "≡"]
quantifiers = ["∀", "∃"]

# TODO:
# URGENT
# RECURSIVE!!!
# IT WILL TRY TO RESOLVE() EVERY TIME IT ENCOUNTERS A []
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
        print(fragment)

        # marking down every negated
        fragment = re.sub(r'¬\*(.*?)\*', r'¬&\1&', fragment)
        print(fragment)

        # negating every positive (non-marked)
        fragment = re.sub(r'\*(.*?)\*', r'*¬\1*', fragment)
        print(fragment)

        # de_negating every negated (marked down)
        fragment = re.sub(r'¬&([^&]*)&', r'*\1*', fragment)
        print(fragment)


        # > ¬(P ^ ¬Q ^ ¬¬P) negate every double negated, 
        fragment = re.sub(r'¬¬\*(.*?)\*', r'¬*\1*', fragment)
        # because
        # every double negated, if there's any, is actually a triple
        # negated, so in this case ¬¬P = P, ¬( is negating it again,
        # therefore, P = ¬P

        # ugly: removing by brute-force the first negation
        fragment = re.sub(r'¬\(', r'(', fragment)

        print(fragment)
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

    trimmed = fragment
    trimmed = trimmed.replace(" ", "")
    if(trimmed.startswith("¬(")):

        # This here will distribute the ¬ over the predicates.
        # For: ¬(¬P ^ Q ^ ¬¬P)
        # It will do:

        # finding by predicate
        # > ¬(¬P ^ $*Q*$ ^ ¬¬P) markdown the non-negated

        # finding by ¬ 
        # > ¬(P ^ $*Q*$  ^ ¬¬P) de_negate every negated
        
        # finding by predicate
        # > ¬(P ^ ¬Q ^ ¬¬P) negate the non-negated(marked down)

        # > ¬(P ^ ¬Q ^ ¬¬P) negate every double negated, 
        # because
        # every double negated, if there's any, is actually a triple
        # negated, so in this case ¬¬P = P, ¬( is negating it again,
        # therefore, P = ¬P
        print('yes')
        # replace every lonely ¬ with nothing
        fragment = re.sub(r'(?<!¬)¬(?!¬)', '', fragment)

        # replace every two or more ¬ with only one ¬
        fragment = re.sub(r'(¬{2,})', '¬', fragment)

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
    pass

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

def subdivide(line):
    return line


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
    print("Modified: ", line)
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
# print(_switch_operator(de_negate_every_member("¬((*X* ∨ ¬*Y*) ∧ (¬*X* ∨ *Y*))")))