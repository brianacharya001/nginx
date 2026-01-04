# Add these triggers to your existing 'on' section
on:
  issues:
    types: [opened, closed]
  workflow_dispatch:

jobs:
  deploy-and-notify:
    runs-on: self-hosted
    steps:
      # ... [Your existing deployment steps] ...

      - name: Send Email on Success or Failure
        if: always() # Ensures the email is sent regardless of success or failure
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 465
          username: ${{ secrets.GMAIL_USER }}
          password: ${{ secrets.GMAIL_APP_PASSWORD }}
          subject: "GitHub Action Result: ${{ github.workflow }} - ${{ job.status }}"
          to: recipient@gmail.com
          from: GitHub Automation
          body: |
            Workflow run finished with status: ${{ job.status }}
            
            Details:
            - Repository: ${{ github.repository }}
            - Triggered by: ${{ github.actor }}
            - Action Link: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
            
            Issue Details (if applicable):
            - Title: ${{ github.event.issue.title || 'N/A' }}
            - Status: ${{ github.event.action || 'N/A' }}
