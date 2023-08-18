
export function authenticateUserWithMetaMask() {
  // Check if MetaMask is installed and the wallet is unlocked
  if (mm.checkMetamask() && mm.checkIsLocked()) {
    const userWalletAddress = mm.getConnectedAccounts();

    // Request a challenge from the server
    return axios.post('/request_challenge', { wallet_address: userWalletAddress })
      .then(response => {
        const challenge = response.data.challenge;

        // Sign the challenge using MetaMask
        return mm.connectWallet()
          .then(() => {
            return ethereum.request({
              method: 'personal_sign',
              params: [challenge, userWalletAddress]
            });
          })
          .then(signature => {
            // Send the signature to the server for verification
            return axios.post('/verify_signature', { wallet_address: userWalletAddress, signature: signature });
          });
      });
  } else {
    throw new Error('MetaMask is not installed or the wallet is locked.');
  }
}
