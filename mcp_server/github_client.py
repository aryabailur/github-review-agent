from github import Github
from github import Auth 
from dotenv import load_dotenv
import os
load_dotenv()
github_token=os.getenv("GITHUB_TOKEN")

def git_initialization(repo_name,pr_number):
    g=Github(github_token)
    repo=g.get_repo(repo_name)
    pr=repo.get_pull(pr_number)
    return pr

def get_pr_files(repo_name:str,pr_number:int):
    
    pr=git_initialization(repo_name,pr_number)
    files=pr.get_files()
    files_dict={}
    files_list=[]
    for file in files:
        files_dict={
            "name":file.filename,
            "differences":file.patch
        }
        files_list.append(files_dict)
    return files_list

def get_pr_details(repo_name,pr_number):
    pr=git_initialization(repo_name,pr_number)
    pr_info={
        "title":pr.title,
        "body":pr.body,
        "state":pr.state,
        "username":pr.user.login
    }
    return pr_info

def get_file_content(repo_name,file_path):
    g=Github(github_token)
    repo=g.get_repo(repo_name)
    file=repo.get_contents(file_path)
    return file.decoded_content.decode("utf-8")

def post_review_comment(repo_name,pr_number,comment):
    pr=git_initialization(repo_name,pr_number)
    comment=pr.create_issue_comment(comment)
    return comment.body