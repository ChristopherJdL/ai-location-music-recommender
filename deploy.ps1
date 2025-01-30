#source my_virtual_env/bin/activate #to go into virtual env


#pip3 install --target ./package boto3

rm ./deployment_package.zip
cd package
zip -r ../deployment_package.zip .                                       
cd ..
zip deployment_package.zip lambda_function.py                            
zip deployment_package.zip prompts/*

# aws lambda update-function-code --zip-file ./my_deployment_package.zip --publish