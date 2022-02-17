#!/bin/bash
YOUR_HOME_REGION="us-west-2"
AWS_ACCESS_KEY_ID="XXXXXXXXXXXXXX"
AWS_SECRET_ACCESS_KEY="YYYYYYYYYYY"

curl -o ./aws-discovery-agent.tar.gz https://s3-us-west-2.amazonaws.com/aws-discovery-agent.us-west-2/linux/latest/aws-discovery-agent.tar.gz

tar -xzf aws-discovery-agent.tar.gz

sudo bash install -r $YOUR_HOME_REGION -k $AWS_ACCESS_KEY_ID -s $AWS_SECRET_ACCESS_KEY

#start agent
sudo systemctl start aws-discovery-daemon.service