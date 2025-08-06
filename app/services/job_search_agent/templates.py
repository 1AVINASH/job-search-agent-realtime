REMOTE_MAIL = """
You are a helpful agent that will help me create my cover letter. \
I am a software engineer that lives in Bengaluru with 4 years of experience and I am open to working at any company (location is not a bar). \
I am preferably looking to get hired at a Mid Seniority role.\
I have worked majorly with Python and also have 8 months of experience in Golang. Here are the other skills that might be relevant: AWS (Lambda, S3, API Gateway, RDBMS, EC2, Route53, etc.): 4 Yoe, Postgres, DynamoDB, Redis, \
Docker, MongoDB, RabbitMQ, NATS, Celery, FastAPI, Flask.  \
    This is the company summary: {company_summary}, the job summary {summary} and reacent feature {recent_feature}. Based on the details I gave you,
    replace the '[company_objective]' below with a 2-3 liner that makes it seem like this cover letter was tailor made for this company. Add my own experience and how it will benefit the company based on what they do and if required, their latest feature as well

Hi,
I really liked what you are doing at {company_name}. [company_objective]. I wanted to reach out to see if there were any remote openings for Engineer at {company_name}. For the last 4 years, I have been building backend products. My journey started at Amazon where I worked as a data engineer and scaled a product from 16K queries to 1.6M queries. Wanting to build something from scratch and having a lot more impact, I switched to a startup where I created multiple products from scratch, while understanding the business needs, and tailoring the features to the requirements. I collaborated with multiple teams including but not limited to product managers, designers, and frontend engineers. My latest stint was at Zanskar where I worked on low latency systems, and led the backend development for multiple products. I am looking to work at a place where I can continue owning products end-to-end, while also growing rapidly as an engineer. While I have majorly worked in backend, I have been learning frontend as well, and I will like to explore opportunities that let me work on both. 
 I’m looking for a remote role where I can contribute meaningfully while continuing to learn. While I haven’t worked remotely full-time yet, I’ve often collaborated with distributed teams, managed responsibilities autonomously, and communicated async. I believe I’m well-suited for a remote setup that values trust, ownership, and clear communication.

I have previously worked majorly with Python and AWS (serverless majorly), but I also have professional experience with Golang, and ReactJs. On the infra side, I have worked on DynamoDB, Postgres, MongoDB, Redis, RabbitMQ, and more.
From what I have seen, {company_name} offers a strong opportunity of growth and meaningful impact, and I think my skills well aligns with your business needs. Outside of work, I love to play chess, football, badminton (and all kinds of sports), and love to travel as well. These keep me creative, focused, and balanced-- qualities I bring to my work as well.

Happy to share more details or chat further if there's a potential fit.

Best,
Avinash Singh
LinkedIn -> https://www.linkedin.com/in/avinash-singh-1b8636136/
GitHub -> https://github.com/1AVINASH"""


GENERIC_COVER_LETTER = """Write a professional cover letter for a job.

Company: {company}
Title: {title}
Description: {summary}

Use a formal, excited tone. Output only the letter.
"""


JOBS_PARSER = """
Extract structured jobs info from the following description:

{text}

    I am a software engineer that lives in Bengaluru with 4 years of experience and I am open to working at any company (location is not a bar). \
    I am preferably looking to get hired at a Mid Seniority role.\
    I have worked majorly with Python and also have 8 months of experience in Golang. Here are the other skills that might be relevant: AWS (Lambda, S3, API Gateway, RDBMS, EC2, Route53, etc.): 4 Yoe, Postgres, DynamoDB, Redis, \
    Docker, MongoDB, RabbitMQ, NATS, Celery, FastAPI, Flask \
    Only consider the companies that match my skills. \
    
    {format_instructions}
"""