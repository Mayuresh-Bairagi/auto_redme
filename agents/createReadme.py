from agents.CodeReader import CodeReader
from agents.clone_github import CloneGitHubRepo
from fastapi import HTTPException
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os

class ReadmeGenerator:
    def __init__(self,github_url: str):
        try :
            self.clone_dir = "cloned_repos"
            self.clone_repo = CloneGitHubRepo(self.clone_dir)
            self.clone_repo.clone_repo(github_url)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error cloning repository: {str(e)}")

        try:
            load_dotenv()
            os.environ["GROQ_API_KEY"] = os.getenv("groq_key")
            self.llm = ChatGroq(model="llama3-8b-8192")
            self.code_reader = CodeReader()
            self.code_summary = self.code_reader.summary_code()  
            self.repo_structure = self.code_reader.repoAnalysis() 

            self.system_prompt = """
                You are a professional technical writer skilled in writing clear and attractive open-source project README files across different programming languages and tech stacks.
                Based on the following two inputs, generate a complete, production-ready README.md file using Markdown syntax.

                Project Summary:
                {code_summary}

                Project File/Folder Structure:
                {repo_structure}
            """

            self.user_prompt = """
                The generated README.md file should include the following sections:
                - Project Title
                - Overview
                - Key Features
                - Folder Structure (as a Markdown code block)
                - Installation (use tech-specific install commands like `pip install`, `npm install`, etc.)
                - Usage (run instructions)
                - Technologies Used
                - Contributing Guidelines
                - License (default to MIT if not mentioned)

                If any information is unclear, use placeholders and mention that users should replace them.
                Strictly output only the README markdown. No extra comments.
            """

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading environment variables: {str(e)}")

    def generate_readme(self):
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                ("user", self.user_prompt)
            ])

            chain = prompt | self.llm

            result = chain.invoke({
                "code_summary": self.code_summary,
                "repo_structure": self.repo_structure
            })

            return result.content

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating README: {str(e)}")

    def write_readme(self):
        try:
            readme_content = self.generate_readme()
            with open("README.md", "w", encoding="utf-8") as f:
                f.write(readme_content)
            print("README.md file generated successfully.")
            self.clone_repo.delete_clone()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error writing README file: {str(e)}")
