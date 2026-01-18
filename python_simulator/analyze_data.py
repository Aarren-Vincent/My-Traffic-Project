"""
Data Analyzer for RTOS Traffic System
Generates reports and visualizations from logged data
"""
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime
import os

class TrafficDataAnalyzer:
    def __init__(self, log_file="traffic_log.csv"):
        self.log_file = log_file
        self.df = None
        
    def load_data(self):
        """Load data from CSV log file"""
        if not os.path.exists(self.log_file):
            print(f"Error: Log file '{self.log_file}' not found!")
            return False
            
        self.df = pd.read_csv(self.log_file)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        print(f"Loaded {len(self.df)} records from {self.log_file}")
        return True
    
    def generate_summary_report(self):
        """Generate a comprehensive summary report"""
        if self.df is None:
            print("No data loaded!")
            return
            
        print("\n" + "="*70)
        print("RTOS TRAFFIC SYSTEM - PERFORMANCE REPORT")
        print("="*70)
        
        # System Overview
        start_time = self.df['timestamp'].min()
        end_time = self.df['timestamp'].max()
        duration = (end_time - start_time).total_seconds() / 60  # Minutes
        
        print(f"\n📊 SYSTEM OVERVIEW")
        print(f"   Period: {start_time.strftime('%Y-%m-%d %H:%M:%S')} to {end_time.strftime('%H:%M:%S')}")
        print(f"   Duration: {duration:.1f} minutes")
        print(f"   Total Events: {len(self.df)}")
        
        # Emergency Response Analysis
        emergency_events = self.df[self.df['event_type'] == 'EMERGENCY_ACTIVATED']
        if not emergency_events.empty:
            print(f"\n🚑 EMERGENCY RESPONSE ANALYSIS")
            print(f"   Total Emergencies: {len(emergency_events)}")
            
            # Response times
            response_times = emergency_events['response_time_ms'].dropna()
            if not response_times.empty:
                print(f"   Average Response: {response_times.mean():.1f} ms")
                print(f"   Minimum Response: {response_times.min():.1f} ms")
                print(f"   Maximum Response: {response_times.max():.1f} ms")
                
                # Deadline compliance
                deadline_misses = len(response_times[response_times > 500])
                print(f"   Deadline Misses: {deadline_misses} ({deadline_misses/len(response_times)*100:.1f}%)")
        
        # Traffic Pattern Analysis
        print(f"\n🚦 TRAFFIC PATTERNS")
        for light_state in ['GREEN', 'RED', 'YELLOW']:
            count = len(self.df[self.df['lights_NS'] == light_state])
            percentage = count / len(self.df) * 100
            print(f"   NS Light {light_state}: {percentage:.1f}% of time")
        
        # Weather Impact
        if 'weather' in self.df.columns:
            print(f"\n🌤️ WEATHER IMPACT")
            for weather in self.df['weather'].unique():
                weather_data = self.df[self.df['weather'] == weather]
                if len(weather_data) > 0:
                    avg_wait = weather_data['avg_wait_time'].mean()
                    print(f"   {weather}: Avg wait {avg_wait:.1f}s ({len(weather_data)} samples)")
        
        # Task State Analysis
        print(f"\n⚡ RTOS TASK ANALYSIS")
        task_states = {}
        for _, row in self.df.iterrows():
            try:
                states = json.loads(row['task_states'])
                for task, state in states.items():
                    if task not in task_states:
                        task_states[task] = {}
                    if state not in task_states[task]:
                        task_states[task][state] = 0
                    task_states[task][state] += 1
            except:
                pass
        
        for task, states in task_states.items():
            total = sum(states.values())
            print(f"   {task}:")
            for state, count in states.items():
                percentage = count / total * 100
                print(f"     {state}: {percentage:.1f}%")
    
    def create_visualizations(self, output_dir="reports"):
        """Create visualization charts"""
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Emergency Response Times
        emergency_data = self.df[self.df['event_type'] == 'EMERGENCY_ACTIVATED']
        if not emergency_data.empty:
            plt.figure(figsize=(10, 6))
            plt.plot(emergency_data['timestamp'], emergency_data['response_time_ms'], 'ro-')
            plt.axhline(y=500, color='r', linestyle='--', label='500ms Deadline')
            plt.xlabel('Time')
            plt.ylabel('Response Time (ms)')
            plt.title('Emergency Response Times')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(f"{output_dir}/emergency_response.png")
            plt.close()
        
        # 2. Traffic Light State Distribution
        plt.figure(figsize=(8, 6))
        light_states = self.df['lights_NS'].value_counts()
        plt.pie(light_states.values, labels=light_states.index, autopct='%1.1f%%')
        plt.title('North-South Traffic Light State Distribution')
        plt.savefig(f"{output_dir}/light_distribution.png")
        plt.close()
        
        # 3. Wait Times Over Time
        if 'avg_wait_time' in self.df.columns:
            plt.figure(figsize=(12, 6))
            plt.plot(self.df['timestamp'], self.df['avg_wait_time'], 'b-', alpha=0.7)
            plt.xlabel('Time')
            plt.ylabel('Average Wait Time (seconds)')
            plt.title('Vehicle Wait Times Over Time')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(f"{output_dir}/wait_times.png")
            plt.close()
        
        print(f"\n📈 Visualizations saved to '{output_dir}/' folder")
    
    def export_report(self, output_file="traffic_report.txt"):
        """Export report to text file"""
        import sys
        from io import StringIO
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        self.generate_summary_report()
        
        report_text = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        # Write to file
        with open(output_file, 'w') as f:
            f.write(report_text)
        
        print(f"📄 Report exported to: {output_file}")

if __name__ == "__main__":
    analyzer = TrafficDataAnalyzer()
    
    if analyzer.load_data():
        analyzer.generate_summary_report()
        analyzer.create_visualizations()
        analyzer.export_report()
        
        print("\n" + "="*70)
        print("ANALYSIS COMPLETE!")
        print("="*70)
        print("\nGenerated files:")
        print("• traffic_report.txt - Text summary")
        print("• reports/emergency_response.png - Response time chart")
        print("• reports/light_distribution.png - Light state pie chart")
        print("• reports/wait_times.png - Wait time trend")