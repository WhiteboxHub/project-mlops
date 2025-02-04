

perliminary setup & aws permisssions need

iam role and persmissions


Lambda role permissions

s3 read permissions -> to allow lambda to read from the bucket

lambda execution permission -> to allow execution

ecs/ec2 start permissioin -> to start a Docker container

Cloudwatch Logging -> for debugging

s3 event notification configuration to trigger lambda on new CSV uplodes into the bucket



folder structure

```
└── 📁dvc_data_pipeline
    └── 📁config
        └── dvc_config.yaml
    └── 📁lambda
        └── handler.py
    └── 📁pipeline
        └── data_preprocessing.py
        └── data_validataion.py
        └── dvc.yaml
    └── 📁Scripts
        └── run_dvc.sh
    └── .dvc
    └── .dvcignore
    └── Dockerfile
    └── README.md
    └── requirements.txt
```