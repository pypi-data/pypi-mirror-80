import __main__
import re

def commit_push_changes(message):
    print("Committing changes:::")
    path = __main__.os.path.abspath(__main__.os.getcwd())   
    git_commit_command = "git commit -am '{}'".format(message)
    process_git_commit = __main__.Popen(git_commit_command, shell=True, stdout=__main__.PIPE, cwd=path)
    print("Commit result: ", process_git_commit.communicate()[0])
        
    auth = "//" + __main__.os.environ.get('GITLAB_USER_LOGIN') + ":" + __main__.os.environ.get('PRIVATE_TOKEN') + "@"

    repository_url = __main__.os.environ.get("CI_REPOSITORY_URL")
    ## CI_PROJECT_URL
        
    ## Repository url with token
    ci_repo_url  = re.sub("//.*?@", auth, repository_url)
    
    if __main__.branch == '':
        __main__.branch = 'develop'
        
    print("Pushing version changes:::")
    ##git_push_command = "git push origin {}".format(os.environ.get('CI_COMMIT_BRANCH'))
    git_push_command = "git config user.name {}; git config user.email {}; git push {} HEAD:{}".format(__main__.os.environ.get('GITLAB_USER_LOGIN'), __main__.os.environ.get('GITLAB_USER_EMAIL'), ci_repo_url, __main__.branch)
    ##git_push_command = "git config user.name {}; git config user.email {}; git push {} HEAD:{}".format(os.environ.get('GITLAB_USER_LOGIN'), os.environ.get('GITLAB_USER_EMAIL'), ci_repo_url, os.environ.get('CI_COMMIT_BRANCH'))
    process_git_push = __main__.Popen(git_push_command, shell=True, stdout=__main__.PIPE, cwd=path)
    print("Push result: ", process_git_push.communicate()[0])