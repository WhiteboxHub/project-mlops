CONFIG_FILE=".env"

if [ -f "$CONFIG_FILE" ]; then
    echo "Loading configuration from $CONFIG_FILE..."
    source "$CONFIG_FILE"
else
    echo "Error: Configuration file $CONFIG_FILE not found!"
    exit 1
fi


dvc init
dvc remote add s3remote s3://$BUCKET_NAME/trainingdata
dvc remote modify s3remote endpointurl https://s3.amazonaws.com
dvc remote modify s3remote access_key_id $AWS_ACCESS_KEY_ID
dvc remote modify s3remote secret_access_key $AWS_SECRET_ACCESS_KEY
