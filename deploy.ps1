#source my_virtual_env/bin/activate #to go into virtual env


#pip3 install --target ./package boto3
if (Select-String -Path "lambda_function.py" -Pattern 'os.getenv("') { Write-Error "os.getenv found in the file."; return }

rm ./my_deployment_package.zip
Set-Location package
zip -r ../my_deployment_package.zip .                                       
Set-Location ..
zip my_deployment_package.zip lambda_function.py                            
zip my_deployment_package.zip values.py

# aws lambda update-function-code --zip-file ./my_deployment_package.zip --publish