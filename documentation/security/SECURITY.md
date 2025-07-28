# Security Guidelines for SmartShop AI Test Framework

## 🔒 Security Overview

This document outlines security best practices and guidelines for the SmartShop AI Test Framework to ensure sensitive data and credentials are properly protected.

## 🚨 Critical Security Files

### Files that should NEVER be committed to Git:

1. **Environment Files**
   - `.env` - Contains API keys and secrets
   - `.env.local` - Local environment overrides
   - `.env.production` - Production environment variables
   - `.env.staging` - Staging environment variables

2. **API Keys and Credentials**
   - `secrets.json` - API keys and tokens
   - `credentials.json` - Service account credentials
   - `*.key` - Private key files
   - `*.pem` - Certificate files
   - `api_keys.txt` - API key listings

3. **Database Files**
   - `*.db` - SQLite databases
   - `*.sqlite` - SQLite database files
   - `database/` - Database directories

4. **Log Files**
   - `*.log` - Application logs
   - `logs/` - Log directories
   - `reports/logs/` - Test execution logs

5. **Test Artifacts**
   - `reports/screenshots/` - Test screenshots
   - `reports/allure-results/` - Allure test results
   - `reports/html/` - HTML test reports

## ✅ Security Checklist

### Before Committing Code:

- [ ] No `.env` files in repository
- [ ] No API keys in code or comments
- [ ] No database files committed
- [ ] No log files with sensitive data
- [ ] No screenshots with personal information
- [ ] No credentials in demo scripts
- [ ] `.gitignore` is properly configured
- [ ] Pre-commit hooks are installed

### Environment Setup:

- [ ] Copy `env_example.txt` to `.env`
- [ ] Fill in your actual API keys in `.env`
- [ ] Never commit `.env` file
- [ ] Use different keys for different environments

## 🔐 API Key Management

### OpenAI API Key:
```bash
# In .env file (DO NOT COMMIT)
OPENAI_API_KEY=sk-your-actual-key-here
```

### Other API Keys:
```bash
# Applitools API Key
APPLITOOLS_API_KEY=your-applitools-key

# Database Credentials
DB_PASSWORD=your-db-password

# Email/Slack Notifications
SMTP_PASSWORD=your-smtp-password
SLACK_WEBHOOK_URL=your-slack-webhook
```

## 🛡️ Security Best Practices

### 1. Environment Variables
- Always use environment variables for sensitive data
- Never hardcode secrets in source code
- Use different keys for development/staging/production

### 2. API Key Rotation
- Regularly rotate API keys
- Use least privilege principle
- Monitor API usage for anomalies

### 3. Test Data
- Use fake data for testing
- Never use real user data in tests
- Sanitize any real data before logging

### 4. Logging
- Never log sensitive information
- Use log levels appropriately
- Rotate log files regularly

### 5. File Permissions
- Set appropriate file permissions
- Restrict access to sensitive files
- Use secure file transfer methods

## 🚨 Security Alerts

### If you accidentally commit sensitive data:

1. **Immediate Actions:**
   - Remove the file from Git history
   - Rotate any exposed credentials
   - Check for unauthorized access

2. **Git Commands to Remove Sensitive Files:**
   ```bash
   # Remove file from Git history
   git filter-branch --force --index-filter \
   'git rm --cached --ignore-unmatch .env' \
   --prune-empty --tag-name-filter cat -- --all

   # Force push to remove from remote
   git push origin --force --all
   ```

3. **Notify Team:**
   - Inform team members immediately
   - Document the incident
   - Update security procedures

## 🔍 Security Scanning

### Automated Security Checks:

1. **Pre-commit Hooks:**
   - Bandit security scanner
   - Safety dependency checker
   - Custom security validators

2. **CI/CD Security:**
   - Automated vulnerability scanning
   - Dependency security checks
   - Secret detection

3. **Manual Security Review:**
   - Code review for security issues
   - Configuration security audit
   - Access control verification

## 📋 Security Configuration

### .gitignore Security Section:
```gitignore
# Environment variables
.env*
*.env

# API Keys and secrets
secrets/
*.key
*.pem
credentials.json

# Database files
*.db
*.sqlite*

# Logs
*.log
logs/

# Test artifacts
reports/screenshots/
reports/allure-results/
```

### Pre-commit Security Hooks:
```yaml
- repo: https://github.com/pycqa/bandit
  rev: v1.7.5
  hooks:
    - id: bandit
      args: [-r, ., -f, json, -o, reports/security-scan.json]
```

## 🆘 Emergency Contacts

### Security Issues:
- Create a security issue in the repository
- Contact the project maintainer immediately
- Document the incident thoroughly

### API Key Compromise:
- Rotate the compromised key immediately
- Check for unauthorized usage
- Update all environment files
- Notify team members

## 📚 Additional Resources

- [GitHub Security Best Practices](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure)
- [OpenAI API Security](https://platform.openai.com/docs/guides/safety-best-practices)
- [Python Security Best Practices](https://python-security.readthedocs.io/)

---

**Remember: Security is everyone's responsibility!**

Last updated: July 19, 2025
