MSGBody='[{"Id":"1","MessageBody":"hello"}'
for ID in {2..10}
do
MSGBody+=',{"Id":"'$ID'","MessageBody":"hello"}'
done
MSGBody+=']'

for ID in {1..100}
do
res=$(aws sqs send-message-batch --queue-url="<REPLACE_WITH_YOUR_QUEUE_URL>" --entries $MSGBody)
echo $res
done
echo "sent 1000"