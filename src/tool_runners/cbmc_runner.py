#!/usr/bin/env python3
import subprocess
import json
import time
import re
from pathlib import Path

class CBMCRunner:
    def __init__(self):
        self.tool_name = "cbmc"
        self.container = "cbmc"  # service name in docker-compose.yml
    
    def run_verification(self, benchmark_path, output_dir):
        """Run CBMC from host using Docker Compose"""
        benchmark_path = Path(benchmark_path).resolve()
        output_dir = Path(output_dir).resolve()
        container_benchmark_path = f"/workspace/{benchmark_path.relative_to(Path.cwd())}"
        
        start_time = time.time()
        cmd = [
            "docker", "compose", "run", "--rm", "--platform", "linux/amd64",
            self.container,
            "--json-ui", container_benchmark_path
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
            
            return {
                "tool": self.tool_name,
                "benchmark": benchmark_path.name,
                "success": result.returncode == 0 or "VERIFICATION FAILED" in result.stdout,
                "execution_time": execution_time,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "result": analysis_result,
                "bugs_detected": self.count_bugs_detected(result.stdout),
                "properties_verified": self.count_properties_verified(result.stdout)
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
            "bugs_detected": 0,
            "properties_verified": 0
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
            "bugs_detected": 0,
            "properties_verified": 0
        }
    
    def parse_output(self, result):
        """Parse CBMC JSON output"""
        try:
            if result.stdout.strip():
                return json.loads(result.stdout)
        except:
            pass
        
        # Fallback to text parsing
        output = result.stdout + result.stderr
        
        analysis_result = {
            "status": "UNKNOWN",
            "verification_failed": "VERIFICATION FAILED" in output,
            "verification_successful": "VERIFICATION SUCCESSFUL" in output,
            "errors_found": len(re.findall(r"error|violation", output, re.IGNORECASE)),
            "warnings": len(re.findall(r"warning", output, re.IGNORECASE))
        }
        
        if "VERIFICATION SUCCESSFUL" in output:
            analysis_result["status"] = "SAFE"
        elif "VERIFICATION FAILED" in output:
            analysis_result["status"] = "UNSAFE"
        
        return analysis_result
    
    def count_bugs_detected(self, output):
        """Count number of bugs detected in output"""
        bugs = 0
        bugs += len(re.findall(r"VERIFICATION FAILED", output))
        bugs += len(re.findall(r"array.*out of bounds", output, re.IGNORECASE))
        bugs += len(re.findall(r"pointer.*outside", output, re.IGNORECASE))
        bugs += len(re.findall(r"division by zero", output, re.IGNORECASE))
        bugs += len(re.findall(r"arithmetic overflow", output, re.IGNORECASE))
        return bugs
    
    def count_properties_verified(self, output):
        """Count number of properties verified"""
        return len(re.findall(r"VERIFICATION SUCCESSFUL", output))