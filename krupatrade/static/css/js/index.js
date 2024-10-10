document.getElementById('verifyBtn').addEventListener('click', function() {
    const gstin = document.getElementById('gstin').value;
    const apiKey = 'eiYUAWE3dmV3tfzRqvfBrtYICKA2';
    const url = 'https://appyflow.in/api/verifyGST?gstNo=${gstin}&key_secret=${apiKey}';
    const loader = document.getElementById('loader');
    
    loader.style.display = 'block';

    fetch(url)
        .then(response => response.json())
        .then(data => {
            loader.style.display = 'none';
            if (!data.error) {
                const gstDetails = `
                    <strong>Owner Name:</strong> ${data.taxpayerInfo.lgnm}<br>
                    <strong>Shop Name:</strong> ${data.taxpayerInfo.tradeNam}<br>
                    <strong>Address:</strong> ${data.taxpayerInfo.pradr.addr.bno}, ${data.taxpayerInfo.pradr.addr.st}, ${data.taxpayerInfo.pradr.addr.loc}, ${data.taxpayerInfo.pradr.addr.dst}, ${data.taxpayerInfo.pradr.addr.stcd}, ${data.taxpayerInfo.pradr.addr.pncd}
                `;
                document.getElementById('gstDetails').innerHTML = gstDetails;
                document.getElementById('verifyBtn').style.display = 'none';
                document.getElementById('otpSection').classList.remove('hidden');
            } else {
                alert('GST Verification failed. Please try again.');
            }
        })
        .catch(error => {
            loader.style.display = 'none';
            alert('An error occurred during GST verification. Please try again later.');
        });
});
