document.addEventListener('DOMContentLoaded', async () => {
    const statusElement = document.getElementById('status');
    
    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        const url = tab.url;
        
        const response = await fetch('http://localhost:3000/api/check-url', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to check URL');
        }

        if (data) {
            const isPhishing = data.is_phishing === 1;
            statusElement.innerHTML = `
                <h3 style="color: ${isPhishing ? '#d32f2f' : '#2e7d32'}">
                    ${data.message}
                </h3>
                        ${data.is_phishing ? `
                <img src="${chrome.runtime.getURL('danger.png')}" 
                    alt="Danger Warning" 
                    style="width: 100%; margin-bottom: 10px; display: block;">
            ` : `
                <img src="${chrome.runtime.getURL('safe.png')}" 
                    alt="Safe" 
                    style="width: 100%; margin-bottom: 10px; display: block;">
            `}
                <p>URL: ${data.url}</p>
                <p>Page Rank: ${data.analysis.page_rank}</p>
                <p>Google Index: ${data.analysis.google_index}</p>
                <p>Prediction Score: ${(data.prediction_score * 100).toFixed(2)}%</p>
            `;
        } else {
            statusElement.textContent = "No analysis available for this page...";
        }
    } catch (error) {
        console.error("Error:", error);
        statusElement.textContent = "Error analyzing URL.";
    }
});