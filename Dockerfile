FROM public.ecr.aws/lambda/python:3.9

# Copy requirements and install them
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy your function code
COPY lambda_function.py ./

# Set the CMD to your handler (app.lambda_handler)
CMD ["lambda_function.lambda_handler"]
