# SAT_2025

## Informații utile ℹ️

**Titlul lucrării:** *Problema SAT în Informatică: Metode de rezolvare și analiză a algoritmilor tradiționali: DP, DPLL, Rezoluție.*  

**Autor:** Alexandra - Sofia Csizmadia, Departamentul de Informatică, Facultatea de Matematică și Informatică, Universitatea de Vest din Timișoara, Timișoara, România  

**E-mail:** alexandra.csizmadia06@e-uvt.ro  

**Rezumat:**  

Problema satisfiabilității unei formule (SAT) este una dintre cele mai fundamentale probleme ale informaticii teoretice, fiind prima demonstrată ca NP-completă. Această lucrare explorează și analizează metodele clasice de abordare ale problemei SAT, incluzând algoritmii Davis-Putnam (DP), Davis–Putnam–Logemann–Loveland (DPLL) și algoritmul de rezoluție. Lucrarea studiază eficiența acestor algoritmi prin analiza memoriei utilizate, a timpului de execuție, a numărului de pași executați și a timpului CPU-ului.  



Rezultatele experimentale oferă dovezi ale beneficiilor și limitărilor meto- delor studiate, contribuind la înțelegerea performanței algoritmilor în cazul problemelor NP-complete. Concluziile evidențiază impactul acestor metode asupra domeniului informaticii și propun direcții viitoare de cercetare.  

**Acest proiect este o aplicație scrisă în Python, rulabilă pe Windows, macOS și Linux, folosind Visual Studio Code.**  

## Fișiere 📂

Folder-ul mare conține:
  - programele și fișierele cu conexiune directă cu acesta în folder-ul `Program`
  - seturile de date și excel-uri și grafice sunt fiecare fie în câte o arhivă, fie în foldere individuale cu nume.
  - **IMPORTANT** mai există două fișiere de date care nu rulează, mai exact `random_500` și `set_validare_4` care au dimensiuni prea mari pentru GitHub. în caz că se doresc a fi studiate rog să primesc e-mail pentru a le trimite prin WeTransfer 

## Instrucțiuni de instalare și rulare 📖

1. Accesează pagina acestui proiect pe GitHub.
2. Apasă pe butonul verde **Code** și selectează **Download ZIP**.
3. După descărcare:
   - Pe **Windows**: clic dreapta pe fișierul ZIP → „Extract All...” → „Extract”
   - Pe **macOS**: dublu clic pe fișierul ZIP
   - Pe **Linux**: clic dreapta → „Extract Here” sau în terminal: `unzip nume-arhiva.zip`
4. Deschide **Visual Studio Code**.
5. În VS Code, mergi la `File` → `Open Folder...` și selectează folder-ul dezarhivat.
6. Dacă nu ai Python instalat:
   - Pe **Windows/macOS**: descarcă de pe [python.org](https://www.python.org/downloads/)
   - Pe **Linux (Debian/Ubuntu)**: instalează cu `sudo apt install python3`
7. Verifică instalarea Python:
   - În terminal: `python --version` sau `python3 --version`
8. În Visual Studio Code:
   - Apasă `Ctrl + Shift + P` (`Cmd + Shift + P` pe Mac), caută `Python: Select Interpreter` și alege versiunea Python instalată.
   - Dacă VS Code îți cere să instalezi extensia Python, acceptă.
9. Deschide fișierul principal (`SAT_17052025.py`).
10. Verifică să ai toate pachetele instalate
    - folosește comanda `pip install psutil` pentru python și `python3 -m pip install psutil` pentru python3
11. Copiază datele de intrare
    - în folder-ul `Seturi de date și analize finale` vei găsi mai multe foldere cu mai multe fișiere
    - deschizi folder-ul dorit și va exista, sub diferite denumiri, un fișier cu configurația și datele de test în format .txt pe care îl deschizi
    - Ctrl + A, Ctrl + C și revi în folder-ul cu proiectul principal unde vei găsi un fișier `input.txt`
    - Ctrl + A, Ctrl + V și ștergi primele linii astfel încât seturile de date să înceapă de la linia 1
    - Ctrl + S
12. Pentru a rula programul principal `SAT_17052025.py`:
    - deschide în Visual Studio Code proiectul
    - asigură-te că în `input.txt` există date, dacă nu du-te la pasul 13 și revin-o la 12
    - Apasă pe butonul `Run` din colțul dreapta sus al editorului
    - Sau deschide terminalul în VS Code și scrie `python SAT_17052025.py` sau `python3 SAT_17052025.py`
13. Pentru a rula generatorul de clauze:
    - deschide fișierul `generator_clauze.py`
    - modifică parametrii doriți
    - Apasă pe butonul `Run` din colțul dreapta sus al editorului
    - Sau deschide terminalul în VS Code și scrie `python generator_clauze.py` sau `python3 generator_clauze.py`
14. Pentru a rula `transformare_csv.py`:
    - deschide `transformare_csv.py`
    - asigură-te ca în fișierul `output.txt` se află date, dacă nu du-te la pasul 12.
    - Apasă pe butonul `Run` din colțul dreapta sus al editorului
    - Sau deschide terminalul în VS Code și scrie `python transformare_csv.py` sau `python3 transformare_csv.py`







