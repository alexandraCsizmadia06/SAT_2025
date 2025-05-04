import random

num_formulas = 500    
num_clauses = 500    
num_literals = 500 
unsat_prob = 0.5    
literals_per_clause_range = (1,250)  

def generate_formula(num_clauses, num_literals, unsat_prob, literals_per_clause_range):
    min_literals, max_literals = literals_per_clause_range
    formula = set()  

    if random.random() < unsat_prob and num_clauses >= 2:
        literal = random.randint(1, num_literals)
        formula.add((literal,))   
        formula.add((-literal,)) 
        clauses_remaining = num_clauses - 2
    else:
        clauses_remaining = num_clauses

    for _ in range(clauses_remaining):
        clause_size = random.randint(min_literals, max_literals)
        if clause_size > num_literals:
            raise ValueError("Dimensiunea clauzei nu poate depasi numarul total de literali")
        
        vars_chosen = random.sample(range(1, num_literals + 1), clause_size)
        clause = tuple(
            (var if random.choice([True, False]) else -var)
            for var in vars_chosen
        )
        formula.add(clause)

    return [list(clause) for clause in formula]

def write_input_file(filename, formulas):
    with open(filename, "w") as f:
        for formula in formulas:
            for clause in formula:
                f.write(" ".join(map(str, clause)) + "\n")
            f.write("\n") 

if __name__ == "__main__":
    formulas = [
        generate_formula(num_clauses, num_literals, unsat_prob, literals_per_clause_range)
        for _ in range(num_formulas)
    ]
    write_input_file("input.txt", formulas)
    print(f"input.txt generated with {num_formulas} formulas.")
