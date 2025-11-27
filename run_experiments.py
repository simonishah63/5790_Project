#!/usr/bin/env python3
import json
import time
import yaml
from pathlib import Path
from src.benchmark_generator import BenchmarkGenerator
from src.tool_runners.cbmc_runner import CBMCRunner
from src.tool_runners.framac_runner import FramaCValueRunner, FramaCWPRunner
from src.tool_runners.eacsl_runner import EACSLRunner
from src.results_analyzer import ResultsAnalyzer
from src.visualization import ResultsVisualizer

class ExperimentRunner:
    def __init__(self, config_path="config/experiment_config.yaml"):
        self.config = self.load_config(config_path)
        self.results = []
        self.benchmarks_path = Path("benchmarks")
        self.results_path = Path("results")
        
        # Initialize tool runners
        self.tool_runners = {
            "cbmc": CBMCRunner(),
            "framac_value": FramaCValueRunner(),
            "framac_wp": FramaCWPRunner(),
            "eacsl": EACSLRunner()
        }
        
        # Benchmark to tool mapping
        self.benchmark_mapping = {
            "buffer_overflow.c": ["cbmc", "eacsl"],
            "null_pointer.c": ["cbmc", "framac_value"],
            "arithmetic_safety.c": ["cbmc", "framac_value", "eacsl"],
            "resource_usage.c": ["framac_value"],
            "functional_correctness.c": ["framac_wp", "eacsl"],
            "concurrency_safety.c": ["cbmc", "eacsl"],
            "cruise_control.c": ["framac_wp", "cbmc", "framac_value"]
        }
    
    def load_config(self, config_path):
        """Load experiment configuration"""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def setup_environment(self):
        """Setup the experimental environment"""
        print("🚀 Setting up experimental environment...")
        
        # Create directories
        self.results_path.mkdir(exist_ok=True)
        (self.results_path / "raw").mkdir(exist_ok=True)
        (self.results_path / "processed").mkdir(exist_ok=True)
        
        # Generate benchmarks
        generator = BenchmarkGenerator()
        generator.generate_all_benchmarks()
        
        print("✅ Environment setup complete!")
    
    def run_all_experiments(self):
        """Run all experiments"""
        print("🔬 Starting experimental runs...")
        
        all_benchmarks = []
        for category in ["memory_safety", "arithmetic", "resource", "functional", "advanced"]:
            category_path = self.benchmarks_path / category
            if category_path.exists():
                all_benchmarks.extend(list(category_path.glob("*.c")))
        
        total_experiments = sum(len(self.benchmark_mapping.get(b.name, [])) for b in all_benchmarks)
        completed = 0
        
        for benchmark in all_benchmarks:
            tools = self.benchmark_mapping.get(benchmark.name, [])
            
            for tool_name in tools:
                completed += 1
                print(f"📊 Running {tool_name} on {benchmark.name} ({completed}/{total_experiments})")
                
                try:
                    runner = self.tool_runners[tool_name]
                    result = runner.run_verification(
                        benchmark, 
                        self.results_path / "raw"
                    )
                    
                    self.results.append(result)
                    
                    # Save intermediate results
                    self.save_results()
                    
                except Exception as e:
                    print(f"❌ Error running {tool_name} on {benchmark.name}: {e}")
                    error_result = {
                        "tool": tool_name,
                        "benchmark": benchmark.name,
                        "success": False,
                        "error": str(e),
                        "execution_time": 0,
                        "result": {"status": "ERROR"}
                    }
                    self.results.append(error_result)
        
        print("✅ All experiments completed!")
        return self.results
    
    def save_results(self):
        """Save results to JSON file"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        results_file = self.results_path / "raw" / f"experiment_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Also save to latest file
        latest_file = self.results_path / "raw" / "latest_results.json"
        with open(latest_file, 'w') as f:
            json.dump(self.results, f, indent=2)
    
    def analyze_results(self):
        """Analyze and visualize results"""
        print("📈 Analyzing results...")
        
        analyzer = ResultsAnalyzer(self.results_path / "raw" / "latest_results.json")
        analyzer.generate_comprehensive_analysis()
        
        visualizer = ResultsVisualizer(self.results_path / "raw" / "latest_results.json")
        visualizer.generate_all_visualizations()
        
        print("✅ Analysis complete! Check results/processed/ for outputs.")

def main():
    """Main execution function"""
    print("=" * 60)
    print("      SAFETY-CRITICAL VERIFICATION EXPERIMENTAL SETUP")
    print("=" * 60)
    
    runner = ExperimentRunner()
    
    # Step 1: Setup environment
    runner.setup_environment()
    
    # Step 2: Run experiments
    results = runner.run_all_experiments()
    
    # Step 3: Analyze results
    runner.analyze_results()
    
    print("🎉 Experimental pipeline completed successfully!")
    print(f"📁 Results saved in: {runner.results_path}")

if __name__ == "__main__":
    main()