from fastapi import FastAPI
from src.services.insert_csv_service import InsertUserService
from src.infra.dynamodb_config import s3


# boto3.setup_default_session(profile_name="Matt")
# s3 = boto3.client('s3')

# uiq-upload-bucket-edesoft
# test.csv

app = FastAPI()

@app.get('/get_csv/{bucket_name}/{object_key}')
async def get_csv(bucket_name: str, object_key: str):
    
    obj = s3.get_object(Bucket=bucket_name, Key=object_key)
    data = obj['Body'].read().decode('utf-8-sig').splitlines()
    data = list(data)

    try:
        response = InsertUserService.execute(data=data)
    except:
        return 'Error'

    return response


if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run("main:app", host="localhost", port=8000, log_level="info", reload=True)
