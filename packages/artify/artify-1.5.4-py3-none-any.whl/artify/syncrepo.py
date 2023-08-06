import __main__
import re

def commit_push_changes(message):
    print("Committing changes:::")
    
    git_tag_command = ''
    git_push_command = ''
    
    path = __main__.os.path.abspath(__main__.os.getcwd())   
    
    if message == 'tag':
        # To-do Extract version number from project
        version = '1.0.0'
        git_tag_command = "git tag v{}".format(version)
        process_git_tag = __main__.Popen(git_tag_command, shell=True, stdout=__main__.PIPE, cwd=path)
        print("INFO: Tag v{} created".format(version))
    else:   
        git_commit_command = "git commit -am '{}'".format(message)
        process_git_commit = __main__.Popen(git_commit_command, shell=True, stdout=__main__.PIPE, cwd=path)
        print("INFO: Commit result: ", process_git_commit.communicate()[0])
    
    if __main__.os.environ.get('PRIVATE_TOKEN') == None:
        print("ERROR: Private token missing. Please added PRIVATE_TOKEN to Environment variables")
        __main__.os.sys.exit(1)
    
    auth = "//" + __main__.os.environ.get('GITLAB_USER_LOGIN') + ":" + __main__.os.environ.get('PRIVATE_TOKEN') + "@"

    repository_url = __main__.os.environ.get("CI_REPOSITORY_URL")
    ## CI_PROJECT_URL
        
    ## Repository url with token
    ci_repo_url  = re.sub("//.*?@", auth, repository_url)
    
    if __main__.branch == '' and message != 'tag':
        __main__.branch = 'develop'
    
    if __main__.branch == '' and message == 'tag':
        __main__.branch = 'master'
      
    print("INFO: Pushing version changes:::")
    ##git_push_command = "git push origin {}".format(os.environ.get('CI_COMMIT_BRANCH'))
    
    # To-do Delete branch after merge with feature/patch-version, feature/minor-version, feature/major-version, feature/release-version
    # delete branch locally
    # git branch -d localBranchName

    # delete branch remotely
    # git push origin --delete remoteBranchName
    
    if message == 'tag':
        git_push_command = "git config user.name {}; git config user.email {}; git push --tags {} HEAD:{}".format(__main__.os.environ.get('GITLAB_USER_LOGIN'), __main__.os.environ.get('GITLAB_USER_EMAIL'), ci_repo_url, __main__.branch)
    else: 
        git_push_command = "git config user.name {}; git config user.email {}; git push {} HEAD:{}".format(__main__.os.environ.get('GITLAB_USER_LOGIN'), __main__.os.environ.get('GITLAB_USER_EMAIL'), ci_repo_url, __main__.branch)
 
    ##git_push_command = "git config user.name {}; git config user.email {}; git push {} HEAD:{}".format(os.environ.get('GITLAB_USER_LOGIN'), os.environ.get('GITLAB_USER_EMAIL'), ci_repo_url, os.environ.get('CI_COMMIT_BRANCH'))
    process_git_push = __main__.Popen(git_push_command, shell=True, stdout=__main__.PIPE, cwd=path)
    print("INFO: Push result: ", process_git_push.communicate()[0])