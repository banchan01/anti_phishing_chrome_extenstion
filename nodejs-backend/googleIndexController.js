async function getGoogleIndex(url) {
    try {
        const apiKey = process.env.GOOGLE_API_KEY;
        const cx = process.env.GOOGLE_SEARCH_ENGINE_ID;
        
        const searchUrl = `https://www.googleapis.com/customsearch/v1?key=${apiKey}&cx=${cx}&q=site:${encodeURIComponent(url)}`;
        
        const response = await fetch(searchUrl);
        const data = await response.json();
        
        const isIndexed = data.searchInformation?.totalResults > 0;
        console.log('Search results:', {
            url,
            totalResults: data.searchInformation?.totalResults,
            isIndexed
        });
        
        return { isIndexed: isIndexed ? 1 : 0 };
    } catch (error) {
        console.error('Google Index Error:', error);
        return { isIndexed: 0 };
    }
};

export default getGoogleIndex;