import re

# Read the broken index.html
with open(r'C:\Users\12736\.gemini\antigravity\scratch\amz_ai_replica\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the hero section start
hero_match = re.search(r'<section class="hero-section">', content)
if hero_match:
    hero_start = hero_match.start()
    # Get all content from hero section onwards
    hero_and_rest = content[hero_start:]
    
    # Create the correct header structure
    correct_header = '''<!DOCTYPE html>
<html lang="zh-CN">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>亚马逊AI竞品分析工具 - 深度挖掘评论与竞品数据 | 竞品分析助手</title>
    <meta name="description" content="竞品分析助手是一款基于AI的亚马逊竞品分析工具。自动抓取竞品核心参数，深度分析用户评论情感，提供差异化营销策略建议，助您打造爆款产品。">
    <meta name="keywords" content="亚马逊竞品分析, AI选品工具, 亚马逊评论分析, 竞品调研, 亚马逊运营工具">
    <link rel="icon" href="favicon.png" type="image/png">
    <link rel="stylesheet" href="styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
</head>

<body>
    <div class="app-container">
        <header class="main-header">
            <div class="logo-section">
                <div class="logo-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        class="lucide lucide-bot">
                        <path d="M12 8V4H8" />
                        <rect width="16" height="12" x="4" y="8" rx="2" />
                        <path d="M2 14h2" />
                        <path d="M20 14h2" />
                        <path d="M15 13v2" />
                        <path d="M9 13v2" />
                    </svg>
                </div>
                <span class="logo-text">AI 竞品分析 <span class="logo-sub">Amazon Analysis Platform</span></span>
            </div>
            <nav class="main-nav">
                <a href="index.html" class="nav-link active">首页</a>
                <a href="create.html" class="nav-link">创建分析</a>
                <a href="cases.html" class="nav-link">案例展示</a>
                <a href="blog.html" class="nav-link">博客</a>
            </nav>
            <div class="lang-switch">
                <a href="index_en.html" class="lang-btn">EN</a>
            </div>
        </header>

        <main class="main-content">
            '''
    
    # Combine correct header with the rest of the content
    fixed_content = correct_header + hero_and_rest
    
    # Write it back
    with open(r'C:\Users\12736\.gemini\antigravity\scratch\amz_ai_replica\index.html', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("Fixed index.html successfully")

# Now fix index_en.html
with open(r'C:\Users\12736\.gemini\antigravity\scratch\amz_ai_replica\index_en.html', 'r', encoding='utf-8') as f:
    content_en = f.read()

hero_match_en = re.search(r'<section class="hero-section">', content_en)
if hero_match_en:
    hero_start_en = hero_match_en.start()
    hero_and_rest_en = content_en[hero_start_en:]
    
    correct_header_en = '''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Competitor Analysis - Amazon Analysis Platform</title>
    <link rel="icon" href="favicon.png" type="image/png">
    <link rel="stylesheet" href="styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
</head>

<body>
    <div class="app-container">
        <header class="main-header">
            <div class="logo-section">
                <div class="logo-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        class="lucide lucide-bot">
                        <path d="M12 8V4H8" />
                        <rect width="16" height="12" x="4" y="8" rx="2" />
                        <path d="M2 14h2" />
                        <path d="M20 14h2" />
                        <path d="M15 13v2" />
                        <path d="M9 13v2" />
                    </svg>
                </div>
                <span class="logo-text">AI Analysis <span class="logo-sub">Amazon Analysis Platform</span></span>
            </div>
            <nav class="main-nav">
                <a href="index_en.html" class="nav-link active">Home</a>
                <a href="create_en.html" class="nav-link">Create Analysis</a>
                <a href="cases_en.html" class="nav-link">Case Studies</a>
                <a href="blog_en.html" class="nav-link">Blog</a>
            </nav>
            <div class="lang-switch">
                <a href="index.html" class="lang-btn">中</a>
            </div>
        </header>

        <main class="main-content">
            '''
    
    fixed_content_en = correct_header_en + hero_and_rest_en
    
    with open(r'C:\Users\12736\.gemini\antigravity\scratch\amz_ai_replica\index_en.html', 'w', encoding='utf-8') as f:
        f.write(fixed_content_en)
    
    print("Fixed index_en.html successfully")

print("All files fixed!")
