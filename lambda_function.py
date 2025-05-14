import os
import csv
import openpyxl
import tempfile
import boto3

def lambda_handler(event, context):
    print("Received event:", event)
    
    s3 = boto3.client('s3')
    
    try:
        for record in event['Records']:
            bucket_name = record['s3']['bucket']['name']
            file_key = record['s3']['object']['key']
            
            # Only process .xlsx files
            if not file_key.lower().endswith('.xlsx'):
                print(f"Skipping non-Excel file: {file_key}")
                continue

            temp_dir = tempfile.mkdtemp()
            try:
                # Download the Excel file
                local_excel_path = os.path.join(temp_dir, 'input.xlsx')
                s3.download_file(bucket_name, file_key, local_excel_path)

                # Load workbook
                workbook = openpyxl.load_workbook(local_excel_path)
                base_filename = os.path.splitext(os.path.basename(file_key))[0]

                # Only one sheet expected
                sheet_obj = workbook.active  # gets the first/only sheet
                csv_filename = f"{base_filename}.csv"
                csv_path = os.path.join(temp_dir, csv_filename)
                
                with open(csv_path, 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    for row in sheet_obj.iter_rows():
                        writer.writerow([cell.value for cell in row])
                
                # Upload CSV to S3 under 'converted/' prefix
                s3.upload_file(csv_path, bucket_name, f"converted/{csv_filename}")
                print(f"Uploaded converted/{csv_filename} to S3")

                cleanup_temp_directory(temp_dir)

            except Exception as e:
                print(f"Failed to process file {file_key}: {e}")

    except Exception as e:
        print(f"Error parsing event: {e}")
        return {"status": "error", "message": str(e)}

    return {"status": "success"}
    
def cleanup_temp_directory(temp_dir):
    for file in os.listdir(temp_dir):
        path = os.path.join(temp_dir, file)
        try:
            os.remove(path)
        except Exception as e:
            print(f"Failed to delete file {path}: {e}")
    try:
        os.rmdir(temp_dir)
    except Exception as e:
        print(f"Failed to remove directory {temp_dir}: {e}")
