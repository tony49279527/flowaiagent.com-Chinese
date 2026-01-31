/**
 * report-loader.js - Universal Report Rendering System
 * Loads Markdown content dynamically and handles TOC/UI.
 */

document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const reportId = urlParams.get('id');

    if (!reportId) {
        console.error('No report ID provided in URL.');
        return;
    }

    loadReport(reportId);
});

async function loadReport(id) {
    const reportBody = document.getElementById('report-body');
    const reportTitle = document.getElementById('dynamic-title');
    const reportDate = document.getElementById('dynamic-date');
    const reportCategory = document.getElementById('dynamic-category');
    const tocContainer = document.getElementById('toc-container');

    try {
        // 1. Fetch metadata to get the title
        const metadataResponse = await fetch('data/reports/index.json');
        const metadataList = await metadataResponse.json();
        const metadata = metadataList.find(r => r.id === id);

        if (metadata) {
            reportTitle.textContent = metadata.title;
            reportDate.textContent = '生成时间：' + metadata.date;
            document.title = metadata.title + ' | FlowAI Agent';
        }

        // 2. Fetch Markdown content
        const contentResponse = await fetch(`data/reports/${id}.md`);
        if (!contentResponse.ok) throw new Error('Report content not found');
        const markdown = await contentResponse.text();

        // 3. Render Markdown
        if (typeof marked === 'undefined') {
            console.error('marked.js not loaded');
            reportBody.innerHTML = '<p>Error: Markdown renderer not available.</p>';
            return;
        }

        // Configure marked to handle IDs for TOC (Universal compatibility)
        const renderer = new marked.Renderer();
        renderer.heading = function (arg1, arg2) {
            let text = '', level = 1;
            if (typeof arg1 === 'object' && arg1 !== null) {
                text = arg1.text || '';
                level = arg1.depth || 1;
            } else {
                text = arg1 || '';
                level = arg2 || 1;
            }
            // Ensure text is a string
            const safeText = String(text || '');
            const escapedText = safeText.toLowerCase().replace(/[^\w\u4e00-\u9fa5]+/g, '-');
            return `<h${level} id="${escapedText}" style="scroll-margin-top: 100px;">${safeText}</h${level}>`;
        };

        reportBody.innerHTML = marked.parse(markdown, { renderer: renderer });

        // 4. Generate TOC
        generateTOC(reportBody, tocContainer);

        // 5. Setup Features (PDF, Share)
        setupFeatures(metadata || { title: '分析报告', id: id });

    } catch (error) {
        console.error('Failed to load report:', error);
        reportBody.innerHTML = `<p style="color:red; pading:20px;">抱歉，报告加载失败: ${error.message}<br><small>${error.stack}</small></p>`;
    }

    // 6. Load Recommended Reports
    if (typeof loadRecommended === 'function') {
        loadRecommended(id);
    }
}

async function loadRecommended(currentId) {
    const container = document.getElementById('recommended-grid');
    if (!container) return;

    try {
        const response = await fetch('data/reports/index.json');
        const reports = await response.json();

        // Filter out current and pick random 2-3
        const others = reports.filter(r => r.id !== currentId);
        const shuffled = others.sort(() => 0.5 - Math.random());
        const selected = shuffled.slice(0, 3); // Show 3

        container.innerHTML = selected.map(report => `
            <a href="report.html?id=${report.id}" style="text-decoration: none; color: inherit;">
                <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; transition: transform 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.02);" onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform='none'">
                    <div style="height: 140px; background: #f1f5f9; position: relative; overflow: hidden;">
                        <img src="${report.cover || 'assets/default-cover.png'}" alt="${report.title}" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.9;">
                    </div>
                    <div style="padding: 16px;">
                        <h4 style="margin: 0 0 8px; font-size: 1rem; font-weight: 600; line-height: 1.4; color: #1e293b; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">${report.title}</h4>
                        <div style="font-size: 0.85rem; color: #64748b;">${report.date}</div>
                    </div>
                </div>
            </a>
        `).join('');

        if (selected.length === 0) {
            document.getElementById('recommended-section').style.display = 'none';
        }

    } catch (e) {
        console.error('Failed to load recommended:', e);
    }
}

function setupFeatures(data) {
    const downloadBtn = document.getElementById('download-pdf');
    const shareBtn = document.getElementById('share-report');
    const modal = document.getElementById('share-modal-overlay');
    const closeBtn = document.getElementById('close-share');
    const copyBtn = document.getElementById('copy-btn');
    const shareUrlInput = document.getElementById('share-url');

    // PDF Download
    if (downloadBtn) {
        downloadBtn.addEventListener('click', () => {
            window.print();
        });
    }

    // Share Functionality
    if (shareBtn) {
        shareBtn.addEventListener('click', () => {
            const currentUrl = window.location.href;
            shareUrlInput.value = currentUrl;

            // Generate QR Code
            const qrContainer = document.getElementById('qrcode');
            qrContainer.innerHTML = '';
            new QRCode(qrContainer, {
                text: currentUrl,
                width: 180,
                height: 180,
                colorDark: "#2c3e50",
                colorLight: "#ffffff",
                correctLevel: QRCode.CorrectLevel.H
            });

            // Native Share API if available (for mobile)
            if (navigator.share) {
                navigator.share({
                    title: data.title,
                    text: '查看这份由 FlowAI Agent 生成的深入竞品分析报告',
                    url: currentUrl,
                }).catch(err => {
                    console.log('Share error:', err);
                    modal.classList.add('active'); // fallback
                });
            } else {
                modal.classList.add('active');
            }
        });
    }

    if (closeBtn) closeBtn.addEventListener('click', () => modal.classList.remove('active'));
    if (copyBtn) {
        copyBtn.addEventListener('click', () => {
            shareUrlInput.select();
            document.execCommand('copy');
            copyBtn.textContent = '已复制';
            setTimeout(() => {
                copyBtn.textContent = '复制';
            }, 2000);
        });
    }

    // Close modal on click outside
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.classList.remove('active');
        });
    }
}

function generateTOC(contentEl, tocEl) {
    if (!tocEl) return;

    const headings = contentEl.querySelectorAll('h1, h2, h3');
    if (headings.length === 0) return;

    const tocList = document.createElement('ul');
    tocList.className = 'toc-list';

    headings.forEach((heading, index) => {
        const level = parseInt(heading.tagName.substring(1));
        if (level === 1 && index > 0) return; // Skip title if it's already in the header

        const li = document.createElement('li');
        li.className = `toc-item toc-level-${level}`;

        const a = document.createElement('a');
        a.href = '#' + heading.id;
        a.textContent = heading.textContent;
        a.addEventListener('click', (e) => {
            e.preventDefault();
            const targetElement = document.getElementById(heading.id);
            if (targetElement) {
                const offset = 100;
                const bodyRect = document.body.getBoundingClientRect().top;
                const elementRect = targetElement.getBoundingClientRect().top;
                const elementPosition = elementRect - bodyRect;
                const offsetPosition = elementPosition - offset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });

        li.appendChild(a);
        tocList.appendChild(li);
    });

    tocEl.innerHTML = '<h3>目录</h3>';
    tocEl.appendChild(tocList);

    // Initial highlight
    highlightTOC(headings);

    // Scroll highlight
    window.addEventListener('scroll', () => {
        highlightTOC(headings);
        updateProgressBar();
    });
}

function updateProgressBar() {
    const progressBar = document.getElementById('reading-progress');
    if (!progressBar) return;

    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    progressBar.style.width = scrolled + "%";
}

function highlightTOC(headings) {
    let currentId = '';
    headings.forEach(heading => {
        const top = heading.getBoundingClientRect().top;
        if (top < 150) {
            currentId = heading.id;
        }
    });

    const tocLinks = document.querySelectorAll('.toc-list a');
    tocLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + currentId) {
            link.classList.add('active');
        }
    });
}
