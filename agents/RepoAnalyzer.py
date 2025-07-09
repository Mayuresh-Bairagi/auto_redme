import os

class RepoAnalyzer:
    def __init__ (self):
        self.repo_path = r'cloned_repos'
    
    def analyze_repo(self):
        try : 
            file_structure = {}
            tech_stack = set()
            important_files = []
            environment_files = []

            for root, dirs, files in os.walk(self.repo_path):
                relative_root = os.path.relpath(root, self.repo_path)
                file_structure[relative_root] = files

                for file in files:
                    file_lower = file.lower()

                    if file_lower.endswith('.py'):
                        tech_stack.add('Python')
                    if file_lower.endswith('.js'):
                        tech_stack.add('JavaScript')
                    if file_lower.endswith('.java'):
                        tech_stack.add('Java')
                    if file_lower.endswith('.html'):
                        tech_stack.add('HTML/CSS')
                    if file_lower.endswith('.json'):
                        tech_stack.add('JSON')
                    if file_lower in ['app.py', 'main.py', 'server.js', 'index.js', 'manage.py', 'setup.py', 'requirements.txt', 'package.json', 'pyproject.toml', 'docker-compose.yml']:
                        important_files.append(os.path.join(root, file))
                    
                    if file_lower in ['.env', '.env.example', 'docker-compose.yml', 'Makefile']:
                        environment_files.append(os.path.join(root, file))
                
            analysis = {
                'file_structure': file_structure,
                'tech_stack': list(tech_stack),
                'important_files': important_files,
                'environment_files': environment_files
            }
            return analysis
        except FileNotFoundError:
            print(f"Repository path {self.repo_path} does not exist.")
            return None