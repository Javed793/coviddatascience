from uk_covid19 import Cov19API
import boto3
from datetime import datetime

def covidUkScraper():
    try:
        england_only = [
            'areaType=nation',
            'areaName=England'
        ]

        cases_and_deaths = {
            "date": "date",
            "areaName": "areaName",
            "areaCode": "areaCode",
            "newCasesByPublishDate": "newCasesByPublishDate",
            "cumCasesByPublishDate": "cumCasesByPublishDate",
            "newDeathsByDeathDate": "newDeathsByDeathDate",
            "cumDeathsByDeathDate": "cumDeathsByDeathDate"
        }

        api = Cov19API(filters=england_only, structure=cases_and_deaths)
        data = api.get_csv()
        writeToBucket(data)

    except Exception as e: print(e)
        
def writeToBucket(csvDailyData):
    try:
        now = datetime.now()
        DATE = now.strftime("%H:%M:%S")
        
        s3 = boto3.resource('s3')
        print ("[INFO] Request COVID-19 data...")
        BUCKET_NAME = "dailycovid19jav"
        OUTPUT_NAME = f"dataKeyTest{DATE}.csv"
        OUTPUT_BODY = csvDailyData
        print (f"[INFO] Saving Data to S3 {BUCKET_NAME} Bucket...")
        s3.Bucket(BUCKET_NAME).put_object(Key=OUTPUT_NAME, Body=OUTPUT_BODY)
        print (f"[INFO] Job done at {DATE}")
        
    except Exception as e: print(e)
    
def lambda_handler(event, context):
    covidUkScraper()

if __name__ == "__main__":
    covidUkScraper()
