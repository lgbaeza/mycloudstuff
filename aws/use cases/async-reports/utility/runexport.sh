IdReporte=$1
REMOTE_HOST=YOUR_REMOTE_HOST
YOUR_AWS_REGION="us-east-1"
PGPASSWORD="$(aws rds generate-db-auth-token --hostname $REMOTE_HOST --port 5432 --region $YOUR_AWS_REGION --username rdsiamuser;)"

export PGPASSWORD=$PGPASSWORD
echo "IdReporte: $IdReporte"

RESULT=$(php exportdb.php $IdReporte $REMOTE_HOST $PGPASSWORD)
if [ "$RESULT"="0" ]; then
    echo "ok"    
    exit
else
    echo "error"
    echo $RESULT
    exit 1
fi