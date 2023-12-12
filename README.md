# Pinterest Data Pipeline WIP
---
This project creates a data pipeline using data from Pinterest, including batch and streaming data containing details of a post, details of the user and geographical details. The data comes in a stream using AWS Kinesis, and is cleaned in Databricks using PySpark.\
Skills used:
- AWS (EC2, IAM, S3, MSK Connect, API Gateway, Kinesis, MWAA)
- Databricks
- PySpark
- SQL

## Table of Contents

- [1. Dependencies](#1-dependencies)
- [2. Installation](#2-installation)
- [3. The Pipeline](#3-the-pipeline)
    * [3.1. EC2](#31-EC2)
    * [3.2. MSK Connect](#32-msk-connect)
    * [3.3. API Gateway](#33-api-gateway)
    * [3.4. Databricks](#34-databricks)
    * [3.5. Streaming with Kinesis](#35-kinesis)
- [4. Usage](#4-usage)
- [5. File Structure](#5-file-structure)

## 1. Dependencies
Install the following python packages before running the project:

- requests
- time
- random
- multiprocessing
- boto3
- json
- sqlalchemy
- urllib
- pyspark

This project uses several services from AWS, so ensure you have an account ready to use. Also ensure that you have a working Databricks account.

## 2. Installation

To begin the project, clone the repo by running the following line in your terminal:

```
git clone https://github.com/kentlisa/pinterest-data-pipeline.git
```

Or, if you have GitHub CLI then run the following:

```
gh repo clone kentlisa/pinterest-data-pipeline
```

## 3. The Pipeline

### 3.1. EC2
 
Firstly, create an IAM user, then create an EC2 instance in your AWS account and connect to this on your local machine. Install Apache Kafka in you EC2 instance. Create three Kafka topics; one for post data (```.pin```), one for geographical data (```.geo```) and one for user data (```.user```). These will receive the batch and streaming data.

### 3.2. MSK Connect

Create an AWS S3 bucket to store your data. Download the Confluent.io Amazon S3 Connector and copy it into your S3 bucket. Then create a custom plugin in the MSK connect console. Finally, create a connector using the name of your S3 bucket, and the access role from your IAM user.

### 3.3. API Gateway

Create an API with a PROXY integration. Within this resource, create an **HTTP ANY** method. Deploy the API and make a note of the _invoke url_ for use later. Next, install the confluent package for the REST Proxy on your EC2 client machine.\
Start the REST Proxy on your EC2 client machine and run the ```user_posting_emulation.py``` file. This will send data to the Kafka topics. Find the data stored in your S3 bucket.

### 3.4. Databricks

Mount your S3 bucket to your Databricks account. Import the ```pinterest_notebook.ipynb``` file to Databricks.
Create an MWAA environment with an S3 bucket. Set up an MWAA-Databricks connection. Create a DAG to run the notebook daily. Upload the DAG to the MWAA S3 bucket.

### 3.5. Streaming with Kinesis 

Currently working on.


## 4. File Structure
```
├── 0ed442ca38ad_dag.py
├── 0ed442ca38ad-key-pair.pem
├── pinterest_notebook.ipynb
├── user_posting_emulation.py
├── user_posting_emulation_streaming.py
└── README.md
```
