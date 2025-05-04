import csv
import re

def parse_data(input_file):
    data = []
    # Dictionar folosit pentru a mapa rezultatul la forma dorita
    result_mapping = {
        "Satisfiable": "SAT",
        "Unsatisfiable": "UNSAT"
    }
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # impartim continutul pe seturi, folosind "Set <numar>:" ca delimitator
        sets = re.split(r"Set \d+:", content)
        if sets[0].strip() == "":
            sets = sets[1:]
        
        # Modelele regex pentru fiecare sectiune
        resolution_pattern = (
            r"Resolution:\s*([\waista\s]+),\s*(\d+)\s+clauze generate,\s*([\d.]+)\s*sec,"
            r"\s*CPU:\s*([\d.]+)\s*sec,\s*Mem:\s*([\d.-]+)\s*MB"
        )
        dp_pattern = (
            r"DP:\s*([\waista\s]+),\s*(\d+)\s+pasi,\s*([\d.]+)\s*sec,"
            r"\s*CPU:\s*([\d.]+)\s*sec,\s*Mem:\s*([\d.-]+)\s*MB"
        )
        dpll_pattern = (
            r"DPLL:\s*([\waista\s]+),\s*(\d+)\s+pasi,\s*([\d.]+)\s*sec,"
            r"\s*CPU:\s*([\d.]+)\s*sec,\s*Mem:\s*([\d.-]+)\s*MB"
        )
        
        for set_str in sets:
            resolution_match = re.search(resolution_pattern, set_str)
            dp_match         = re.search(dp_pattern, set_str)
            dpll_match       = re.search(dpll_pattern, set_str)
            
            if resolution_match and dp_match and dpll_match:
                # Extragem rezultatul din DP si DPLL si mapam la forma dorita (SAT sau UNSAT)
                raw_dp    = dp_match.group(1).strip()
                raw_dpll  = dpll_match.group(1).strip()
                dp_result    = result_mapping.get(raw_dp, raw_dp)
                dpll_result  = result_mapping.get(raw_dpll, raw_dpll)
                
                if  dpll_result:
                    final_result = dpll_result
                else:
                    final_result = f"DP: {dp_result} / DPLL: {dpll_result}"
                
                # Pentru campurile numerice se inlocuieste punctul cu virgula.
                row = [
                    resolution_match.group(2).strip().replace(".", ","),  # pasi_rezolutie
                    resolution_match.group(3).strip().replace(".", ","),  # timp_rezolutie
                    resolution_match.group(4).strip().replace(".", ","),  # cpu_rezolutie
                    resolution_match.group(5).strip().replace(".", ","),  # memorie_rezolutie
                    dp_match.group(2).strip().replace(".", ","),          # pasi_dp
                    dp_match.group(3).strip().replace(".", ","),          # timp_dp
                    dp_match.group(4).strip().replace(".", ","),          # cpu_dp
                    dp_match.group(5).strip().replace(".", ","),          # memorie_dp
                    dpll_match.group(2).strip().replace(".", ","),        # pasi_dpll
                    dpll_match.group(3).strip().replace(".", ","),        # timp_dpll
                    dpll_match.group(4).strip().replace(".", ","),        # cpu_dpll
                    dpll_match.group(5).strip().replace(".", ","),        # memorie_dpll
                    final_result                                          # rezultat (SAT/UNSAT sau combinatie)
                ]
                print("Linie extrasa:", row)  # Debug, afiseaza randul extras
                data.append(row)
            else:
                print("Set nerecunoscut sau format incorect:", set_str)
    
    return data

def write_csv(data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        # Setam delimiterul la punct si virgula
        writer = csv.writer(f, delimiter=';')
        header = [
            "pasi_rezolutie", "timp_rezolutie", "cpu_rezolutie", "memorie_rezolutie",
            "pasi_dp", "timp_dp", "cpu_dp", "memorie_dp",
            "pasi_dpll", "timp_dpll", "cpu_dpll", "memorie_dpll", "rezultat"
        ]
        writer.writerow(header)
        writer.writerows(data)
    print(f"Datele au fost salvate in fisierul {output_file}.")

if __name__ == "__main__":
    input_file = "output.txt"  # Numele fisierului de intrare
    output_file = "fisier_output.csv"   # Numele fisierului CSV de iesire
    extracted_data = parse_data(input_file)
    
    if extracted_data:
        write_csv(extracted_data, output_file)
    else:
        print("Nu s-au gasit date valide in fisierul de intrare.")
