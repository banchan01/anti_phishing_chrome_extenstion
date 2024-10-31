document.addEventListener('DOMContentLoaded', function() {
    // Get the current tab's information
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        const currentTab = tabs[0];
        
        // Display the URL
        document.getElementById('url-display').textContent = `URL: ${currentTab.url}`;
        
        // Get stored analysis data for this URL
        chrome.storage.local.get(['phishingData'], function(result) {
            if (result.phishingData) {
                const confidence = (result.phishingData.prediction_score * 100).toFixed(1);
                document.getElementById('confidence-display').textContent = 
                    `Confidence: ${confidence}% likely to be a phishing site`;
            }
        });
    });

    // Handle button clicks
    document.getElementById('goBack').addEventListener('click', function() {
        chrome.tabs.goBack();
        window.close();
    });

    document.getElementById('proceed').addEventListener('click', function() {
        window.close();
    });
});