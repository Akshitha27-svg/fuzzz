import random
import string
import os
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(filename='fuzzing_log.txt', level=logging.INFO)

# Directory to store crashing inputs
CRASH_DIR = "crashes"
os.makedirs(CRASH_DIR, exist_ok=True)

# -------------------------------
# Simulated Target Function
# -------------------------------
def mock_sumatra_pdf_parser(input_data):
    """
    Simulated behavior of target parsing function of Sumatra PDF.
    In reality, this would be an API like PdfParser::ParseObject()
    """
    # Simulated crash conditions
    crash_keywords = ['%PDF-1337', 'MALFORMED-XREF', 'OVERFLOW']
    
    for keyword in crash_keywords:
        if keyword in input_data:
            raise ValueError(f"Crash Triggered by Input: {keyword}")
    
    # Simulate successful parsing
    return "Parsed successfully"

# -------------------------------
# Input Mutation Engine
# -------------------------------
def mutate_input(seed_input):
    mutations = []
    
    # Add random bytes
    for _ in range(5):
        mutation = seed_input + ''.join(random.choices(string.printable, k=10))
        mutations.append(mutation)
    
    # Inject special crash triggers
    mutations.append(seed_input + '%PDF-1337')       # Simulated crash
    mutations.append(seed_input + 'MALFORMED-XREF')  # Simulated crash
    mutations.append(seed_input + 'OVERFLOW')        # Simulated crash
    
    return mutations

# -------------------------------
# Fuzzing Harness Simulator
# -------------------------------
def fuzz_target(seed_input, iterations=10):
    logging.info(f"=== Fuzzing started at {datetime.now()} ===")
    
    for i in range(iterations):
        mutated_inputs = mutate_input(seed_input)
        
        for index, mutated_input in enumerate(mutated_inputs):
            try:
                result = mock_sumatra_pdf_parser(mutated_input)
                logging.info(f"[OK] Iteration {i}-{index} | Result: {result}")
            
            except Exception as e:
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                crash_file = f"{CRASH_DIR}/crash_{timestamp}_{i}_{index}.txt"
                with open(crash_file, 'w') as f:
                    f.write(mutated_input)
                logging.error(f"[CRASH] Iteration {i}-{index} | {str(e)} | Input saved to {crash_file}")

# -------------------------------
# Run Fuzzing Session
# -------------------------------
if __name__ == "__main__":
    seed = "%PDF-1.7 Sample Document"
    fuzz_target(seed, iterations=20)
    print("Fuzzing session complete. Check fuzzing_log.txt and crashes/ folder.")
