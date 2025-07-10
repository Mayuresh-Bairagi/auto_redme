import os
from agents.RepoAnalyzer import RepoAnalyzer
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()

class CodeReader:
    def __init__(self, repo_path: str = 'cloned_repos'):
        try:
            self.repo_analyzer = RepoAnalyzer()
            self.analysis = self.repo_analyzer.analyze_repo()
        except Exception as e:
            print(f"Error initializing CodeReader: {e}")

        try:
            os.environ["GROQ_API_KEY"] = os.getenv("groq_key")
        except Exception as e:
            print(f"Error setting environment variable: {e}")

    def read_code(self):
        try:
            important_files_content = {}
            for file in self.analysis['important_files']:
                file_name = os.path.basename(file)
                with open(file, 'r') as f:
                    important_files_content[file_name] = f.read()
            return important_files_content
        except Exception as e:
            print(f"Error reading code files: {e}")
    
    def get_code_as_string(self):
        try:
            code = ""
            important_files_content = self.read_code()
            for key, value in important_files_content.items():
                code += f"### {key}\n\n"
                code += value + "\n\n"
            return code
        except Exception as e:
            print(f"Error getting code as string: {e}")
            return ""
        
    def summary_code(self):
        try:
            code = self.get_code_as_string()
            llm = ChatGroq(model="llama3-8b-8192")
            system_prompt = """
                You are an expert technical writer and software engineer. I will provide you with a limited code snippet (only ~1000 characters) from the main file of my project. Despite this partial input, your job is to deeply analyze the code structure, logic, and possible project goals. Based on your technical expertise and standard coding practices, write a precise, beginner-friendly, and professional summary for the README file.
                Your summary must explain:
                    - What this project does (main objective).
                    - Core functionalities (key features & logic).
                    - Probable use cases or applications.
                    - Technologies/libraries used (if visible in the snippet).
                If the code snippet is incomplete, fill gaps with logical assumptions but clearly indicate if something is an assumption.
                Don't explain the code line by line.
                Write in a clean, polished, and engaging style — like a good open-source README intro.
                """
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("user", "{code}")
            ])
            response = prompt | llm
            return response.invoke({"code": code}).content
        except Exception as e:
            print(f"Error summarizing code: {e}")
            return "Error summarizing code."
        
    def repoAnalysis(self):
        try:
            return self.analysis
        except Exception as e:
            print(f"Error retrieving repo analysis: {e}")
            return {}