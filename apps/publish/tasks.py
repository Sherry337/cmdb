from __future__ import absolute_import
from rest_framework.response import Response
from devops.celery import app
from utils.jenkins_api import JenkinsApi
from time import time,sleep
from publish.models import Deploy
from celery import shared_task,task



@app.task(name='release')
def release_code(pk,project_name,number):
    jenkins = JenkinsApi()
    start_time = time()
    data = {}
    sleep(10)
    while True:
       if (jenkins.get_build_info(project_name, number)) == "SUCCESS":
           data["release_status"] = 1
           # print(data)
           # Deploy.objects.filter(pk=pk).update(**data)
           break
       elif (jenkins.get_build_info(project_name, number)) == "ABORTED":
           data["release_status"] = 2
           # print(data)
           # Deploy.objects.filter(pk=pk).update(**data)
           break
       elif (jenkins.get_build_info(project_name, number)) == "FAILURE" or (time() - start_time) > 600:
           jenkins.stop_build(project_name, number)
           data["release_status"] = 3
           # print(data)
           # Deploy.objects.filter(pk=pk).update(**data)
           break
       else:
           console_output = jenkins.get_build_console_output(project_name, number)
           data['console_output'] = console_output
           Deploy.objects.filter(pk=pk).update(**data)
    console_output = jenkins.get_build_console_output(project_name, number)
    data['console_output'] = console_output
    # data['status'] = 4
    Deploy.objects.filter(pk=pk).update(**data)
    return project_name

    # return '[{}] Project release completed.......'.format(project_name)
#     return Response(serializer.data)

# @app.task(name='release')
# def release_code(pk,deploy):
#     jenkins = JenkinsApi()
#     start_time = time()
#     number = jenkins.get_next_build_number(deploy["project_name"])
#     data = {}
#     sleep(15)
#     while True:
#        if (jenkins.get_build_info(deploy["project_name"], number)) == "SUCCESS":
#            release_status = 1
#            deploy['release_status'] = release_status
#            print(data)
#            Deploy.objects.filter(pk=pk).update(**deploy)
#
#            break
#        elif (jenkins.get_build_info(deploy["project_name"], number)) == "ABORTED":
#            release_status = 3
#            deploy['release_status'] = release_status
#            print(data)
#            Deploy.objects.filter(pk=pk).update(**deploy)
#            # deploy.save()
#            break
#        # elif (jenkins.get_build_info(project_name, number)) == "FAILURE" or (time() - start_time) > 300:
#        elif (jenkins.get_build_info(deploy["project_name"], number)) == "FAILURE":
#            release_status = 2
#            deploy['release_status'] = release_status
#            print(data)
#            Deploy.objects.filter(pk=pk).update(**deploy)
#            # deploy.save()
#            break
    # return '[{}] Project release completed.......'.format(project_name)
    # return '[{}] Project release completed.......'.format(deploy.name)