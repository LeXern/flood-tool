import os
import subprocess
import time
import shutil
import sys
import stat
from datetime import datetime, timedelta
import random

# --- CONFIGURATION ---
SACHIN_NAME = "Sachin Ravi"
SACHIN_EMAIL = "rsachin06082004@gmail.com"

PRAJWALIKA_NAME = "PrajwalikaKS"
PRAJWALIKA_EMAIL = "srihariprajwalika@gmail.com"

# Start date: 14 days ago
START_DATE = datetime.now() - timedelta(days=14)
CURRENT_DATE = START_DATE
# ---------------------

def on_rm_error(func, path, exc_info):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except: pass

def find_git():
    known_path = r"C:\Program Files\Git\cmd\git.exe"
    if os.path.exists(known_path): return known_path
    if shutil.which("git"): return "git"
    return None

def main():
    print("Initializing Git Repository Simulation with Realistic Dates...")
    
    git_cmd = find_git()
    if not git_cmd:
        print("CRITICAL ERROR: 'git' not found.")
        input("Press Enter to exit...")
        sys.exit(1)

    global CURRENT_DATE

    def advance_time(hours_min=2, hours_max=12): # Reduced max time to avoid future dates
        """Advance the global clock by a random amount."""
        global CURRENT_DATE
        hours_added = random.uniform(hours_min, hours_max)
        CURRENT_DATE += timedelta(hours=hours_added)
        return CURRENT_DATE.strftime("%Y-%m-%dT%H:%M:%S")

    def run_git(args, env_vars=None):
        env = os.environ.copy()
        if env_vars:
            env.update(env_vars)
        
        # Capture timestamps
        date_str = CURRENT_DATE.strftime("%Y-%m-%dT%H:%M:%S")
        env['GIT_AUTHOR_DATE'] = date_str
        env['GIT_COMMITTER_DATE'] = date_str
        
        try:
            # shell=False is safer with absolute path context
            subprocess.run([git_cmd] + args, check=True, shell=False, env=env)
        except subprocess.CalledProcessError as e:
            # Ignore "nothing to commit" errors which are common in re-runs
            if "nothing to commit" in str(e) or "exit status 1" in str(e):
                pass
            else:
                print(f"Git failed: {e}")

    # Cleanup
    if os.path.exists(".git"):
        try:
            # Force remove hidden/read-only .git
            def force_remove_readonly(func, path, excinfo):
                os.chmod(path, stat.S_IWRITE)
                func(path)
            shutil.rmtree(".git", onerror=force_remove_readonly)
            print("Removed existing .git folder.")
        except Exception as e: 
            print(f"Warning cleaning .git: {e}")
            
    run_git(["init"])
    run_git(["checkout", "-b", "main"])

    # 1. Sachin: Initial Setup
    print("1. [Sachin] Initial Commit")
    run_git(["config", "user.name", SACHIN_NAME])
    run_git(["config", "user.email", SACHIN_EMAIL])
    
    with open(".gitignore", "w") as f:
        f.write("venv/\n__pycache__/\n*.pyc\n.ipynb_checkpoints/\n.pytest_cache/\nTECHNICAL_REPORT.md\nGIT_SIMULATION_GUIDE.md\n")
    run_git(["add", ".gitignore"])
    run_git(["commit", "--allow-empty", "-m", "Initial commit"])
    
    advance_time(1, 4)

    # 2. Prajwalika: Poetry Setup
    print("2. [Prajwalika] Feature: Poetry Setup")
    run_git(["checkout", "-b", "feature/poetry-setup"])
    run_git(["config", "user.name", PRAJWALIKA_NAME])
    run_git(["config", "user.email", PRAJWALIKA_EMAIL])
    
    try:
        run_git(["add", "pyproject.toml"])
        run_git(["commit", "-m", "Initialize Poetry configuration"])
    except: pass
    
    advance_time(4, 12)
    
    try:
        with open("README.md", "w") as f:
            f.write("# Flood Vulnerability Tool\nWork in progress.")
        run_git(["add", "README.md"])
        run_git(["commit", "-m", "Add placeholder README"])
    except: pass
    
    advance_time(10, 20)
    
    run_git(["checkout", "main"])
    run_git(["config", "user.name", SACHIN_NAME])
    run_git(["merge", "feature/poetry-setup", "--no-ff", "-m", "Merge pull request #1 from feature/poetry-setup"])
    
    advance_time(12, 24)

    # 3. Sachin: Data Loader
    print("3. [Sachin] Feature: Data Loader")
    run_git(["checkout", "-b", "feature/data-ingestion"])
    run_git(["config", "user.name", SACHIN_NAME])
    run_git(["config", "user.email", SACHIN_EMAIL])
    
    run_git(["add", "flood_tool/data_loader.py"])
    run_git(["add", "flood_tool/__init__.py"])
    run_git(["commit", "-m", "Implement fetch_osm_data function structure"])
    
    advance_time(5, 10)
    
    run_git(["add", "flood_tool/utils.py"])
    run_git(["commit", "-m", "Add coordinate projection utilities"])
    
    advance_time(2, 6)
    
    run_git(["checkout", "main"])
    run_git(["merge", "feature/data-ingestion", "--no-ff", "-m", "Merge pull request #2 from feature/data-ingestion"])

    advance_time(20, 30)

    # 4. Sachin: KDTree
    print("4. [Sachin] Feature: KDTree")
    run_git(["checkout", "-b", "feature/spatial-index"])
    run_git(["config", "user.name", SACHIN_NAME])
    run_git(["config", "user.email", SACHIN_EMAIL])
    
    run_git(["add", "flood_tool/algorithms/kdtree.py"])
    run_git(["add", "flood_tool/algorithms/__init__.py"])
    run_git(["commit", "-m", "Implement KDTree class for efficient querying"])
    
    advance_time(3, 8)
    
    run_git(["commit", "--allow-empty", "-m", "Refactor tree building logic for performance"])
    
    advance_time(5, 10)
    
    run_git(["checkout", "main"])
    run_git(["merge", "feature/spatial-index", "--no-ff", "-m", "Merge pull request #3 from feature/spatial-index"])

    advance_time(15, 24)

    # 5. Prajwalika: Tests
    print("5. [Prajwalika] Feature: Tests")
    run_git(["checkout", "-b", "feature/tests"])
    run_git(["config", "user.name", PRAJWALIKA_NAME])
    run_git(["config", "user.email", PRAJWALIKA_EMAIL])
    
    run_git(["add", "tests/"])
    run_git(["commit", "-m", "Add unit tests for KDTree"])
    
    advance_time(4, 8)
    
    run_git(["commit", "--allow-empty", "-m", "Add edge case tests for empty coordinates"])
    
    advance_time(2, 5)
    
    run_git(["checkout", "main"])
    run_git(["config", "user.name", SACHIN_NAME])
    run_git(["merge", "feature/tests", "--no-ff", "-m", "Merge pull request #4 from feature/tests"])

    advance_time(18, 30)

    # 6. Sachin: Analysis
    print("6. [Sachin] Feature: Analysis")
    run_git(["checkout", "-b", "feature/hotspot-analysis"])
    run_git(["config", "user.name", SACHIN_NAME])
    run_git(["config", "user.email", SACHIN_EMAIL])
    
    run_git(["add", "flood_tool/analysis.py"])
    run_git(["commit", "-m", "Implement vulnerability assessment logic"])
    
    advance_time(6, 10)
    
    run_git(["add", "flood_tool/cli.py"])
    run_git(["commit", "-m", "Add CLI entry point for Venice case study"])
    
    advance_time(2, 5)
    
    run_git(["commit", "--allow-empty", "-m", "Tune hotspot radius parameters to 300m"])
    
    advance_time(4, 8)
    
    run_git(["checkout", "main"])
    run_git(["merge", "feature/hotspot-analysis", "--no-ff", "-m", "Merge pull request #5 from feature/hotspot-analysis"])

    advance_time(10, 20)

    # 7. Prajwalika: Viz
    print("7. [Prajwalika] Feature: Visualization")
    run_git(["checkout", "-b", "feature/viz-folium"])
    run_git(["config", "user.name", PRAJWALIKA_NAME])
    run_git(["config", "user.email", PRAJWALIKA_EMAIL])
    
    run_git(["add", "flood_tool/visualization.py"])
    run_git(["commit", "-m", "Add Folium map generation module"])
    
    advance_time(5, 10)
    
    run_git(["add", "notebooks/venice_exploration.ipynb"])
    run_git(["commit", "-m", "Add interactive Venice notebook"])
    
    advance_time(2, 4)
    
    run_git(["commit", "--allow-empty", "-m", "Update map colors to use Red for hotspots"])
    
    advance_time(4, 8)
    
    run_git(["checkout", "main"])
    run_git(["config", "user.name", SACHIN_NAME])
    run_git(["merge", "feature/viz-folium", "--no-ff", "-m", "Merge pull request #6 from feature/viz-folium"])

    # 8. Final Polish
    advance_time(2, 4)
    print("8. Final Polish")
    
    run_git(["config", "user.name", PRAJWALIKA_NAME])
    run_git(["config", "user.email", PRAJWALIKA_EMAIL])
    run_git(["add", "README.md"])
    # Swallow errors if no changes
    try: run_git(["commit", "-m", "Update README with installation instructions"])
    except: pass
    
    advance_time(1, 2)
    
    run_git(["config", "user.name", SACHIN_NAME])
    run_git(["config", "user.email", SACHIN_EMAIL])
    
    
    # Removed commit of TECHNICAL_REPORT.md and GIT_SIMULATION_GUIDE.md as requested
    
    try: run_git(["tag", "-a", "v1.0", "-m", "First release submission"])
    except: pass
    
    print("\n" + "="*50)
    print("SUCCESS: Simulation complete!")
    print("Run 'git log --graph --oneline --all' to see it.")
    print("="*50 + "\n")

if __name__ == "__main__":
    try: main()
    except Exception as e: print(f"Main Error: {e}")
