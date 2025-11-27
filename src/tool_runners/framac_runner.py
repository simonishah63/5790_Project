#!/usr/bin/env python3
import subprocess
import time
import re
from pathlib import Path

class FramaCValueRunner:
    def __init__(self):
        self.tool_name = "framac_value"
        self.container = "framac"
    
    def run_verification(self, benchmark_path, output_dir):
        """Run Frama-C Value Analysis on a benchmark"""
        benchmark_path = Path(benchmark_path).resolve()
        container_benchmark_path = f"/workspace/{benchmark_path.relative_to(Path.cwd())}"
        start_time = time.time()
        
        # Run Frama-C
        cmd = [
            "docker", "compose", "run", "--rm",
            self.container,
            "frama-c", "-val", "-metrics", container_benchmark_path
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
                "success": result.returncode == 0,
                "execution_time": execution_time,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "result": analysis_result,
                "alarms_generated": self.count_alarms(result.stdout),
                "proofs_established": self.count_proofs(result.stdout)
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
            "alarms_generated": 0,
            "proofs_established": 0
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
            "alarms_generated": 0,
            "proofs_established": 0
        }
    
    def parse_output(self, result):
        """Parse Frama-C Value Analysis output"""
        output = result.stdout
        
        return {
            "status": "COMPLETED",
            "alarms": self.extract_alarms(output),
            "metrics": self.extract_metrics(output)
        }
    
    def count_alarms(self, output):
        """Count number of alarms generated"""
        return len(re.findall(r"assertion|alarm", output, re.IGNORECASE))
    
    def count_proofs(self, output):
        """Count number of proofs established"""
        return len(re.findall(r"valid", output, re.IGNORECASE))
    
    def extract_alarms(self, output):
        """Extract detailed alarm information"""
        alarms = []
        for line in output.split('\n'):
            if 'assertion' in line.lower() or 'alarm' in line.lower():
                alarms.append(line.strip())
        return alarms
    
    def extract_metrics(self, output):
        """Extract metrics from Frama-C output"""
        metrics = {}
        for line in output.split('\n'):
            if ':' in line and any(term in line.lower() for term in ['time', 'memory', 'proof']):
                parts = line.split(':', 1)
                if len(parts) == 2:
                    metrics[parts[0].strip()] = parts[1].strip()
        return metrics

class FramaCWPRunner:
    def __init__(self):
        self.tool_name = "framac_wp"
        self.container = "framac"
    
    def run_verification(self, benchmark_path, output_dir):
        """Run Frama-C WP on a benchmark"""
        benchmark_path = Path(benchmark_path).resolve()
        container_benchmark_path = f"/workspace/{benchmark_path.relative_to(Path.cwd())}"
        start_time = time.time()
        
        # Run Frama-C WP
        cmd = [
            "docker", "compose", "run", "--rm",
            self.container,
            "frama-c", "-wp", "-wp-rte", container_benchmark_path
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
                "success": result.returncode == 0,
                "execution_time": execution_time,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "result": analysis_result,
                "goals_proven": self.count_proven_goals(result.stdout),
                "goals_failed": self.count_failed_goals(result.stdout)
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
            "goals_proven": 0,
            "goals_failed": 0
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
            "goals_proven": 0,
            "goals_failed": 0
        }
    
    def count_proven_goals(self, output):
        """Count number of proven goals"""
        return len(re.findall(r"Proved", output, re.IGNORECASE))
    
    def count_failed_goals(self, output):
        """Count number of failed goals"""
        return len(re.findall(r"Failed", output, re.IGNORECASE))
    
    def parse_output(self, result):
        """Parse Frama-C WP output"""
        output = result.stdout
        
        return {
            "status": "COMPLETED",
            "goals_proven": self.count_proven_goals(output),
            "goals_failed": self.count_failed_goals(output)
        }