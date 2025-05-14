# Food and Beverages Trend Analysis  

## Objective: 
This project automates the end-to-end pipeline for analyzing food and beverage trends by:
- Ingesting CSV files
- Converting them to Excel format
- Loading data into Amazon Redshift
- Visualizing insights in Power BI

## Tech Stack:
- Containerisation: Docker and Amazon Elastic Container Registry (ECR)
- Storage: Amazon S3 (for raw and processed files)
- File Processing: AWS Lambda (deployed via Docker)
- Data Warehouse: Amazon Redshift Serverless
- Dashboard: Microsoft Power BI

## Workflow:
1. Upload CSV files
- CSV files are uploaded to a designated Amazon S3 bucket.
  
2. Automatic Conversion with AWS Lambda
- A Lambda function is triggered upon file upload.
- It converts the CSV file to Excel format and uploads the result back to S3.
  
3. Load into Amazon Redshift
- A Redshift COPY command ingests the cleaned data into the warehouse.
  
4. Visualize in Power BI
- Power BI connects directly to Redshift.
- Reports are updated automatically on a scheduled refresh.

## Project Files:

1. `lambda_function.py`
- Python script that converts CSV to Excel upon S3 upload trigger.
  
2. `Dockerfile`
- Packages the Lambda function in a container using the AWS-provided Python 3.9 base image
- The Docker image is built locally and pushed to Amazon ECR.

3. `requirements.txt`
- Lists Python dependencies used by the Lambda function.







  

