
# Server
````bash
sudo yum install iperf3
sudo iperf3 -s -V
#find running process
sudo lsof -i:5201
````

# Client
````bash
sudo yum install iperf3
SERVER_IP=10.0.0.1
sudo iperf3 -c "$SERVER_IP" -P 20 -w 128K -V > test1.txt
iperf3 -c $SERVER_IP -u -b 200M -t 30 > test2.txt
cat test1.txt
cat test2.txt
````

# Links
* [AWS Support](https://aws.amazon.com/es/premiumsupport/knowledge-center/low-bandwidth-vpn/)
