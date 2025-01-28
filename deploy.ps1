rm ./my_deployment_package.zip
Set-Location package
zip -r ../my_deployment_package.zip .                                       
Set-Location ..
zip my_deployment_package.zip lambda_function.py                            

aws lambda update-function-code --zip-file ./my_deployment_package.zip --publish