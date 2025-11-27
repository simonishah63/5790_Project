# Comparative Framework for Evaluating Model Checkers on Safety-Critical Embedded Software

A systematic framework for comparative evaluation of formal verification tools (CBMC, Frama-C, E-ACSL) on safety-critical embedded software properties. This research provides empirical evidence for tool selection and performance trade-offs in embedded systems verification.

## 📋 Research Overview

This project addresses the critical challenge of selecting appropriate formal verification tools for safety-critical embedded systems. Our framework provides:

- **Systematic evaluation methodology** using Docker containerization
- **Specialized benchmark suite** covering 10 safety-critical property categories
- **Multi-dimensional metrics** (correctness, performance, usability, expressiveness)
- **Empirical performance data** revealing 26.8x performance differences between verification paradigms
- **Property-specific tool recommendations** based on quantitative analysis

**Key Finding:** CBMC demonstrates 26.8x faster performance than Frama-C WP while detecting 94 concrete bugs across benchmarks.

## 🚀 Quick Start

### Prerequisites

- **Docker** and **Docker Compose**
- **Python 3.8+** with virtual environment
- **Git** for version control

### Installation & Setup

1. **Clone the repository**
   ```
    git clone https://github.com/simonishah63/5790_Project.git
   cd 5790_Project
   ```

2. **Run automated setup**
    ```
    chmod +x setup_and_run.sh
    ./setup_and_run.sh
    ```

3. **Manual setup (alternative)**
    ```
    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate

    # Install dependencies
    pip install -r requirements.txt

    # Build Docker images
    docker-compose build --platform linux/amd64

    # Generate benchmarks
    python src/benchmark_generator.py
    ```

### Running Experiments  
   ```
   python run_experiments.py
   ```

## Tools Evaluated
| Tool | Paradigm | Primary Strength | Execution Time |
|------|------|------------|
| CBMC | Bounded Model Checking | Bug Finding | 0.20s (avg) |
| Frama-C EVA | Abstract Interpretation | Sound Analysis | 0.23s (avg) |
| Frama-C WP | Deductive Verification | Theorem Proving | 5.37s (avg) |
| E-ACSL | Runtime Verification | Runtime Monitoring | 0.55s (avg) |

## Benchmark Categories
Memory Safety: Buffer overflows, null pointer dereferences
Arithmetic Safety: Integer overflows, division by zero
Resource Usage: Memory leaks, infinite loops
Functional Correctness: Pre/post conditions, API contracts
Standards Compliance: MISRA C violations
Concurrency Safety: Data races, synchronization
Complex State Machines: Mode confusion, invariant preservation

## Authors

ENGR 5790 – Group 7  
- Akidabanu Mohammadazam Laliwala: akidabaumohammadazam.laliwala@ontariotechu.net
- Chinimilli Naga Manisha: Chinimilli.nagamanisha@ontariotechu.net
- Mehakpreet Singh: mehakpreet.singh3@ontariotechu.net
- Simoni Mehul Solanki: simonimehul.solanki@ontariotechu.net