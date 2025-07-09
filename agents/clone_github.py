import git
import os
import shutil

class CloneGitHubRepo:
    def __init__(self, clone_dir: str = "cloned_repos"):
        self.clone_dir = clone_dir

    def clone_repo(self,url: str, branch: str = "master"):
        if os.path.exists(self.clone_dir) and os.path.isdir(self.clone_dir):
            print(f"Directory {self.clone_dir} already exists. Using existing directory.")
            shutil.rmtree(self.clone_dir)
        
        os.makedirs(self.clone_dir, exist_ok=True)
        print(f"Cloning {url} into {self.clone_dir} ...")
        try:
            git.Repo.clone_from(url, self.clone_dir, branch=branch)
            print(f"Successfully cloned {url} into {self.clone_dir}.")
        except git.exc.GitCommandError as e:
            print(f"Failed to clone repository: {e}")
            return None
