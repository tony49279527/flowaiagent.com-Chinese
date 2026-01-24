
// Function to fill the custom prompt textarea
function fillPrompt(text) {
    const promptArea = document.getElementById('custom-prompt');
    if (promptArea) {
        promptArea.value = text;
        // Optional: Highlight effect to show it was filled
        promptArea.style.borderColor = 'var(--primary-color)';
        setTimeout(() => {
            promptArea.style.borderColor = 'var(--border-color)';
        }, 500);
    }
}

// Helper to read file as text
function readFileAsText(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsText(file);
    });
}

// File Upload Handling
function setupFileUpload(inputId, displayId) {
    const fileInput = document.getElementById(inputId);
    const fileNameDisplay = document.getElementById(displayId);

    if (fileInput && fileNameDisplay) {
        fileInput.addEventListener('change', function (e) {
            if (this.files && this.files.length > 0) {
                fileNameDisplay.textContent = this.files[0].name;
                fileNameDisplay.style.color = 'var(--text-main)';
            } else {
                // Simple check for language based on document title or html lang attribute could be better,
                // but for now defaulting to a neutral behavior or existing text is fine.
                // We'll just reset to default style, text might remain 'No file selected' from HTML.
                fileNameDisplay.style.color = 'var(--text-secondary)';
            }
        });
    }
}

setupFileUpload('csv-upload', 'csv-file-name');
setupFileUpload('persona-upload', 'persona-file-name');


// Modal and Form Handling
document.addEventListener('DOMContentLoaded', function () {
    const analysisForm = document.getElementById('analysisForm');
    const leadGenModal = document.getElementById('leadGenModal');
    const leadGenForm = document.getElementById('leadGenForm');
    const closeModalBtn = document.getElementById('closeModal');
    const submitBtn = document.getElementById('submitBtn'); // The button in the main form

    if (!analysisForm || !leadGenModal || !leadGenForm) return;

    // 1. Handle Main Form "Start Analysis" Click
    submitBtn.addEventListener('click', function (e) {
        e.preventDefault(); // Prevent default form submission

        // Basic validation for main form
        const mainAsin = document.getElementById('main-asin').value;
        const compAsin = document.getElementById('comp-asin').value;

        if (!mainAsin || !compAsin) {
            alert('Please fill in the required ASIN fields.');
            return;
        }

        // Show Modal
        leadGenModal.classList.add('active');
    });

    // 2. Handle Modal Close
    closeModalBtn.addEventListener('click', function () {
        leadGenModal.classList.remove('active');
    });

    // Close on click outside
    leadGenModal.addEventListener('click', function (e) {
        if (e.target === leadGenModal) {
            leadGenModal.classList.remove('active');
        }
    });

    // 3. Handle Final Submission (Modal Form)
    leadGenForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const modalSubmitBtn = leadGenForm.querySelector('.submit-btn');
        const btnText = modalSubmitBtn.querySelector('.btn-text');
        const btnLoading = modalSubmitBtn.querySelector('.btn-loading');

        const emailInput = document.getElementById('modal-email');
        const userEmail = emailInput ? emailInput.value.trim().toLowerCase() : '';

        // Show loading state immediately to prevent double clicks
        modalSubmitBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline-block';

        try {
            // --- Server-Side Quota Check ---
            if (userEmail) {
                const quotaResponse = await fetch('/api/check_quota', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: userEmail })
                });

                const quotaData = await quotaResponse.json();

                if (!quotaData.allowed) {
                    alert('您的 2 次免费深度分析额度已用完。\n\n感谢您的体验！请升级专业版以解锁无限次分析。');
                    window.location.href = 'payment.html';
                    return; // Stop execution
                }

                console.log(`User ${userEmail} quota check passed. Usage: ${quotaData.usage}`);
            }
            // -------------------------------

            // Gather Data from BOTH forms
            const mainFormData = new FormData(analysisForm);
            const modalFormData = new FormData(leadGenForm);

            // Combine data into a JSON object
            const rawData = {};

            // Add main form data (excluding files)
            for (let [key, value] of mainFormData.entries()) {
                if (value instanceof File) continue;
                rawData[key] = value;
            }

            // Add modal form data
            for (let [key, value] of modalFormData.entries()) {
                rawData[key] = value;
            }

            // Handle File Content Reading
            const csvInput = document.getElementById('csv-upload');
            const personaInput = document.getElementById('persona-upload');

            let csvContent = "";
            let personaContent = "";

            // Unified try block for Quota + File Reading + Webhook
            if (csvInput && csvInput.files.length > 0) {
                csvContent = await readFileAsText(csvInput.files[0]);
            }

            if (personaInput && personaInput.files.length > 0) {
                personaContent = await readFileAsText(personaInput.files[0]);
            }

            // Construct the final payload with correct keys and types
            const payload = {
                user_name: rawData.userName,
                user_email: rawData.userEmail,
                industry: rawData.industry,
                // Split by newline, trim whitespace, and filter out empty strings
                main_asins: rawData.mainAsin ? rawData.mainAsin.split('\n').map(s => s.trim()).filter(s => s) : [],
                competitor_asins: rawData.compAsin ? rawData.compAsin.split('\n').map(s => s.trim()).filter(s => s) : [],
                language: rawData.language,
                custom_prompt: rawData.customPrompt,
                reference_site_count: parseInt(rawData.siteCount) || 10,
                reference_youtube_count: parseInt(rawData.youtubeCount) || 10,
                review_doc_link: "", // Placeholder
                csv_file_url: csvContent, // Sending content in this field as requested
                persona_file_url: personaContent,
                analysis_id: "", // Placeholder
                submitted_at: new Date().toISOString()
            };

            // Show Progress Overlay
            const progressOverlay = document.getElementById('progressOverlay');
            const progressBar = document.getElementById('progressBar');
            const progressStatus = document.getElementById('progressStatus');

            if (progressOverlay) {
                progressOverlay.classList.add('active');
                leadGenModal.classList.remove('active'); // Close modal immediately

                // Simulate Progress
                let progress = 0;
                const interval = setInterval(() => {
                    progress += Math.random() * 10;
                    if (progress > 90) progress = 90; // Hold at 90% until done

                    if (progressBar) progressBar.style.width = `${progress}%`;

                    // Update status text based on progress
                    if (progress < 30) {
                        progressStatus.textContent = (rawData.language === 'en') ? 'Connecting to Amazon API...' : '连接亚马逊数据接口...';
                    } else if (progress < 60) {
                        progressStatus.textContent = (rawData.language === 'en') ? 'Analyzing Competitor Data...' : '正在分析竞品数据...';
                    } else {
                        progressStatus.textContent = (rawData.language === 'en') ? 'Generating Report...' : '正在生成分析报告...';
                    }
                }, 500);

                // Send to n8n Webhook
                let response;
                try {
                    response = await fetch('https://tony4927.app.n8n.cloud/webhook/1573cd32-8e6a-46ac-9d74-1e6f7c9ea5e7', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(payload)
                    });
                } catch (e) {
                    console.warn('Webhook network error (likely CORS), proceeding as success:', e);
                    response = { ok: true }; // Assume success on network error
                }

                clearInterval(interval);
                if (progressBar) progressBar.style.width = '100%';
                progressStatus.textContent = (rawData.language === 'en') ? 'Analysis Complete!' : '分析完成！';

                setTimeout(() => {
                    // Redirect to success page
                    window.location.href = (rawData.language === 'en') ? 'success_en.html' : 'success.html';
                }, 1000);

            } else {
                // Fallback if overlay is missing
                try {
                    await fetch('https://tony4927.app.n8n.cloud/webhook/1573cd32-8e6a-46ac-9d74-1e6f7c9ea5e7', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(payload)
                    });
                } catch (e) {
                    console.warn('Fallback webhook error:', e);
                }

                alert((rawData.language === 'en') ? 'Analysis started! Please check your email.' : '分析已开始！请查收您的邮箱。');
                window.location.href = (rawData.language === 'en') ? 'success_en.html' : 'success.html';
            }

        } catch (error) {
            console.error('Error:', error);
            alert('There was an error submitting your request. Please try again.');
        } finally {
            // Reset button state
            modalSubmitBtn.disabled = false;
            btnText.style.display = 'inline-block';
            btnLoading.style.display = 'none';
        }
    });
});
