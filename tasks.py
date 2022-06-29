from invoke import task, run
import shutil
from distutils import dir_util


@task
def backend(context):
    print("####### BUILDING BACKEND #######")
    run("pip install -r requirements.txt")


@task
def frontend(context):
    print("####### BUILDING FRONTEND #######")
    run("cd frontend && npm install")
    #dir_util.copy_tree("backend/app/templates/", "frontend/public/")
    run("cd frontend && npm run build")
    #run("cd frontend && npm run serve")


@task
def production(context):
    print("####### PREPARE PRODUCTION BUILD #######")
    shutil.copy("frontend/dist/index.html", "server/templates/index.html")
    dir_util.copy_tree("frontend/dist/", "server/static/")
    
    

@task
def build(context):
    backend(context)
    frontend(context)
    production(context)


@task
def serve(context):
    print("####### RUN WEB SERVER #######")
    #run("cd backend && uwsgi -s 0.0.0.0:5001 --protocol=http --module app --callable app")


@task
def buildAndServe(context):
    build(context)
    serve(context)
