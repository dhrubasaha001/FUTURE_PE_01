document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('seoForm');
    const generateBtn = document.getElementById('generateBtn');
    const resultsSection = document.getElementById('resultsSection');
    const loader = document.getElementById('loader');
    
    // Tab Elements
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    // Tab Switching Logic
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));
            
            // Add active class to clicked
            btn.classList.add('active');
            const targetId = btn.getAttribute('data-tab');
            document.getElementById(targetId).classList.add('active');
        });
    });

    // Form Submission Logic
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const topic = document.getElementById('topic').value;
        const businessName = document.getElementById('businessName').value;
        const location = document.getElementById('location').value;
        const targetAudience = document.getElementById('targetAudience').value;

        // Show loading state
        resultsSection.style.display = 'none';
        loader.style.display = 'flex';
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<ion-icon name="hourglass-outline"></ion-icon> Generating...';

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    topic,
                    business_name: businessName,
                    location,
                    target_audience: targetAudience
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Populate tabs with HTML returned by AI
                document.getElementById('outline').innerHTML = data.outline || '<p>No outline generated.</p>';
                document.getElementById('blog').innerHTML = data.blog || '<p>No blog content generated.</p>';
                document.getElementById('cluster').innerHTML = data.cluster || '<p>No content cluster generated.</p>';
                document.getElementById('local').innerHTML = data.local_seo || '<p>No local SEO generated.</p>';

                // Show Results
                loader.style.display = 'none';
                resultsSection.style.display = 'flex';
                
                // Select first tab
                tabBtns[0].click();
            } else {
                alert(`Error: ${data.error}`);
                loader.style.display = 'none';
            }
        } catch (error) {
            alert('A network error occurred. Please try again.');
            console.error(error);
            loader.style.display = 'none';
        }

        // Reset Button
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<ion-icon name="sparkles-outline"></ion-icon> Generate SEO Pack';
    });
});
