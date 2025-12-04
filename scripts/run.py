#!/usr/bin/env python3
import requests, json, re, sys
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

MODELS = [
    "mistral:7b",
    "gemma3:27b",
    "gpt-oss:20b"
]

OLLAMA_URL = "http://0.0.0.0:11434/api/chat"

# Folder paths relative to repo root
ROOT = Path(__file__).resolve().parent.parent
INTERPRETER_FILE = ROOT / "interpreter" / "interpreter.txt"
BENCH_FILE       = ROOT / "benchmark" / "bench_100.txt"

PROGRAMS = {
    "D": ROOT / "programs" / "program_decl.cogBASIC",
    "P": ROOT / "programs" / "program_proc.cogBASIC",
    "C": ROOT / "programs" / "program_conflict.cogBASIC",
    "R": ROOT / "programs" / "program_resolution.cogBASIC",
}

RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)


# ============================================================
# STREAMING CHAT
# ============================================================
def chat_stream(prompt: str, model: str):
    r = requests.post(
        OLLAMA_URL,
        json={"model": model, "messages": [{"role": "user", "content": prompt}], "stream": True},
        stream=True, timeout=600,
    )
    r.raise_for_status()

    for line in r.iter_lines():
        if not line:
            continue
        try:
            body = json.loads(line.decode("utf-8"))
        except:
            continue

        if "message" in body:
            yield body["message"].get("content", "")
        if body.get("done"):
            break


# ============================================================
# BENCHMARK PARSER
# ============================================================
def load_benchmark(path: Path):
    """
    Parses benchmark file with entries of the form:

    ### TASK: R01
    TYPE: R
    SCENARIO:
    ...
    """
    text = path.read_text()
    blocks = re.split(r"(?im)^###\s*TASK\s*:\s*", text)[1:]
    tasks = []

    for blk in blocks:
        id_line = re.match(r"\s*([^\r\n]+)", blk)
        if not id_line:
            continue

        tid = id_line.group(1).strip()

        mtype = re.search(r"(?im)^TYPE\s*:\s*([DPCR])", blk)
        if not mtype:
            print(f"⚠️ Missing TYPE in task {tid}, skipping.")
            continue
        ttype = mtype.group(1).strip()

        mscen = re.search(r"(?is)SCENARIO\s*:\s*(.*)$", blk)
        if not mscen:
            print(f"⚠️ Missing SCENARIO in task {tid}, skipping.")
            continue
        scen = mscen.group(1).strip()

        tasks.append({
            "id": tid,
            "type": ttype,
            "scenario": scen
        })

    return tasks


# ============================================================
# MAIN
# ============================================================
def main():
    print("🔍 Loading interpreter and benchmark...\n")

    if not INTERPRETER_FILE.exists():
        print(f"❌ Missing interpreter file: {INTERPRETER_FILE}")
        return
    if not BENCH_FILE.exists():
        print(f"❌ Missing benchmark file: {BENCH_FILE}")
        return

    interpreter = INTERPRETER_FILE.read_text().strip()
    tasks = load_benchmark(BENCH_FILE)

    print(f"📦 Found {len(tasks)} tasks.\n")

    # ========================================================
    # RUN MODELS
    # ========================================================
    for model in MODELS:
        print("\n============================================================")
        print(f"🏁 RUNNING BENCHMARK WITH MODEL: {model}")
        print("============================================================\n")

        results_path = RESULTS_DIR / f"results_{model.replace(':','_')}.txt"
        results_path.write_text(f"=== RESULTS FOR MODEL: {model} ===\n\n")

        for t in tasks:
            program_path = PROGRAMS.get(t["type"])
            if not program_path or not program_path.exists():
                print(f"❌ Missing program file for TYPE={t['type']} — skipping task {t['id']}")
                continue

            program = program_path.read_text().strip()

            print("\n============================================================")
            print(f"🧩 TASK: {t['id']}   (TYPE {t['type']})")
            print("------------------------------------------------------------")
            print(f"Scenario:\n{t['scenario']}\n")
            print(f"Using program: {program_path.name}\n")

            exec_prompt = (
                "You are the CogBASIC Interpreter.\n"
                + interpreter +
                "\n\n--- Scenario Text ---\n"
                + t["scenario"] +
                "\n--- End Scenario ---\n\n"
                "--- CogBASIC Program ---\n"
                + program +
                "\n\nExecute step by step and produce your full output."
            )

            print("⏳ Executing...\n")

            output = ""
            for chunk in chat_stream(exec_prompt, model):
                sys.stdout.write(chunk)
                sys.stdout.flush()
                output += chunk

            print("\n\n✅ Finished.\n")

            with results_path.open("a") as f:
                f.write("============================================================\n")
                f.write(f"TASK {t['id']} (TYPE {t['type']})\n")
                f.write("------------------------------------------------------------\n")
                f.write(output)
                f.write("\n\n")

        print("============================================================")
        print(f"🌟 FINISHED ALL TASKS FOR MODEL {model}")
        print(f"📄 Saved results to {results_path}")
        print("============================================================\n")


if __name__ == "__main__":
    main()