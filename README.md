# Cognitive BASIC

Cognitive BASIC is a lightweight, line-numbered cognitive programming framework executed *inside* large language models.  
It provides deterministic control flow for tasks such as declarative extraction, procedural extraction, conflict detection, and conflict resolution.  
All reasoning steps run in-model through a textual interpreter.

This repository accompanies the research paper:
paper/cognitiveBASIC.pdf

-------------------------------------------------------------------------------

## Concept

Cognitive BASIC embeds a minimal BASIC-style program inside an LLM.  
The model must execute instructions step by step, maintain structured memory, and output an explicit reasoning trace.

Example (excerpt):

10 LET working = INPUT()  
20 facts = EXTRACT_DECLARATIVE(working)  
30 ADD declarative FROM facts  
40 conflicts_tmp = DETECT_CONFLICTS()  
50 ADD conflicts FROM conflicts_tmp  
60 IF CONFLICTS_COUNT() > 0 THEN 90  
70 END  
90 resolution = RESOLVE_CONFLICTS()  
100 END

-------------------------------------------------------------------------------

## Repository Structure

cognitive-BASIC/  
├── interpreter/interpreter.txt  
├── programs/program_*.cogBASIC  
├── benchmark/bench_25.txt  
├── scripts/run.py  
├── results/  
└── paper/cognitiveBASIC.pdf

-------------------------------------------------------------------------------

## Installation

Install Ollama:

curl -fsSL https://ollama.com/install.sh | sh  
ollama pull mistral:7b

Clone the repo:

git clone https://github.com/evolution-strategies/cognitive-BASIC.git  
cd cognitive-BASIC

Optional Python env:

python3 -m venv venv  
source venv/bin/activate  
pip install requests

-------------------------------------------------------------------------------

## Running the Benchmark

python scripts/run.py

This loads the interpreter, executes all programs on all scenarios, and writes results to `results/`.

-------------------------------------------------------------------------------

## Cognitive Programs

D — Declarative extraction  
P — Procedural extraction  
C — Conflict detection  
R — Conflict resolution  

-------------------------------------------------------------------------------

## Extending Cognitive BASIC

The framework supports adding new primitives, memory structures, cognitive tasks, or tool-use steps.  
Programs are short and modular, making extensions easy.

-------------------------------------------------------------------------------

## Reference

For the full research description and evaluation:
paper/cognitiveBASIC.pdf

-------------------------------------------------------------------------------

## License

MIT License