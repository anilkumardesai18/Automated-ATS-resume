import csv
import random

resumes = [
    "Senior data analyst with 6 years of experience in business intelligence, SQL, Python, Tableau, and data warehousing. Led data engineering team to build pipeline saving 500 hours annually.",
    "Full stack developer with 5 years of experience in React, Node.js, Express, MongoDB, and AWS cloud architecture. Built responsive SaaS platform handling 100k daily users.",
    "Cybersecurity analyst with 5 years of experience in network security, incident response, SIEM tools, firewalls, and risk assessments. Certified CISSP.",
    "Sales manager with 7 years of experience in B2B enterprise software sales, CRM management, pipeline building, and negotiating contracts. Closed $5M in new business.",
    "Healthcare analyst with 4 years of experience in medical data analysis, EMR systems, patient flow optimization, and SQL dashboard reporting.",
    "Backend engineer with 5 years of experience building scalable APIs in Go and Python. Expert in PostgreSQL database tuning and Redis caching.",
    "DevOps engineer with 4 years of experience in Docker, Kubernetes, Jenkins CI/CD pipelines, and Terraform infrastructure as code on GCP.",
    "Digital payments product manager with 6 years of experience launching and scaling payment products. Expert in UPI, cards, and PCI-DSS compliance.",
    "Operations manager with 9 years of experience in supply chain, logistics operations, warehouse management, and vendor renegotiation.",
    "Pilot with 12 years of experience flying commercial aircraft. Captain, logged 8000+ flight hours. Expert in safety compliance."
]

jds = [
    "Senior Business Intelligence Analyst at enterprise firm. Required skills: SQL, Python, Tableau, data warehousing, BI reporting, stakeholder collaboration.",
    "Full Stack Engineer at startup. Required skills: React, Node.js, REST APIs, cloud databases, frontend design, agile methodology.",
    "Cybersecurity Analyst at enterprise firm. Required skills: network protection, security auditing, SIEM monitoring, threat intelligence, risk mitigation.",
    "Sales Manager at SaaS company. Required skills: B2B sales experience, CRM tracking, customer success, negotiation, quota attainment.",
    "Healthcare Data Analyst at hospital network. Required skills: health datasets, EMR documentation, reporting tools, SQL database management.",
    "Backend Engineer at a fast-growing e-commerce platform. Required skills: Python/Go, REST API development, database optimization, microservices.",
    "DevOps Cloud Engineer. Required skills: containerization (Docker, Kubernetes), AWS/GCP architecture, automated CI/CD pipelines, scripting.",
    "Product Manager - Payments. Required skills: product roadmap planning, online payment flows (cards, wallets), API integrations, agile delivery.",
    "Logistics and Supply Chain Operations Lead. Required skills: team management, warehouse storage optimization, vendor procurement, budget planning.",
    "Captain / Pilot for commercial airline. Required skills: commercial flight license, safety regulation knowledge, team coordination, emergency management."
]

labels = ["high", "medium", "low", "HIGH", "High", "MEDIUM"]

# Generate 320 records to match the EDA notebook characteristics
data = []
for i in range(320):
    # Select index for resume and jd
    r_idx = random.randint(0, len(resumes) - 1)
    # 70% chance to match the correct JD for high score, 30% chance for mismatches
    if random.random() < 0.4:
        j_idx = r_idx
        score = round(random.uniform(0.75, 0.95), 2)
        label = random.choice(["high", "HIGH", "High"])
    elif random.random() < 0.8:
        j_idx = (r_idx + random.randint(1, 3)) % len(jds)
        score = round(random.uniform(0.40, 0.70), 2)
        label = random.choice(["medium", "MEDIUM"])
    else:
        j_idx = (r_idx + random.randint(4, len(jds) - 1)) % len(jds)
        score = round(random.uniform(0.05, 0.35), 2)
        label = "low"
    
    # Introduce some outliers / invalid values as flagged in Notebook 1
    if i in [247, 261, 262, 266, 309, 319]:
        if i == 247:
            score = 2.30
            label = "medium"
        elif i == 261:
            score = 1.50
            label = "high"
        elif i == 262:
            score = -0.20
            label = "high"
        elif i == 266:
            score = 99.00
            label = "low"
        elif i == 309:
            score = 1.20
            label = "high"
        elif i == 319:
            score = -0.05
            label = "high"
            
    data.append({
        "resume_text": resumes[r_idx],
        "job_description": jds[j_idx],
        "match_score": score,
        "match_label": label
    })

# Write to file
import os
os.makedirs("dataset", exist_ok=True)
with open("dataset/resumeJD_pairs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["resume_text", "job_description", "match_score", "match_label"])
    writer.writeheader()
    writer.writerows(data)

print("Mock dataset generated successfully at dataset/resumeJD_pairs.csv")
