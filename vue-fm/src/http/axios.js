import axios from 'axios';

const instance = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'https://msus1.megashares.com', // Use the environment variable
  // other configurations
});

axios.post('/request_challenge', { wallet_address: userWalletAddress })
    .then(response => {
        const challenge = response.data.challenge;
        // Sign the challenge using the user's private key (Web3.js can be used for this)
        const signature = web3.eth.sign(challenge, userWalletAddress);
        
        // Send the signature to the server for verification
        axios.post('/verify_signature', { wallet_address: userWalletAddress, signature: signature })
            .then(response => {
                if (response.data.status === 'success') {
                    // User is authenticated
                } else {
                    // Handle error
                }
            });
    });
    


export default instance;