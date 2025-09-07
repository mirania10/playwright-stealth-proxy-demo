# Playwright Stealth Proxy Demo

A production-ready GitHub Actions workflow for human-like browsing automation using Playwright with comprehensive stealth capabilities, proxy support, and anti-detection measures.

## Features

🎭 **Playwright Stealth Integration**
- Full Playwright stealth plugin integration
- Comprehensive anti-detection measures
- Non-headless browser for realistic behavior

🌐 **Proxy Support**
- HTTP/HTTPS proxy configuration
- Authentication with username/password
- Environment-based proxy settings

🤖 **Human Behavior Simulation**
- Realistic mouse movements and scrolling
- Variable timing patterns
- Natural interaction sequences
- Reading pause simulation

⚙️ **Production Ready**
- Comprehensive error handling
- Detailed logging with artifacts
- Configurable via environment variables
- GitHub Actions workflow automation

## Repository Structure

```
├── .github/workflows/
│   └── browse-as-human.yml    # GitHub Actions workflow
├── automation/
│   ├── requirements.txt       # Python dependencies
│   └── browse_human.py       # Main automation script
└── README.md                 # This file
```

## Quick Start

### 1. Set Up Repository Secrets

Go to your repository **Settings** → **Secrets and variables** → **Actions** and add the following secrets:

#### Required Proxy Secrets
```
PROXY_HOST=your.proxy.host
PROXY_PORT=8080
PROXY_USERNAME=your_proxy_username
PROXY_PASSWORD=your_proxy_password
```

#### Optional Configuration Secrets
```
TIMEZONE=America/New_York
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
VIEWPORT_WIDTH=1920
VIEWPORT_HEIGHT=1080
LOCALE=en-US
```

### 2. Manual Workflow Execution

1. Go to **Actions** tab in your GitHub repository
2. Select "Browse as Human Simulation" workflow
3. Click "Run workflow"
4. Configure parameters:
   - **Target URL**: Default is `https://creditBPO.com`
   - **Duration**: Default is `5` minutes
5. Click "Run workflow"

### 3. Scheduled Execution

The workflow is configured to run automatically:
- **Daily at 10:00 UTC** (configurable in `.github/workflows/browse-as-human.yml`)

## Configuration Guide

### Environment Variables

The automation script supports extensive configuration via environment variables:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `TARGET_URL` | Website to browse | `https://creditBPO.com` | No |
| `DURATION_MINUTES` | How long to browse | `5` | No |
| `PROXY_HOST` | Proxy server hostname | - | Yes (for proxy) |
| `PROXY_PORT` | Proxy server port | - | Yes (for proxy) |
| `PROXY_USERNAME` | Proxy authentication username | - | No |
| `PROXY_PASSWORD` | Proxy authentication password | - | No |
| `TIMEZONE` | Browser timezone | `America/New_York` | No |
| `USER_AGENT` | Browser user agent | Auto-generated | No |
| `VIEWPORT_WIDTH` | Browser window width | `1920` | No |
| `VIEWPORT_HEIGHT` | Browser window height | `1080` | No |
| `LOCALE` | Browser locale | `en-US` | No |

### Workflow Customization

Edit `.github/workflows/browse-as-human.yml` to customize:

```yaml
# Change schedule (currently daily at 10:00 UTC)
schedule:
  - cron: '0 10 * * *'  # Change this cron expression

# Modify default inputs
inputs:
  target_url:
    default: 'https://your-target-site.com'  # Change default URL
  duration_minutes:
    default: '10'  # Change default duration
```

## Local Development

### Prerequisites

- Python 3.8+
- pip package manager

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/playwright-stealth-proxy-demo.git
   cd playwright-stealth-proxy-demo
   ```

2. **Install dependencies**:
   ```bash
   cd automation
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**:
   ```bash
   playwright install chromium
   ```

4. **Set up environment variables**:
   ```bash
   export TARGET_URL="https://example.com"
   export DURATION_MINUTES="3"
   export PROXY_HOST="your.proxy.host"
   export PROXY_PORT="8080"
   export PROXY_USERNAME="your_username"
   export PROXY_PASSWORD="your_password"
   ```

5. **Run the script**:
   ```bash
   python browse_human.py
   ```

## Advanced Features

### Anti-Detection Measures

The script implements comprehensive anti-detection techniques:

- **Browser fingerprint randomization**
- **Realistic user agent rotation**
- **JavaScript injection to mask automation**
- **Natural timing patterns**
- **Viewport and locale randomization**
- **Plugin and language spoofing**

### Human Behavior Simulation

- **Variable scroll patterns**: Up/down scrolling with realistic amounts
- **Mouse movement simulation**: Natural cursor movements across the page
- **Reading pauses**: Longer delays to simulate content reading
- **Interaction randomization**: Random combination of actions
- **Realistic timing**: Gamma distribution for natural delays

### Logging and Monitoring

- **Comprehensive logging**: All actions logged with timestamps
- **Error handling**: Graceful error recovery and reporting
- **Progress tracking**: Regular updates on simulation progress
- **Artifact collection**: Logs automatically uploaded as GitHub Actions artifacts

## Troubleshooting

### Common Issues

#### 1. Proxy Connection Failed
```
Error: Proxy connection failed
```
**Solution**: Verify proxy credentials and connectivity:
- Check `PROXY_HOST` and `PROXY_PORT` values
- Verify `PROXY_USERNAME` and `PROXY_PASSWORD` if authentication required
- Test proxy connectivity from your network

#### 2. Browser Launch Failed
```
Error: Failed to launch browser
```
**Solution**: 
- Ensure Playwright browsers are installed: `playwright install chromium`
- Check system dependencies (especially in CI environments)
- Verify sufficient system resources

#### 3. Target Site Unreachable
```
Error: Navigation timeout
```
**Solution**:
- Verify target URL accessibility
- Check proxy configuration if using proxy
- Increase timeout values if needed

### Debug Mode

Enable verbose logging by modifying the script:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    # ... rest of config
)
```

## Security Considerations

- **Never commit credentials**: Always use GitHub Secrets for sensitive data
- **Proxy security**: Use HTTPS proxies when possible
- **Rate limiting**: Be respectful of target sites' resources
- **Legal compliance**: Ensure compliance with target sites' terms of service

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -m 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## License

This project is provided as-is for educational and demonstration purposes. Please ensure compliance with all applicable laws and terms of service when using this code.

## Support

For issues and questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Search existing [GitHub Issues](../../issues)
3. Create a new issue with detailed information

---

**⚠️ Disclaimer**: This tool is for educational and testing purposes. Always respect robots.txt, rate limits, and terms of service of target websites. Users are responsible for ensuring their usage complies with all applicable laws and regulations.
