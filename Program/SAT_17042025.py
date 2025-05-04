import time
import sys
import psutil
from concurrent.futures import ProcessPoolExecutor, as_completed

sys.setrecursionlimit(10000)

def parse_input_file_generator(filename):
    current_set = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                if current_set:
                    yield current_set
                    current_set = []
            else:
                clause = list(map(int, line.split()))
                current_set.append(clause)
        if current_set:
            yield current_set


def write_output_file(filename, results):
    with open(filename, "w", encoding="utf-8") as f:
        for i, res in enumerate(results):
            f.write(f"Set {i + 1}:\n")
            for alg_name, values in res.items():
                # Fiecare valoare este un tuple de forma:
                # (result_message, duration (sec), cpu_time (sec), memory_used (MB))
                result, duration, cpu_time, memory_used = values
                f.write(f"  {alg_name}: {result}, {duration:.6f} sec, CPU: {cpu_time:.6f} sec, Mem: {memory_used:.2f} MB\n")
            f.write("\n")

#--- Rezolutie ---
def resolve_pair(ci, cj):
    resolvents = set()
    for literal in ci:
        if -literal in cj:
            resolvent = (ci - {literal}) | (cj - {-literal})
            resolvents.add(frozenset(resolvent))
    return resolvents


def resolution(clauses, timeout=10, max_clauses=1000, return_clauses=False):
    start_time = time.time()
    clauses_set = set(frozenset(clause) for clause in clauses)
    clause_count = len(clauses_set)

    print("REZOLUtIE")
    while True:
        if time.time() - start_time > timeout:
            print("Rezolutia a fost abandonata din cauza timeout-ului de 50 secunde.")
            if return_clauses:
                return "Prea dificila", clause_count, list(clauses_set)
            else:
                return "Prea dificila", clause_count

        if len(clauses_set) > max_clauses:
            print(f"Limita de {max_clauses} clauze a fost atinsa.")
            if return_clauses:
                return "Satisfiable", clause_count, list(clauses_set)
            else:
                return "Satisfiable", clause_count

        new_clauses = set()
        pairs = [(ci, cj) for ci in clauses_set for cj in clauses_set if ci != cj]
        for (ci, cj) in pairs:
            resolvents = resolve_pair(ci, cj)
            if frozenset() in resolvents:  # Clauza goala derivata
                if return_clauses:
                    return "Unsatisfiable", clause_count, list(clauses_set)
                else:
                    return "Unsatisfiable", clause_count
            new_clauses = new_clauses.union(resolvents)

        if new_clauses.issubset(clauses_set):
            if return_clauses:
                return "Satisfiable", clause_count, list(clauses_set)
            else:
                return "Satisfiable", clause_count

        clauses_set.update(new_clauses)
        clause_count = len(clauses_set)


# --- DP  ---
def dp(clauses, timeout=10, max_steps=100, max_clauses=10000):
    print("DP")
    sys.stdout.flush()
    start_time = time.time()

    def dp_recursive(formula, steps):
        # Verificare numar maxim de pasi.
        if steps >= max_steps:
            print(f"Numarul maxim de pasi ({max_steps}) a fost atins in DP.")
            sys.stdout.flush()
            return "Prea dificila", steps

        # Verificare timeout.
        if time.time() - start_time > timeout:
            print(f"Timeout atins in DP dupa {timeout} secunde.")
            sys.stdout.flush()
            return "Prea dificila", steps

        # Verificare daca numarul de clauze este prea mare:
        if len(formula) > max_clauses:
            print(f"Numarul maxim de clauze ({max_clauses}) a fost depasit. DP renunta.")
            sys.stdout.flush()
            return "Prea dificila", steps

        # Daca formula este goala, ea este satisfiabila.
        if not formula:
            return "Satisfiable", steps

        # Daca exista o clauza goala, formula este insatisfiabila.
        for clause in formula:
            if not clause:
                return "Unsatisfiable", steps

        # Regula 1: Eliminarea literaliilor pure.
        all_literals = [lit for clause in formula for lit in clause]
        pure_literals = []
        for var in set(map(abs, all_literals)):
            positive_exists = any(lit == var for clause in formula for lit in clause)
            negative_exists = any(lit == -var for clause in formula for lit in clause)
            if positive_exists and not negative_exists:
                pure_literals.append(var)
            elif negative_exists and not positive_exists:
                pure_literals.append(-var)
        if pure_literals:
            new_formula = []
            for clause in formula:
                # Elimina clauzele care contin cel putin un literal pur.
                if not any(lit in clause for lit in pure_literals):
                    new_formula.append(clause)
            return dp_recursive(new_formula, steps + len(pure_literals))
        
        # Regula 2: Pasul de rezolutie.
        chosen_var = None
        for clause in formula:
            for lit in clause:
                if -lit in [l for c in formula for l in c]:
                    chosen_var = abs(lit)
                    break
            if chosen_var is not None:
                break
        
        # Daca nu se gaseste o variabila de bifurcare, formula este satisfiabila.
        if chosen_var is None:
            return "Satisfiable", steps
        
        pos_clauses = [clause for clause in formula if chosen_var in clause]
        neg_clauses = [clause for clause in formula if -chosen_var in clause]
        remaining_clauses = [clause for clause in formula if (chosen_var not in clause and -chosen_var not in clause)]
        
        # Generare rezolvante prin combinarea clauzelor din pos si neg.
        resolvents = []
        for clause_pos in pos_clauses:
            for clause_neg in neg_clauses:
                # Elimina literalul ales si complementul sau, combinand restul literaliilor.
                resolvent = list((set(clause_pos) - {chosen_var}) | (set(clause_neg) - {-chosen_var}))
                # Evita rezolvantele tautologice.
                if any(l in resolvent and -l in resolvent for l in resolvent):
                    continue
                resolvents.append(resolvent)
        
        new_formula = remaining_clauses + resolvents
        
        # Verifica progresul: daca noua formula este aceeasi ca cea curenta, renunta.
        if sorted([sorted(clause) for clause in new_formula]) == sorted([sorted(clause) for clause in formula]):
            print("Nu s-a inregistrat progres in reducerea formulei. DP renunta.")
            sys.stdout.flush()
            return "Prea dificila", steps
        
        return dp_recursive(new_formula, steps + 1)
    
    return dp_recursive(clauses, 0)



# --- DPLL  ---
def simplify_clauses(clauses, assignment):
    new_clauses = []
    for clause in clauses:
        new_clause = set()
        satisfied = False
        for lit in clause:
            var = abs(lit)
            if var in assignment:
                if (lit > 0 and assignment[var]) or (lit < 0 and not assignment[var]):
                    satisfied = True
                    break
            else:
                new_clause.add(lit)
        if not satisfied:
            new_clauses.append(new_clause)
    return new_clauses


def dpll(clauses, assignment, timeout=10, max_steps=300):
    print("DPLL")
    start_time = time.time()

    def dpll_recursive(clauses, assignment, steps):
        # Verificam timeout-ul
        if time.time() - start_time > timeout:
            print(f"Timeout atins dupa {timeout} secunde.")
            return "Prea dificila", steps

        # Verificam limita de pasi
        if steps > max_steps:
            print(f"Numarul maxim de pasi ({max_steps}) a fost atins.")
            return "Prea dificila", steps

        # Simplificam clauzele
        clauses = simplify_clauses(clauses, assignment)

        if any(len(clause) == 0 for clause in clauses):
            return "Unsatisfiable", steps
        if not clauses:
            return "Satisfiable", steps

        # Unit propagation
        unit_clauses = [clause for clause in clauses if len(clause) == 1]
        if unit_clauses:
            for clause in unit_clauses:
                lit = next(iter(clause))
                assignment[abs(lit)] = (lit > 0)
            return dpll_recursive(clauses, assignment, steps + len(unit_clauses))

        # Pure literal elimination
        all_lits = {lit for clause in clauses for lit in clause}
        for lit in list(all_lits):
            if -lit not in all_lits:
                assignment[abs(lit)] = (lit > 0)
                return dpll_recursive(clauses, assignment, steps + 1)

        # Ramificare
        for clause in clauses:
            for lit in clause:
                if abs(lit) not in assignment:
                    # Ramura in care literalul ia valoarea True
                    assignment_copy_true = assignment.copy()
                    assignment_copy_true[abs(lit)] = (lit > 0)
                    result_true, steps_true = dpll_recursive(clauses, assignment_copy_true, steps + 1)
                    if result_true == "Satisfiable":
                        assignment.update(assignment_copy_true)
                        return result_true, steps_true

                    # Ramura in care literalul ia valoarea False
                    assignment_copy_false = assignment.copy()
                    assignment_copy_false[abs(lit)] = not (lit > 0)
                    result_false, steps_false = dpll_recursive(clauses, assignment_copy_false, steps + 1)
                    if result_false == "Satisfiable":
                        assignment.update(assignment_copy_false)
                        return result_false, steps_false

                    # Daca una dintre ramuri a intrerupt executia din cauza limitelor, propaga mesajul "Prea dificila"
                    if (isinstance(result_true, str) and result_true.startswith("Prea dificila")) or \
                       (isinstance(result_false, str) and result_false.startswith("Prea dificila")):
                        return "Prea dificila", max(steps_true, steps_false)
                    
                    # Daca ambele ramuri s-au incheiat cu "Unsatisfiable", se returneaza aceasta stare
                    return "Unsatisfiable", steps
        return "Unsatisfiable", steps

    return dpll_recursive(clauses, assignment, 0)


# ---------------------------
# PROCESSING CLAUSE SETS (CU METRICI CPU & MEMORIE)
# ---------------------------
def process_clause_set(clauses, set_index, resolution_timeout=10):
    results = {}
    proc = psutil.Process()

    # --- Rezolutie ---
    start_cpu = proc.cpu_times()
    start_mem = proc.memory_info().rss
    start_time = time.time()
    
    # Trimitem timeout-ul functiei `resolution`
    res_resolution, clause_count = resolution(clauses, timeout=resolution_timeout, max_clauses=1000)
    duration = time.time() - start_time
    
    end_cpu = proc.cpu_times()
    end_mem = proc.memory_info().rss

    cpu_time = ((end_cpu.user + end_cpu.system) - (start_cpu.user + start_cpu.system))
    mem_used = max(0, end_mem - start_mem) / (1024 ** 2)  # evitam valori negative
    
    # Salvam rezultatele in dictionarul `results`
    results["Resolution"] = (
        f"{res_resolution}, {clause_count} clauze generate",
        duration,
        cpu_time,
        mem_used,
    )
    print(f"Rezolutie finalizata: {res_resolution}, durata: {duration:.2f} secunde.")

    # --- DP ---
    start_cpu = proc.cpu_times()
    start_mem = proc.memory_info().rss
    start_time = time.time()
    dp_result, dp_steps = dp(clauses, timeout=10, max_steps=1000)
    duration = time.time() - start_time
    end_cpu = proc.cpu_times()
    end_mem = proc.memory_info().rss

    cpu_time = ((end_cpu.user + end_cpu.system) - (start_cpu.user + start_cpu.system))
    mem_used = max(0, end_mem - start_mem) / (1024 ** 2)
    results["DP"] = (
        f"{dp_result}, {dp_steps} pasi",
        duration,
        cpu_time,
        mem_used,
    )

    # --- DPLL ---
    start_cpu = proc.cpu_times()
    start_mem = proc.memory_info().rss
    start_time = time.time()
    dpll_result, dpll_steps = dpll(clauses, {}, timeout=10, max_steps=300)
    duration = time.time() - start_time
    end_cpu = proc.cpu_times()
    end_mem = proc.memory_info().rss

    cpu_time = ((end_cpu.user + end_cpu.system) - (start_cpu.user + start_cpu.system))
    mem_used = max(0, end_mem - start_mem) / (1024 ** 2)
    results["DPLL"] = (
        f"{dpll_result}, {dpll_steps} pasi",
        duration,
        cpu_time,
        mem_used,
    )

    return set_index, results


# ---------------------------
# FUNCtIA PRINCIPALa (PARALELa)
# ---------------------------
def main_parallel():
    input_filename = "input.txt"
    output_filename = "output.txt"

    try:
        print("Citire fisier de intrare...")
        clause_sets = list(parse_input_file_generator(input_filename))
        print(f"S-au citit {len(clause_sets)} seturi de clauze.")
    except Exception as e:
        print(f"Eroare la citirea fisierului de intrare: {e}")
        return

    results = {}

    try:
        print("incep procesarea paralela...")
        with ProcessPoolExecutor() as executor:
            futures = {
                executor.submit(process_clause_set, clauses, idx): idx
                for idx, clauses in enumerate(clause_sets)
            }
            for future in as_completed(futures):
                try:
                    set_index, result = future.result()
                    results[set_index] = result
                    print(f"Setul {set_index + 1} procesat cu succes.")
                except Exception as e:
                    print(f"Eroare la procesarea setului {futures[future]}: {e}")
    except Exception as e:
        print(f"Eroare generala la procesarea paralela: {e}")
        return

    try:
        print("Scriere rezultate in fisier...")
        sorted_results = [results[i] for i in sorted(results.keys())]
        write_output_file(output_filename, sorted_results)
        print(f"Rezultatele au fost scrise cu succes in '{output_filename}'.")
    except Exception as e:
        print(f"Eroare la scrierea fisierului de iesire: {e}")
        return

    print(f"Procesare completa. S-au procesat {len(clause_sets)} seturi de clauze.")


if __name__ == "__main__":
    print("Pornire program...")
    main_parallel()
