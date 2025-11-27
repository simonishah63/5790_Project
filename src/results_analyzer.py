#!/usr/bin/env python3
import json
import pandas as pd
import numpy as np
from pathlib import Path

class ResultsAnalyzer:
    def __init__(self, results_file):
        self.results_file = Path(results_file)
        self.df = self.load_results()
    
    def load_results(self):
        """Load results from JSON file"""
        with open(self.results_file, 'r') as f:
            results = json.load(f)
        
        # Convert to DataFrame
        df = pd.json_normalize(results)
        return df
    
    def generate_comprehensive_analysis(self):
        """Generate comprehensive analysis of results"""
        print("📊 Generating comprehensive analysis...")
        
        analysis = {
            "summary": self.generate_summary(),
            "performance_comparison": self.performance_analysis(),
            "effectiveness_comparison": self.effectiveness_analysis(),
            "tool_recommendations": self.generate_recommendations()
        }
        
        # Save analysis
        output_dir = Path("results/processed")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "comprehensive_analysis.json"
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        # Generate CSV reports
        self.generate_csv_reports(output_dir)
        
        return analysis
    
    def generate_summary(self):
        """Generate summary statistics"""
        total_experiments = len(self.df)
        successful_runs = len(self.df[self.df.get('success', False) == True])
        failed_runs = len(self.df[self.df.get('success', False) == False])
        
        summary = {
            "total_experiments": total_experiments,
            "successful_runs": successful_runs,
            "failed_runs": failed_runs,
            "tools_tested": self.df['tool'].unique().tolist() if 'tool' in self.df else [],
            "benchmarks_tested": self.df['benchmark'].unique().tolist() if 'benchmark' in self.df else [],
            "average_execution_time": self.df['execution_time'].mean() if 'execution_time' in self.df else 0,
            "total_execution_time": self.df['execution_time'].sum() if 'execution_time' in self.df else 0,
        }
        
        # Tool-specific summaries
        tool_summary = {}
        if 'tool' in self.df:
            for tool in self.df['tool'].unique():
                tool_data = self.df[self.df['tool'] == tool]
                tool_summary[tool] = {
                    "runs": len(tool_data),
                    "success_rate": len(tool_data[tool_data.get('success', False) == True]) / max(len(tool_data), 1),
                    "avg_time": tool_data['execution_time'].mean() if 'execution_time' in tool_data else 0,
                    "total_bugs_detected": tool_data['bugs_detected'].sum() if 'bugs_detected' in tool_data else 0
                }
        summary['tool_performance'] = tool_summary
        return summary
    
    def performance_analysis(self):
        """Analyze performance metrics"""
        performance = {}
        if 'tool' not in self.df or 'execution_time' not in self.df:
            return performance
        
        for tool in self.df['tool'].unique():
            tool_data = self.df[self.df['tool'] == tool]
            execution_times = tool_data['execution_time']
            performance[tool] = {
                "mean_execution_time": execution_times.mean(),
                "median_execution_time": execution_times.median(),
                "std_execution_time": execution_times.std(),
                "min_execution_time": execution_times.min(),
                "max_execution_time": execution_times.max(),
                "timeout_count": len(tool_data[execution_times >= 299])
            }
        return performance
    
    def effectiveness_analysis(self):
        """Analyze effectiveness metrics"""
        effectiveness = {}
        if 'tool' not in self.df:
            return effectiveness
        
        for tool in self.df['tool'].unique():
            tool_data = self.df[self.df['tool'] == tool]
            effectiveness[tool] = {
                "success_rate": len(tool_data[tool_data.get('success', False) == True]) / max(len(tool_data), 1),
                "bugs_detected_avg": tool_data['bugs_detected'].mean() if 'bugs_detected' in tool_data else 0,
                "properties_verified_avg": tool_data['properties_verified'].mean() if 'properties_verified' in tool_data else 0,
                "alarms_generated_avg": tool_data['alarms_generated'].mean() if 'alarms_generated' in tool_data else 0
            }
        return effectiveness
    
    def generate_recommendations(self):
        """Generate tool recommendations based on analysis"""
        recommendations = {}
        performance_data = self.performance_analysis()
        effectiveness_data = self.effectiveness_analysis()
        
        if performance_data:
            recommendations["fastest_tool"] = min(performance_data.items(), key=lambda x: x[1]["mean_execution_time"])[0]
        if effectiveness_data:
            recommendations["most_effective_bug_finder"] = max(effectiveness_data.items(), key=lambda x: x[1]["bugs_detected_avg"])[0]
            recommendations["best_for_proofs"] = max(effectiveness_data.items(), key=lambda x: x[1]["properties_verified_avg"])[0]
        
        # Property-specific recommendations
        property_recommendations = {}
        if 'benchmark' in self.df and 'success' in self.df:
            for benchmark in self.df['benchmark'].unique():
                bench_data = self.df[self.df['benchmark'] == benchmark]
                if not bench_data.empty:
                    best_tool = bench_data.loc[bench_data['success'].idxmax(), 'tool']
                    property_recommendations[benchmark] = best_tool
        recommendations["property_specific"] = property_recommendations
        return recommendations
    
    def generate_csv_reports(self, output_dir):
        """Generate CSV reports for detailed analysis"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Main results CSV
        self.df.to_csv(output_dir / "experiment_results.csv", index=False)
        
        # Performance comparison CSV
        performance_data = []
        if 'tool' in self.df:
            for tool in self.df['tool'].unique():
                tool_data = self.df[self.df['tool'] == tool]
                performance_data.append({
                    'tool': tool,
                    'mean_time': tool_data['execution_time'].mean() if 'execution_time' in tool_data else 0,
                    'success_rate': len(tool_data[tool_data.get('success', False) == True]) / max(len(tool_data), 1),
                    'total_runs': len(tool_data)
                })
        performance_df = pd.DataFrame(performance_data)
        performance_df.to_csv(output_dir / "performance_comparison.csv", index=False)
