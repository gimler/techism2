#!/usr/bin/env python

from yaml import load, dump
from yaml import Loader, Dumper
import sys, subprocess
from datetime import date

def prod_deploy():
    _pull()
    _check_git_status()
    
    version = _update_app_yaml_for_prod_deploy()
    _update_version_html(version)
    _commit_prod_deploy(version)
    _tag_prod_deploy(version)
    _deploy()
    
    next_dev_version = _update_app_yaml_for_dev()
    _update_version_html(next_dev_version)
    _commit_dev(next_dev_version)
    
    _push()
    sys.stdout.write("Prod deployment successful, check http://%s.latest.techism2.appspot.com and update default version in App Engine console.\n" % version)
    
    
def _check_git_status():
    # check clean working copy using 'git status'
    proc = subprocess.Popen(["git", "status", "--porcelain"], stdout=subprocess.PIPE)
    git_status_result = proc.communicate()[0]
    if len(git_status_result) > 0:
        sys.stderr.write("Uncommitted changes, please clean up first:\n")
        sys.stdout.write(git_status_result)
        sys.exit(1)


def _pull():
    subprocess.check_call(["git", "pull"])


def _push():
    subprocess.check_call(["git", "push"])


def _commit_prod_deploy(version):
    subprocess.check_call(["git", "commit", "-a", "-m", "Prepare prod deployment, version " + str(version)])


def _commit_dev(next_version):
    subprocess.check_call(["git", "commit", "-a", "-m", "Prepare development, next version " + str(next_version)])


def _tag_prod_deploy(version):
    subprocess.check_call(["git", "tag", "-a", "v"+str(version), "-m", "Tag version " + str(version)])
    sys.stdout.write("Created tag v" + str(version) + " for prod deployment\n")


def _deploy():
    #subprocess.check_call(["./manage.py", "deploy", "--nosyncdb"])
    subprocess.check_call(["./manage.py", "deploy"])


def _update_app_yaml_for_prod_deploy():
    '''
    Updates 'app.yaml', sets the application to 'techism2'.
    '''
    infile = file('app.yaml')
    data = load(infile, Loader=Loader)
    infile.close()
    data['application'] = "techism2"
    data['version'] = str(data['version']).split('-devel')[0]
    outfile = file('app.yaml', 'w')
    dump(data, outfile)
    outfile.close()
    version = data['version']
    sys.stdout.write("Updated app.yaml for prod deployment, version " + str(version) + "\n")
    return version


def _update_app_yaml_for_dev():
    '''
    Updates 'app.yaml', sets the application to 'techism2-devel' and increments the version and append '-devel'.
    '''
    infile = file('app.yaml')
    data = load(infile, Loader=Loader)
    infile.close()
    data['application'] = "techism2-devel"
    data['version'] = str(int(data['version']) + 1) + "-devel"
    outfile = file('app.yaml', 'w')
    dump(data, outfile)
    outfile.close()
    next_version = data['version']
    sys.stdout.write("Updated app.yaml for development, next version " + str(next_version) + "\n")
    return next_version


def _update_version_html(version):
    '''
    Updates the 'templates/version.html'.
    '''
    infile = file('templates/version.html')
    newlines = []
    for line in infile:
        if 'version.number' in line:
            newlines.append("  <span id=\"version.number\">Version %s,</span>\n" % str(version))
        elif 'version.tag' in line:
            newlines.append("  <span id=\"version.tag\"><a href=\"http://github.com/cko/techism2/tree/v%s\">Git Tag</a>,</span>\n" % str(version))
        elif 'version.date' in line:
            newlines.append("  <span id=\"version.date\">%s</span>\n" % date.today().isoformat())
        else:
            newlines.append(line)
    infile.close()
    outfile = file('templates/version.html', 'w')
    outfile.writelines(newlines)
    outfile.close()
    sys.stdout.write("Updated version.html, version " + str(version) + "\n")


