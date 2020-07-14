# Frontend Automation

This is a web automation framework for automating the steps as mentioned in the TestFlow document, using Python & Webdriver. Page Object Model (POM) is used to make the code more readable, maintainable, and resuable.

## Prerequisite:
1. Python 3.x
2. pip
3. Selenium Webdriver
4. Chrome Browser(can be extended for Firefox, IE)
5. Chromedriver

## How to run locally?

C:\testsample>python DickSmithWebUI.py

Note:
1. Ensure python executable is set in PATH environment variable
2. Set browser driver path, if needed
   Eg. chrome_driver_path = "chromedriver.exe"

## To Run tests in Continuous Integration tool (Jenkins)
Before begin, make sure that Python is installed on machine that Jenkins runs on it and that Python executable was added as environment variable.
1. Create a Jenkins job and configure Git repo in it, set Repository URL
2. In Build-steps, select Execute shell script option
3. Give command,
	python <python_script>.py
4. Save the jon and click on Build.
5. Check the console output.

## To Run in AWS Cloud
Tools: EC2, S3, Lambda, SQS, Cloudwatch
1. I'll be creating a Serverless.yaml file adding list of properties.
2. Deploy the code (*.py) using,
   $> sls deploy
3. Goto to correspondong lamda function, add a trigger using a lambda_fn_name to monitor Cloudwatch logs. 
4. Goto S3 bucket, upload testdata files
5. Create another json file for triggering the test, place it in SQS which will inturn trigger lambda function.
6. Goto cloudwatch an look for any observations.

Note: You will have to get your S3 file (convert testdata file *.csv to *.json) using boto3, write its contents inside /tmp (this is the only writable directory inside Lambda functions) and finally invoke it like:
os.system('python /tmp/myscript.py')
