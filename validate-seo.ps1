# SEO Validation Script
# Run this script to check SEO optimization status across all HTML files

Write-Host "`n=== SEO VALIDATION REPORT ===" -ForegroundColor Cyan
Write-Host "Checking all HTML files for Google 2025 SEO compliance`n"

$htmlFiles = Get-ChildItem "C:/Users/12736/.gemini/antigravity/scratch/amz_ai_replica" -Filter "*.html"

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    
    Write-Host "`n--- $($file.Name) ---" -ForegroundColor Yellow
    
    # Check title tag length
    if ($content -match '<title>([^<]+)</title>') {
        $title = $Matches[1]
        $titleLen = $title.Length
        if ($titleLen -ge 50 -and $titleLen -le 60) {
            Write-Host "  Title: âœ" GOOD ($titleLen chars)" -ForegroundColor Green
        } elseif ($titleLen -gt 0) {
            Write-Host "  Title: âš  $titleLen chars (recommend 50-60)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  Title: âœ— MISSING" -ForegroundColor Red
    }
    
    # Check meta description
    if ($content -match 'name="description" content="([^"]+)"') {
        $desc = $Matches[1]
        $descLen = $desc.Length
        if ($descLen -ge 150 -and $descLen -le 160) {
            Write-Host "  Description: âœ" GOOD ($descLen chars)" -ForegroundColor Green
        } elseif ($descLen -gt 0) {
            Write-Host "  Description: âš  $descLen chars (recommend 150-160)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  Description: âœ— MISSING" -ForegroundColor Red
    }
    
    # Check viewport
    if ($content -match 'name="viewport"') {
        Write-Host "  Viewport: âœ" Present" -ForegroundColor Green
    } else {
        Write-Host "  Viewport: âœ— MISSING" -ForegroundColor Red
    }
    
    # Check structured data
    $schemaCount = ([regex]::Matches($content, '@type')).Count
    if ($schemaCount -gt 0) {
        Write-Host "  Structured Data: âœ" $schemaCount schema(s) found" -ForegroundColor Green
    } else {
        Write-Host "  Structured Data: âš  None found" -ForegroundColor Yellow
    }
}

Write-Host "`n`n=== VALIDATION COMPLETE ===" -ForegroundColor Cyan
Write-Host "Next: Test homepage schema at https://validator.schema.org/`n"
