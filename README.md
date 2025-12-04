# CogBASIC: A Cognitive Programming Framework for LLMs

CogBASIC is a retro-inspired cognitive programming language executed inside large language models.
It provides a deterministic, stepwise interpreter—similar to vintage BASIC—allowing LLMs to:

- extract declarative knowledge
- extract procedural knowledge
- detect contradictions
- resolve conflicting beliefs
- maintain structured working memory
- follow line-numbered control flow
- execute transparent, inspectable reasoning traces

This repository accompanies the research paper:

paper/cognitiveBASIC.pdf  
A detailed explanation of the CogBASIC design, experiments, and evaluation results.

-------------------------------------------------------------------------------

## Concept

Rather than relying on free-form prompting, CogBASIC embeds a lightweight programming language inside an LLM.
The model must:

1. read and execute line-numbered instructions  
2. maintain structured memory blocks  
3. simulate program execution step by step  
4. produce a detailed reasoning trace  

Example program (excerpt):

10 REM Extract declarative knowledge, detect conflicts, and resolve them  
20 LET working = INPUT()  
30 facts = EXTRACT_DECLARATIVE(working)  
40 ADD declarative FROM facts  
50 conflicts_tmp = DETECT_CONFLICTS()  
60 ADD conflicts FROM conflicts_tmp  
70 IF CONFLICTS_COUNT() > 0 THEN 90  
80 END  
90 resolution = RESOLVE_CONFLICTS()  
100 END

The LLM essentially acts as a virtual machine, providing transparent cognitive computation.

-------------------------------------------------------------------------------

# Repository Structure

cogbasic/  
│  
├── interpreter/  
│   └── interpreter.txt  
│  
├── programs/  
│   ├── program_decl.cogBASIC  
│   ├── program_proc.cogBASIC  
│   ├── program_conflict.cogBASIC  
│   └── program_resolution.cogBASIC  
│  
├── benchmark/  
│   └── bench_25.txt  
│  
├── scripts/  
│   └── run.py  
│  
├── paper/  
│   └── cognitiveBASIC.pdf  
│  
├── results/  
│   └── results_model.txt  
│  
└── README.md  

-------------------------------------------------------------------------------

# Installation and Setup

### 1. Install Ollama

curl -fsSL https://ollama.com/install.sh | sh

Pull example models:

ollama pull mistral:7b  
ollama pull gpt-oss:20b  
ollama pull gemma3:27b

### 2. Clone the repository

git clone https://github.com/<your-user>/cogbasic.git  
cd cogbasic

### 3. Optional: create a Python environment

python3 -m venv venv  
source venv/bin/activate  
pip install requests

-------------------------------------------------------------------------------

# Running the Benchmark

Execute:

python scripts/run.py

This will:

- load the interpreter  
- load all four cognitive programs  
- load all benchmark scenarios  
- run each model on each task  
- save logs under `results/`  

-------------------------------------------------------------------------------

# Interpreting the Results

Execution logs contain:

- each executed line  
- the memory state after each instruction  
- the final memory block  

This allows assessment of:

- memory stability  
- correct extraction  
- conflict detection  
- consistency of reasoning steps  

-------------------------------------------------------------------------------

# Cognitive Programs Provided

D — Declarative extraction  
P — Procedural extraction  
C — Conflict detection  
R — Conflict resolution  

All programs are modular and short, enabling easy extension.

-------------------------------------------------------------------------------

# Reproducing Evaluation Results

Run:

python scripts/run.py

Results will be stored in:

results/results_MODELNAME.txt

-------------------------------------------------------------------------------

# Extending CogBASIC

CogBASIC can be extended with:

- new primitives and memory structures  
- additional cognitive tasks  
- hierarchical controllers  
- evolved cognitive programs (e.g., via genetic algorithms)

-------------------------------------------------------------------------------

# Reference

For the complete research description, experimental results, and theoretical motivation, see:

paper/cognitiveBASIC.pdf

-------------------------------------------------------------------------------

# Contributing

Contributions are welcome.  
Suggestions for new primitives, tasks, or integrations can be submitted via issues or pull requests.

-------------------------------------------------------------------------------

# License

MIT License