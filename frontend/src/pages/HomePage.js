import React from 'react';

const HomePage = () => {
    function handleLogin() {
        const clientId = 'SamirCho-itemtrac-PRD-c4db2d93b-dd561dd4';
        const redirectUri = 'Samir_Chowdhury-SamirCho-itemtr-apwqznrun'  // 'Samir_Chowdhury-SamirCho-itemtr-hdghgnj';
        const scope = 'https://api.ebay.com/oauth/api_scope/sell.inventory';
        const authUrl = `https://auth.ebay.com/oauth2/authorize?client_id=${clientId}&response_type=code&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${encodeURIComponent(scope)}`;
        
        window.location.href = authUrl;
      }

    return (
        <div>
            <h1>Home Page</h1>
            <button onClick={handleLogin}>Login with eBay</button>
        </div>
    );
};

export default HomePage;