import os
import time

from abkit.models import Experiment
import abkit.db as db

from markdown import markdown
import requests
from functools import wraps



def exception_resistant(func):
    num_fails = 0
    max_fails = 6

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal num_fails
        func_name = func.__name__
        try:
            return func(*args, **kwargs)
        except Exception as e:
            num_fails += 1
            if num_fails == 1:
                print(('Something went wrong in `{}`. ' +
                       'The process will continue to ' +
                       'execute.').format(func_name))
            if num_fails <= max_fails:
                print('`{}`: {}'.format(func_name, e))
            elif num_fails == max_fails + 1:
                print(('The rest of the `{}` errors ' +
                       'are hidden.').format(func_name))
    return wrapper

def check_service_ifready(port,host="localhost"):
    url = "http://{host}:{port}/meta".format(host=host,port=port)
    try:
        resp=requests.get(url)
        return resp.status_code
    except Exception as e:
        print(e) 
        return 300
    
#check_service_ifready(9002)

def wait_until_port_used(
    port, max_wait_sec=20, interval_sec=0.5
):
    """
    wait until the port is used.  *Notice this function will invoke\
    a bash shell to execute command [netstat]!*
    :return:
        return True if the port is used
    """
    curr_wait_sec = 0 
    while curr_wait_sec < max_wait_sec:
        fd_pid = os.popen("lsof -i:%s|awk '{print $2}'" % str(port))
        pids = fd_pid.read().strip().split('\n')
        #if is_port_free(port) is None:
        if len(pids)>1:
            return True
        curr_wait_sec += interval_sec
        time.sleep(interval_sec)
    return False

def kill9_byport(port):
    """
    kill -9 process by name
    """
    fd_pid = os.popen("lsof -i:%s|awk '{print $2}'" % str(port))
    pids = fd_pid.read().strip().split('\n')
    
    fd_pid.close()
    print(pids)
    for pid in pids:
        os.system("kill -9 %s" % (pid))
        
        
#kill9_byport("9001")





def determine_period():
    per={'period':'day'}
    period = per.get('period', 'day')
    if period not in ['day', 'week', 'month', 'year']:
        err = {'error': 'invalid argument: {0}'.format(period), 'status': 400}
        #abort(400, jsonify(err))
    return period
def simple_markdown(experiment):
    description = experiment['description']
    if description and description != '':
        experiment['pretty_description'] = markdown(description)
    return experiment

def experiment_list():
    experiments = Experiment.all(redis=db.REDIS)
    period = determine_period()
    experiments = [simple_markdown(exp.objectify_by_period(period)) for exp in experiments]
    return experiments
def archived():
    experiments = Experiment.archived(redis=db.REDIS)
    period = determine_period()
    experiments = [simple_markdown(exp.objectify_by_period(period)) for exp in experiments]
    return experiments

def paused():
    experiments = Experiment.paused(redis=db.REDIS)
    period = determine_period()
    experiments = [simple_markdown(exp.objectify_by_period(period)) for exp in experiments]#[exp.name for exp in experiments]
    return experiments


def find_or_404(experiment_name,kpi=None):
    try:
        experiment_name = experiment_name
        exp = Experiment.find(experiment_name, db.REDIS)
        if kpi:#设置kpi，用于页面查询，需要kpis列表非空否则出错，server端调用时也需要有kpi的参数输入
            exp.set_kpi(kpi)
        #if request.args.get('kpi'):
        #   exp.set_kpi(request.args.get('kpi'))
        return True,exp
    except ValueError:
        return False,None

# Set winner for an experiment
def set_winner(experiment_name,alternative_name):
    bRet,experiment = find_or_404(experiment_name)
    if bRet:
        experiment.set_winner(alternative_name)
        return True,"Sucess"
    else:
        return False,"None experiment is found"

# Reset experiment not run
def reset_experiment_old(experiment_name):
    bRet,experiment = find_or_404(experiment_name)
    if experiment:
        exp_name = experiment.name
        exp_desc = experiment.description
        exp_alts = experiment.get_alternative_names()
        experiment.reset()
        print(exp_name,exp_alts,exp_desc,"haahhahah")
        new_exp = Experiment.find_or_create(exp_name,exp_alts,redis=db.REDIS)
        new_exp.update_description(exp_desc)
        return True,"Sucess"
    else:
        return False,"None experiment is found"
# Reset experiment running
def reset_experiment(experiment_name):
    bRet,experiment = find_or_404(experiment_name)
    if experiment:
        exp_name = experiment.name
        exp_desc = experiment.description
        exp_alts = experiment.get_alternative_names()
        experiment.delete()
        new_exp = Experiment.find_or_create(exp_name,exp_alts,redis=db.REDIS)
        new_exp.update_description(exp_desc)
        return True,"Sucess"
    else:
        return False,"None experiment is found"
# Pause experiment
def toggle_experiment_pause(experiment_name):
    bRet,experiment = find_or_404(experiment_name)
    if experiment.is_paused():
        experiment.resume()
    else:
        experiment.pause()
    return True,"Sucess"
# Pause experiment
def update_experiment_description(experiment_name,description):
    bRet,experiment = find_or_404(experiment_name)
    experiment.update_description(description)
    return True,"Sucess"

# Archive experiment
def toggle_experiment_archive(experiment_name):
    bRet,experiment = find_or_404(experiment_name)
    if experiment.is_archived():
        return False,"Exp has already archived"
    else:
        experiment.archive()
    return True,"Sucess"
# Delete experiment
def delete_experiment(experiment_name):
    bRet,experiment = find_or_404(experiment_name)
    experiment.delete()
    return True,"Sucess"

def reset_winner(experiment_name):
    bRet,experiment = find_or_404(experiment_name)
    experiment.reset_winner()
    return True,"Sucess"