from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from agents.createReadme import ReadmeGenerator
import os

app = FastAPI()
load_dotenv()

@app.post("/generate_readme/")
async def generate_readme(github_url: str):
    if not github_url:
        raise HTTPException(status_code=400, detail="GitHub URL is required")
    
    try:
        readme_generator = ReadmeGenerator(github_url)
        readme_file = readme_generator.write_readme()
        return FileResponse(path=readme_file, filename="downloaded_file.txt", media_type='application/octet-stream')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating README: {str(e)}")