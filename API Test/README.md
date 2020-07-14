# API Automation

This is a API automation framework for automating the steps as mentioned in the requirement document, using Python.

## Prerequisite:
1. Python 3.x
2. pip

## How to run locally?
C:\testsample>python AirVisualWebAPI.py

Note:
1. Ensure python executable is set in PATH environment variable
2. ApiKey.txt file is in place

## To Run tests in Docker container to enable CICD (Bamboo)
Before begin, make sure you have Bamboo super user privilege to create a job & build.
Configure Github SCM to access the repo,
1. Create a Bamboo job and configure tasks
2. Add a task with below to run a script file,
   Goto folder in bamboo wherever the docker_run.sh has been copied
   chmod 755 docker_run.sh
   ./docker_run.sh
