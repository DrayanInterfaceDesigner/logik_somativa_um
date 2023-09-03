import re


def _process_line(line):

    x = r"(P \vee Q) \rightarrow (P \wedge Q)"

    arr = re.findall(r'\S+|\W', x)
    print(arr)



    # print(x)
    pass

_process_line("line")


def split_terms(line):
    pass

def decide_order(fragments):
    pass

def resolve(fragment):
    
    # Note: Another function already separated the
    # terms, and this function resolves one of them only.
    # So basically, run this, for every single one.

    # Takes a fragment of the equation

    # 1. Eliminates all imps and bimps.
    # 2. Applies DeMorgan
    # 3. Distributes
    # 4. Return it

    pass

def _or(a,b):
    pass
def _xor(a,b):
    pass
def _nor(a,b):
    pass
def _and(a,b):
    # Adds an "and" symbol between two expressions,
    # then, returns it.
    pass

def _switch_operator(operator):
    # removing white spaces
    operator = re.sub(r'\s', '', operator)
    if(operator == fr"\wedge"): return fr"\vee"
    else: return fr"\wedge"

def _is_composed(a):
    return (len(a) > 1)

def _enclosure(a):
    return f"({a})"

def _negate(a):

    # If it's composed (length > 1), it _encloses it, them add
    # the negate symbol. Then return it.
    return _enclosure(fr" \neg {a}") if _is_composed(a) else fr" \neg {a}"

def _concat_in_between(a, operator, b):
    return f"{a} {operator} {b}" or [a, operator, b]

def _imp(a,b):

    #It removes the implications between a and b formulas.
    #for example (P ^ Q) -> U

    # It applies the rule a -> b == ~a || b.

    #if one of them is composed (length > 1), negate everything enclosed.
    # for example: a = P ^ Q. 
    # 1. enclosure: (P ^ Q)
    # 2. negate: ~(P ^ Q)

    # Now, concat !a || b and return it.

    _a = _negate(_enclosure(a)) if _is_composed(a) else _negate(a)
    _b = _enclosure(b) if _is_composed(b) else b

    return _concat_in_between(_a, fr"\vee", _b)

def _bimp(a, b):

    #It removes the bi-implications between a and b formulas.
    #for example (P ^ Q) <-> U

    # It applies the rule a <-> b == (a -> b) ^ ( b -> a).
    []

    # Apply _imp() for both, then, unify them with "^" and return it.

    _a = _imp(a, b)
    _b = _imp(b, a)
    return _concat_in_between(_a, "\wedge", _b)

def _De_Morgan(a):

    # I'm assuming a is a string, if it's an array,
    # it's even easier! :)

    _temp_a = a
    _temp_a = re.sub(r'\s', '', _temp_a)
    _temp_a = re.sub(r'\(', '', _temp_a)
    
    # returns a if it doesn't need DeMorgan
    if(not _temp_a.startswith(fr'\neg')): return a

    # Applies DeMorgan's rules.
    # ASSUMES ALL IMPS AND BIMPS ARE RESOLVED

    # If there's a negation in front (else just return it)
    # 1. Detect negated symbols inside
    # 2. Detect the operator and or ||
    # 3. Make any negated positive
    # 4. Make any non negated, negated
    # 5. Switch the operator
    # 6. Return it

    pass

def _distribute(a,b):
    # This may be the most difficult one.
    # And yet simple enough.

    # Let's suppose A^(B or C)
    # Grab a (A^) term.
    # Concat it with the first term of b (B)
    # Enclosure it.
    # Do the same for the second term.
    # Detect the operator in b.
    # Switch the operator.
    # Concat both terms with the switched operator in between.
    # Return it

    pass














 #string is always a operation between two atoms
    #for example a ^ b, but never an implication
    #or bi-implication

    #1. Separe atoms
    #2. Detect operator
    #3. Apply calc