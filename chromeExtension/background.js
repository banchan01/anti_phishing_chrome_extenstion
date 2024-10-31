chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url) {
        // Check for browser-specific URLs that should be ignored
        const ignoredUrls = [
            'chrome://',
            'chrome-extension://',
            'edge://',
            'about:',
            'firefox:',
            'opera:',
            'view-source:',
            'file:',
            'localhost',
            '127.0.0.1'
        ];

        // Check if URL should be ignored
        const shouldIgnore = ignoredUrls.some(url => tab.url.startsWith(url));

        if (!shouldIgnore) {
            checkUrl(tab.url).then(result => {
                if (result) {
                    // Store the result for the popup to access
                    chrome.storage.local.set({ phishingData: result });

                    // Send results to content script
                    chrome.tabs.sendMessage(tabId, {
                        type: 'PHISHING_CHECK_RESULT',
                        data: result
                    });

                    // If it's a phishing site, show the popup
                    if (result.is_phishing) {
                        chrome.action.setPopup({ popup: 'popup.html' });
                        chrome.action.setBadgeText({ text: '⚠️' });
                        chrome.action.setBadgeBackgroundColor({ color: '#d32f2f' });
                    }
                }
            });
        }
    }
});