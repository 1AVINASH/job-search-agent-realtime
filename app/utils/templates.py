import os
import json

class Templates:
    _instance = None

    REMOTE_MAIL = """
    You are a helpful agent that will help me create my cover letter. \
    I am a software engineer looking to get hired at a entry level role.\
    I have worked primarily with Python. Here are the other skills that might be relevant: AWS (Lambda, S3, API Gateway, RDBMS, EC2, Route53, etc.): 4 Yoe, Postgres, DynamoDB, Redis, \
    Docker, MongoDB, RabbitMQ, NATS, Celery, FastAPI, Flask.  \
        This is the company summary: {company_summary}, the job summary {summary} and reacent feature {recent_feature}. Based on the details I gave you,
        replace the '[company_objective]' below with a 2-3 liner that makes it seem like this cover letter was tailor made for this company. Add my own experience and how it will benefit the company based on what they do and if required, their latest feature as well

    Hi,
    I really liked what you are doing at {company_name}. [company_objective]. I wanted to reach out to see if there were any remote openings for Engineer at {company_name}. For the last 4 years, I have been building backend products. My journey started at Amazon where I worked as a data engineer and scaled a product from 16K queries to 1.6M queries. Wanting to build something from scratch and having a lot more impact, I switched to a startup where I created multiple products from scratch, while understanding the business needs, and tailoring the features to the requirements. I collaborated with multiple teams including but not limited to product managers, designers, and frontend engineers. My latest stint was at Zanskar where I worked on low latency systems, and led the backend development for multiple products. I am looking to work at a place where I can continue owning products end-to-end, while also growing rapidly as an engineer. While I have majorly worked in backend, I have been learning frontend as well, and I will like to explore opportunities that let me work on both. 
    I’m looking for a remote role where I can contribute meaningfully while continuing to learn. While I haven’t worked remotely full-time yet, I’ve often collaborated with distributed teams, managed responsibilities autonomously, and communicated async. I believe I’m well-suited for a remote setup that values trust, ownership, and clear communication.

    I have previously worked majorly with Python and AWS (serverless majorly), but I also have professional experience with Golang, and ReactJs. On the infra side, I have worked on DynamoDB, Postgres, MongoDB, Redis, RabbitMQ, and more.
    From what I have seen, {company_name} offers a strong opportunity of growth and meaningful impact, and I think my skills well aligns with your business needs. 

    Happy to share more details or chat further if there's a potential fit.

    Best,
    Your Name
    LinkedIn -> https://www.linkedin.com/in/your-linked-in/
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

        I am a software engineer with no experience and I am open to working at any company (location is not a bar). \
        I am preferably looking to get hired at a entry level job.\
        I have worked majorly with Python. Here are the other skills that might be relevant: AWS (Lambda, S3, API Gateway, RDBMS, EC2, Route53, etc.): 4 Yoe, Postgres, DynamoDB, Redis, \
        Docker, MongoDB, RabbitMQ, NATS, Celery, FastAPI, Flask \
        Only consider the companies that match my skills. Also make sure to get the job link to apply to\
        
        {format_instructions}
    """

    JOB_SEARCH_QUERY = "Remote software engineer jobs (contract) at recently funded startups in the ai scope"
    LINKEDIN_JOB_SEARCH_QUERY = "site:linkedin.com \"remote\" \"software engineer\" \"startup\" jobs"

    @property
    def job_search_query(self):
        return self.templates.get("job_search_query") or self.JOB_SEARCH_QUERY
    
    @property
    def linkedin_job_search_query(self):
        return self.templates.get("linkedin_job_search_query") or self.LINKEDIN_JOB_SEARCH_QUERY
    
    @property
    def remote_mail(self):
        return self.templates.get("remote_mail_template") or self.REMOTE_MAIL
    
    @property
    def generic_cover_letter(self):
        return self.templates.get("generic_cover_letter_template") or self.GENERIC_COVER_LETTER
    
    @property
    def jobs_parser(self):
        return self.templates.get("jobs_parser_template") or self.JOBS_PARSER
    
    @property
    def templates(self):
        return self._templates
    
    @templates.setter
    def templates(self, templates):
        self._templates = templates
    
    def _initialize_templates(self):
        template_file = "/app/.templates.json"
        if not os.path.exists(template_file):
            print(f"File does not exist")
            self.templates = {}
        with open(template_file, 'r', encoding='utf-8') as f:
            templates = json.load(f)
            self.templates = templates

    def __init__(self):
        print("Initializing template")
        self._initialize_templates()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        
        return cls._instance


templates = Templates()