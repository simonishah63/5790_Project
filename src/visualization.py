#!/usr/bin/env python3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
import json

class ResultsVisualizer:
    def __init__(self, results_file):
        self.results_file = Path(results_file)
        self.df = self.load_results()
        self.setup_plotting()
    
    def setup_plotting(self):
        """Setup matplotlib styling"""
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        self.fig_size = (12, 8)
    
    def load_results(self):
        """Load results from JSON file"""
        with open(self.results_file, 'r') as f:
            results = json.load(f)
        return pd.json_normalize(results)
    
    def generate_all_visualizations(self):
        """Generate all visualizations"""
        print("📊 Generating visualizations...")
        
        self.plot_performance_comparison()
        self.plot_effectiveness_comparison()
        self.plot_success_rates()
        self.plot_tool_benchmark_heatmap()
        self.plot_radar_chart_comparison()
        
        print("✅ Visualizations generated in results/processed/")
    
    def plot_performance_comparison(self):
        """Plot performance comparison across tools"""
        fig, axes = plt.subplots(2, 2, figsize=self.fig_size)
        
        # Execution time box plot
        if not self.df.empty:
            sns.boxplot(data=self.df, x='tool', y='execution_time', ax=axes[0,0])
            axes[0,0].set_title('Execution Time Distribution by Tool')
            axes[0,0].set_ylabel('Time (seconds)')
            axes[0,0].tick_params(axis='x', rotation=45)
        else:
            axes[0,0].text(0.5, 0.5, "No data available", ha='center', va='center')
            axes[0,0].set_axis_off()
        
        # Success rate bar plot
        if 'success' in self.df.columns and not self.df.empty:
            success_rates = self.df.groupby('tool')['success'].mean()
            if not success_rates.empty:
                success_rates.plot(kind='bar', ax=axes[0,1], color='skyblue')
                axes[0,1].set_title('Success Rate by Tool')
                axes[0,1].set_ylabel('Success Rate')
                axes[0,1].tick_params(axis='x', rotation=45)
            else:
                axes[0,1].text(0.5, 0.5, "No data available", ha='center', va='center')
                axes[0,1].set_axis_off()
        else:
            axes[0,1].set_axis_off()
        
        # Timeout analysis
        timeout_data = self.df[self.df['execution_time'] >= 299]
        timeout_counts = timeout_data['tool'].value_counts()
        if not timeout_counts.empty:
            timeout_counts.plot(kind='bar', ax=axes[1,0], color='red')
            axes[1,0].set_title('Timeout Count by Tool')
            axes[1,0].set_ylabel('Number of Timeouts')
            axes[1,0].tick_params(axis='x', rotation=45)
        else:
            axes[1,0].text(0.5, 0.5, "No timeouts detected", ha='center', va='center')
            axes[1,0].set_axis_off()
        
        # Performance by benchmark category
        if not self.df.empty:
            self.df['benchmark_category'] = self.df['benchmark'].apply(self.categorize_benchmark)
            category_performance = self.df.groupby(['tool', 'benchmark_category'])['execution_time'].mean().unstack()
            if not category_performance.empty:
                category_performance.plot(kind='bar', ax=axes[1,1])
                axes[1,1].set_title('Average Time by Tool and Benchmark Category')
                axes[1,1].set_ylabel('Time (seconds)')
                axes[1,1].tick_params(axis='x', rotation=45)
                axes[1,1].legend(title='Category')
            else:
                axes[1,1].text(0.5, 0.5, "No data available", ha='center', va='center')
                axes[1,1].set_axis_off()
        else:
            axes[1,1].set_axis_off()
        
        plt.tight_layout()
        Path("results/processed").mkdir(exist_ok=True)
        plt.savefig('results/processed/performance_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_effectiveness_comparison(self):
        """Plot effectiveness comparison across tools"""
        fig, axes = plt.subplots(2, 2, figsize=self.fig_size)
        
        # Bugs detected
        if 'bugs_detected' in self.df.columns and not self.df.empty:
            bug_data = self.df.groupby('tool')['bugs_detected'].mean()
            if not bug_data.empty:
                bug_data.plot(kind='bar', ax=axes[0,0], color='orange')
                axes[0,0].set_title('Average Bugs Detected by Tool')
                axes[0,0].set_ylabel('Bugs Detected')
                axes[0,0].tick_params(axis='x', rotation=45)
            else:
                axes[0,0].set_axis_off()
        else:
            axes[0,0].set_axis_off()
        
        # Properties verified
        if 'properties_verified' in self.df.columns and not self.df.empty:
            prop_data = self.df.groupby('tool')['properties_verified'].mean()
            if not prop_data.empty:
                prop_data.plot(kind='bar', ax=axes[0,1], color='green')
                axes[0,1].set_title('Average Properties Verified by Tool')
                axes[0,1].set_ylabel('Properties Verified')
                axes[0,1].tick_params(axis='x', rotation=45)
            else:
                axes[0,1].set_axis_off()
        else:
            axes[0,1].set_axis_off()
        
        # Alarms generated
        if 'alarms_generated' in self.df.columns and not self.df.empty:
            alarm_data = self.df.groupby('tool')['alarms_generated'].mean()
            if not alarm_data.empty:
                alarm_data.plot(kind='bar', ax=axes[1,0], color='red')
                axes[1,0].set_title('Average Alarms Generated by Tool')
                axes[1,0].set_ylabel('Alarms Generated')
                axes[1,0].tick_params(axis='x', rotation=45)
            else:
                axes[1,0].set_axis_off()
        else:
            axes[1,0].set_axis_off()
        
        # Combined effectiveness score
        effectiveness_metrics = []
        for tool in self.df['tool'].unique():
            tool_data = self.df[self.df['tool'] == tool]
            score = 0
            if 'bugs_detected' in tool_data.columns:
                score += tool_data['bugs_detected'].mean()
            if 'properties_verified' in tool_data.columns:
                score += tool_data['properties_verified'].mean()
            effectiveness_metrics.append({'tool': tool, 'effectiveness_score': score})
        
        effectiveness_df = pd.DataFrame(effectiveness_metrics)
        if not effectiveness_df.empty:
            effectiveness_df.plot(x='tool', y='effectiveness_score', kind='bar', ax=axes[1,1], color='purple')
            axes[1,1].set_title('Combined Effectiveness Score by Tool')
            axes[1,1].set_ylabel('Effectiveness Score')
            axes[1,1].tick_params(axis='x', rotation=45)
        else:
            axes[1,1].set_axis_off()
        
        plt.tight_layout()
        plt.savefig('results/processed/effectiveness_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_success_rates(self):
        """Plot detailed success rate analysis"""
        fig, ax = plt.subplots(figsize=self.fig_size)
        
        if 'success' in self.df.columns and not self.df.empty:
            self.df['success_numeric'] = self.df['success'].apply(lambda x: 1 if x else 0)
            success_pivot = self.df.pivot_table(
                index='benchmark', 
                columns='tool', 
                values='success_numeric', 
                aggfunc='mean'
            )
            if not success_pivot.empty:
                sns.heatmap(success_pivot, annot=True, fmt=".2f", cmap='RdYlGn', center=0.5, ax=ax)
                ax.set_title('Success Rate by Tool and Benchmark')
                ax.set_ylabel('Benchmark')
                ax.set_xlabel('Tool')
            else:
                ax.text(0.5, 0.5, "No success data", ha='center', va='center')
                ax.set_axis_off()
        else:
            ax.text(0.5, 0.5, "No success column or data", ha='center', va='center')
            ax.set_axis_off()
        
        plt.tight_layout()
        plt.savefig('results/processed/success_rate_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_tool_benchmark_heatmap(self):
        """Plot tool-benchmark compatibility heatmap"""
        fig, ax = plt.subplots(figsize=self.fig_size)
        
        if self.df.empty or 'tool' not in self.df.columns or 'benchmark' not in self.df.columns or 'success' not in self.df.columns:
            ax.text(0.5, 0.5, "No compatibility data", ha='center', va='center')
            ax.set_axis_off()
        else:
            # Convert success boolean to numeric (0 or 1 float)
            self.df['compatibility'] = self.df['success'].apply(lambda x: 1.0 if x else 0.0)
            pivot_table = self.df.pivot_table(
                index='benchmark',
                columns='tool',
                values='compatibility',
                aggfunc='first'  # use first occurrence
            )

            if not pivot_table.empty:
                # Use float format for annotation
                sns.heatmap(pivot_table, annot=True, fmt=".0f", cmap='RdYlGn', center=0.5, ax=ax)
                ax.set_title('Tool-Benchmark Compatibility Matrix')
                ax.set_ylabel('Benchmark')
                ax.set_xlabel('Tool')
            else:
                ax.text(0.5, 0.5, "No compatibility data", ha='center', va='center')
                ax.set_axis_off()

        plt.tight_layout()
        plt.savefig('results/processed/tool_benchmark_compatibility.png', dpi=300, bbox_inches='tight')
        plt.close()

    
    def plot_radar_chart_comparison(self):
        """Plot radar chart for multi-dimensional comparison"""
        metrics = ['success_rate', 'performance', 'bug_detection']
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False)
        
        for tool in self.df['tool'].unique():
            tool_data = self.df[self.df['tool'] == tool]
            if not tool_data.empty:
                values = [
                    tool_data['success'].mean() if 'success' in tool_data.columns else 0,
                    1 / (tool_data['execution_time'].mean() + 1) if 'execution_time' in tool_data.columns else 0,
                    tool_data['bugs_detected'].mean()/10 if 'bugs_detected' in tool_data.columns else 0
                ]
                values += values[:1]  # Complete the circle
                tool_angles = np.concatenate((angles, [angles[0]]))
                ax.plot(tool_angles, values, 'o-', linewidth=2, label=tool)
                ax.fill(tool_angles, values, alpha=0.1)
        
        ax.set_xticks(angles)
        ax.set_xticklabels(metrics)
        ax.set_title('Multi-dimensional Tool Comparison')
        ax.legend(loc='upper right')
        
        plt.tight_layout()
        plt.savefig('results/processed/radar_chart_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def categorize_benchmark(self, benchmark_name):
        """Categorize benchmark by type"""
        if 'buffer' in benchmark_name or 'null' in benchmark_name:
            return 'Memory Safety'
        elif 'arithmetic' in benchmark_name:
            return 'Arithmetic Safety'
        elif 'resource' in benchmark_name:
            return 'Resource Usage'
        elif 'functional' in benchmark_name:
            return 'Functional Correctness'
        elif 'concurrency' in benchmark_name or 'cruise' in benchmark_name:
            return 'Advanced Properties'
        else:
            return 'Other'
