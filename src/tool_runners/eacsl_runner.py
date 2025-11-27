#!/usr/bin/env python3
import subprocess
import time
import re
from pathlib import Path

class EACSLRunner:
    def __init__(self):
        self.tool_name = "eacsl"
        self.container = "framac"  # Docker Compose service name
    
    def run_verification(self, benchmark_path, output_dir):
        """Run E-ACSL from host using Docker Compose"""
        benchmark_path = Path(benchmark_path).resolve()
        output_dir = Path(output_dir).resolve()
        container_benchmark_path = f"/workspace/{benchmark_path.relative_to(Path.cwd())}"
    
        start_time = time.time()
        
        # Run E-ACSL
        cmd = [
            "docker", "compose", "run", "--rm",
            self.container,
            "frama-c", "-e-acsl", container_benchmark_path
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            execution_time = time.time() - start_time
            analysis_result = self.parse_output(result)
            
            instrumented_success = result.returncode == 0
            
            return {
                "tool": self.tool_name,
                "benchmark": benchmark_path.name,
                "success": instrumented_success,
                "execution_time": execution_time,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "result": analysis_result,
                "runtime_checks_inserted": self.count_runtime_checks(result.stdout),
                "instrumentation_success": instrumented_success
            }
            
        except subprocess.TimeoutExpired:
            return self._create_timeout_result(benchmark_path.name)
        except Exception as e:
            return self._create_error_result(benchmark_path.name, str(e))
    
    def _create_timeout_result(self, benchmark_name):
        return {
            "tool": self.tool_name,
            "benchmark": benchmark_name,
            "success": False,
            "execution_time": 300,
            "return_code": -1,
            "stdout": "",
            "stderr": "Timeout after 300 seconds",
            "result": {"status": "TIMEOUT"},
            "runtime_checks_inserted": 0,
            "instrumentation_success": False
        }
    
    def _create_error_result(self, benchmark_name, error_msg):
        return {
            "tool": self.tool_name,
            "benchmark": benchmark_name,
            "success": False,
            "execution_time": 0,
            "return_code": -1,
            "stdout": "",
            "stderr": f"Error: {error_msg}",
            "result": {"status": "ERROR"},
            "runtime_checks_inserted": 0,
            "instrumentation_success": False
        }
    
    def count_runtime_checks(self, output):
        """Count number of runtime checks inserted"""
        return len(re.findall(r"assertion|check|instrumented", output, re.IGNORECASE))
    
    def parse_output(self, result):
        """Parse E-ACSL output"""
        output = result.stdout
        
        return {
            "status": "COMPLETED",
            "instrumentation_details": self.extract_instrumentation_details(output)
        }
    
    def extract_instrumentation_details(self, output):
        """Extract instrumentation details from output"""
        details = {}
        for line in output.splitlines():
            if 'instrumented' in line.lower():
                details['instrumentation_line'] = line.strip()
            if 'assertion' in line.lower():
                details['assertions_found'] = line.strip()
        return details