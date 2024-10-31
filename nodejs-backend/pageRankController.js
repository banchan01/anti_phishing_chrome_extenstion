async function getPageRank(url) {
    try {
        const domain = new URL(url).hostname;
        
        const response = await fetch(
            `https://openpagerank.com/api/v1.0/getPageRank?domains[]=${domain}`,
            {
                headers: {
                    'API-OPR': process.env.OPENPAGE_API_KEY
                }
            }
        );
        
        const data = await response.json();
        
        if (data.status_code === 200 && data.response[0].status_code === 200) {
            return { pageRank: data.response[0].page_rank_decimal };
        } else {
            return { pageRank: 0 };
        }
    } catch (error) {
        console.error('PageRank Error:', error);
        return { pageRank: 0 };
    }
};

export default getPageRank;