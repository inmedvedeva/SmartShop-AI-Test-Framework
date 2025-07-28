# Applitools Eyes Setup Guide

## 🚀 Quick Setup

### 1. Get API Key
1. Visit [https://applitools.com/](https://applitools.com/)
2. Sign up for a free account
3. Go to your account settings
4. Copy your API key

### 2. Configure in Project
```bash
# Run setup script
python scripts/setup_applitools.py

# Or manually edit .env file
APPLITOOLS_API_KEY=your-api-key-here
APPLITOOLS_APP_NAME=SmartShop_AI_Tests
```

### 3. Test Setup
```bash
# Run visual tests
pytest tests/visual/

# Run demo
python examples/applitools_example.py
```

## 🎯 What You Get

### AI-Powered Visual Testing
- **Smart change detection** - Ignores minor changes (time, animations)
- **Critical issue detection** - Flags important UI changes
- **Automatic baseline management** - No manual baseline setup
- **Cross-browser testing** - Test on multiple browsers simultaneously

### Key Features
- ✅ **Baseline creation** - First run creates reference images
- ✅ **Visual comparison** - Compare with baseline on subsequent runs
- ✅ **Region testing** - Test specific areas of the page
- ✅ **Responsive testing** - Test on different screen sizes
- ✅ **AI analysis** - Intelligent difference detection
- ✅ **Detailed reporting** - Comprehensive visual test reports

## 🔧 Configuration Options

### Environment Variables
```bash
APPLITOOLS_API_KEY=your-api-key
APPLITOOLS_APP_NAME=SmartShop_AI_Tests
APPLITOOLS_BATCH_NAME=Visual_Regression_Tests
APPLITOOLS_BATCH_ID=unique-batch-id
```

### Test Configuration
```python
# In your test files
@pytest.mark.visual
@pytest.mark.applitools
class TestVisualRegression:
    def test_home_page_visual(self):
        result = self.visual_tester.check_page_layout("home_page", self.driver)
        assert result['status'] in ['passed', 'baseline_created']
```

## 📊 Understanding Results

### Test Statuses
- **`baseline_created`** - First run, baseline saved
- **`passed`** - No visual differences detected
- **`failed`** - Visual differences found
- **`error`** - Technical error occurred

### Result Object
```python
{
    "status": "failed",
    "differences": {
        "total_differences": 5,
        "difference_percentage": 2.3,
        "critical_changes": 2,
        "minor_changes": 3
    },
    "diff_image": "/path/to/diff.png",
    "recommendations": ["Check header changes", "Verify element visibility"]
}
```

## 🎨 Advanced Usage

### Region-Specific Testing
```python
# Test only header area
header_region = (x, y, width, height)
result = self.visual_tester.check_page_layout("header", driver, region=header_region)
```

### Responsive Testing
```python
# Test on different screen sizes
screen_sizes = [(1920, 1080), (768, 1024), (375, 667)]
for width, height in screen_sizes:
    driver.set_window_size(width, height)
    result = self.visual_tester.check_page_layout(f"responsive_{width}x{height}", driver)
```

### Cross-Browser Testing
```python
# Test on multiple browsers
browsers = ['chrome', 'firefox', 'safari']
for browser in browsers:
    # Setup driver for browser
    result = self.visual_tester.check_page_layout(f"cross_browser_{browser}", driver)
```

## 🔍 Troubleshooting

### Common Issues

#### "Applitools not available"
```bash
# Install Applitools package
pip install eyes-selenium

# Check API key
python scripts/setup_applitools.py
```

#### "Connection error"
- Verify API key is correct
- Check internet connection
- Ensure Applitools service is available

#### "Baseline not created"
- First run should create baseline automatically
- Check write permissions for screenshot directory
- Verify API key has proper permissions

### Fallback Mode
If Applitools is unavailable, the framework falls back to basic image comparison:
- Uses OpenCV for pixel comparison
- Local screenshot storage
- Basic difference detection
- No AI analysis

## 📚 Additional Resources

- [Applitools Documentation](https://applitools.com/docs/)
- [Visual Testing Best Practices](https://applitools.com/blog/visual-testing-best-practices/)
- [API Reference](https://applitools.com/docs/api/)
- [Community Support](https://community.applitools.com/)

## 🎉 Next Steps

1. **Run your first visual test**: `pytest tests/visual/`
2. **Explore the dashboard**: View results in Applitools dashboard
3. **Add visual tests**: Integrate visual testing into your existing tests
4. **Configure CI/CD**: Add visual testing to your pipeline
5. **Customize settings**: Adjust sensitivity and match levels

Happy visual testing! 🎨✨
