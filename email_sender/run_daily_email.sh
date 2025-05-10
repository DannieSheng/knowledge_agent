#!/bin/bash

# Activate conda environment (if using conda)
# source /Users/hudanyunsheng/miniforge3/bin/activate llm_proj


# Run the Python script that sends the email
/Users/hudanyunsheng/miniforge3/envs/llm_proj/bin/python /Users/hudanyunsheng/Documents/GitHub/knowledge_agent/email_sender/email_scheduler.py >> /Users/hudanyunsheng/Documents/GitHub/knowledge_agent/logs/daily_email.log 2>&1