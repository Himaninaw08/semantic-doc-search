# utils/dataset_generator.py
"""
Creates data/sample_docs.csv with synthetic content for testing.
Fields: title,text
"""
import csv
import os

OUT = "data/sample_docs.csv"

SAMPLES = [
    {
        "title": "How to reset your password",
        "text": "If you've forgotten your password, go to the account settings page and click 'Reset password'. You'll receive an email with a link to set a new password. The link expires in 24 hours."
    },
    {
        "title": "Company benefits overview",
        "text": "Employees are eligible for medical insurance after 30 days. The plan covers doctor visits, hospitalization, and dental up to specified limits. Employee contributions are deducted monthly."
    },
    {
        "title": "Onboarding steps for new hires",
        "text": "Welcome to the company! Steps: 1) Complete HR paperwork; 2) Setup work email and tools; 3) Attend orientation; 4) Meet team. Your manager will assign training modules."
    },
    {
        "title": "Getting started with the API",
        "text": "Our REST API supports JSON requests. Base URL: https://api.example.com/v1. Authenticate using an API key passed via the Authorization header. See docs for endpoint details."
    },
    {
        "title": "Troubleshooting VPN connection",
        "text": "If the VPN won't connect, check your network, ensure credentials are correct, and restart the VPN client. If issues persist, collect logs and contact IT with the error code."
    }
]

def main():
    os.makedirs("data", exist_ok=True)
    with open(OUT, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "text"])
        writer.writeheader()
        for s in SAMPLES:
            writer.writerow(s)
    print(f"Wrote sample data to {OUT}")

if __name__ == "__main__":
    main()
