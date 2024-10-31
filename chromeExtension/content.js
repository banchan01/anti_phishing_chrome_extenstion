function showNotification(data) {  // Changed parameter name from features to data
    let notification = document.getElementById('phishing-notification');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'phishing-notification';
        notification.style.cssText = `
            position: fixed;
            top: 10px;
            right: 10px;
            padding: 15px;
            background: white;
            border: 2px solid ${data.is_phishing ? '#d32f2f' : '#2e7d32'};
            border-radius: 5px;
            z-index: 10000;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            font-family: Arial, sans-serif;
            max-width: 300px;
        `;
        document.body.appendChild(notification);
    }

    notification.innerHTML = `
        <h3 style="margin: 0 0 10px 0; color: ${data.is_phishing ? '#d32f2f' : '#2e7d32'}">
            ${data.message}
        </h3>
        <p style="margin: 5px 0">Confidence: ${(data.prediction_score * 100).toFixed(1)}%</p>
        <p style="margin: 5px 0">URL Length: ${data.features.length_url}</p>
        <p style="margin: 5px 0">Dots in URL: ${data.features.nb_dots}</p>
        <p style="margin: 5px 0">Google Indexed: ${data.features.google_index ? 'Yes' : 'No'}</p>
        <p style="margin: 5px 0">Page Rank: ${data.features.page_rank}</p>
        <button id="close-notification" style="
            position: absolute;
            top: 5px;
            right: 5px;
            border: none;
            background: none;
            cursor: pointer;
            font-size: 20px;
            color: #666;
            padding: 5px;
            line-height: 1;
        ">×</button>
    `;

    // Remove old event listener if exists
    const closeButton = document.getElementById('close-notification');
    const newCloseButton = closeButton.cloneNode(true);
    closeButton.parentNode.replaceChild(newCloseButton, closeButton);
    
    newCloseButton.addEventListener('click', () => {
        notification.remove();
    });
}

// Add message listener
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'PHISHING_CHECK_RESULT') {
        showNotification(message.data);
    }
});