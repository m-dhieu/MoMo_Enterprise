/**
 * File Name:   chart_handler.js
 * Description: Fetches Mobile Money transactions from backend API
 *              with Basic Auth process and bucket data, and renders 
 *              interactive charts using Chart.js
 * Author:      Monica Dhieu             
 */

// API endpoint for fetching transactions
const API_URL = 'http://localhost:8090/transactions';

// prompt user for credentials or retrieve if stored in locally
// return null if missing input
function getStoredCredentials() {
    let creds = localStorage.getItem('momoAuth');
    if (!creds) {
        const username = prompt("Enter username:");
        const password = prompt("Enter password:");
        if (!username || !password) {
            alert("Credentials are required to access data.");
            return null;
        }
        creds = btoa(`${username}:${password}`);
        localStorage.setItem('momoAuth', creds);
    }
    return creds;
}

// fetch request with basic authentication header
function fetchWithStoredAuth(url) {
    const creds = getStoredCredentials();
    if (!creds) return Promise.reject('No credentials provided');
    const headers = new Headers();
    headers.append('Authorization', `Basic ${creds}`);
    return fetch(url, { headers });
}

// extract YYYY-MM-DD date string from a DateTime string
function getDateOnly(dtString) {
    return dtString.slice(0, 10);
}

// bucket transaction amounts into predefined ranges & return bucket counts
function bucketAmounts(transactions) {
    const buckets = {
        '0-5,000': 0,
        '5,001-10,000': 0,
        '10,001-20,000': 0,
        '20,001-50,000': 0,
        '50,001+': 0,
    };
    transactions.forEach(({ Amount }) => {
        if (Amount <= 5000) buckets['0-5,000']++;
        else if (Amount <= 10000) buckets['5,001-10,000']++;
        else if (Amount <= 20000) buckets['10,001-20,000']++;
        else if (Amount <= 50000) buckets['20,001-50,000']++;
        else buckets['50,001+']++;
    });
    return buckets;
}

// create & render charts visualizing transaction data 
function createCharts(transactions) {
    // prepare volume data per date
    const volumeData = {};
    transactions.forEach(({ DateTime }) => {
        const date = getDateOnly(DateTime);
        volumeData[date] = (volumeData[date] || 0) + 1;
    });
    const volumeLabels = Object.keys(volumeData).sort();
    const volumeCounts = volumeLabels.map(date => volumeData[date]);

    // prepare amount distribution buckets
    const amountBuckets = bucketAmounts(transactions);
    const amountLabels = Object.keys(amountBuckets);
    const amountCounts = amountLabels.map(label => amountBuckets[label]);

    // prepare counts for transaction types
    const typeCounts = {};
    transactions.forEach(({ TransactionType }) => {
        typeCounts[TransactionType] = (typeCounts[TransactionType] || 0) + 1;
    });
    const typeLabels = Object.keys(typeCounts);
    const totalTypes = Object.values(typeCounts).reduce((a, b) => a + b, 0);
    const typeDataPercent = typeLabels.map(t => (typeCounts[t] / totalTypes) * 100);

    // MTN brand colors
    const mtnColors = ['#ffcc00', '#6e260e', '#f47720', '#005a9c', '#009e49'];

    // create volume line chart
    new Chart(document.getElementById('volumeChart').getContext('2d'), {
        type: 'line',
        data: {
            labels: volumeLabels,
            datasets: [{
                label: 'Number of Transactions',
                data: volumeCounts,
                borderColor: '#ffcc00',
                backgroundColor: 'rgba(255,204,0,0.3)',
                fill: true,
                tension: 0.3,
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Date' } },
                y: { beginAtZero: true, title: { display: true, text: 'Count' } }
            }
        }
    });

    // create amount distribution bar chart
    new Chart(document.getElementById('amountChart').getContext('2d'), {
        type: 'bar',
        data: {
            labels: amountLabels,
            datasets: [{
                label: 'Transactions Count',
                data: amountCounts,
                backgroundColor: '#ffcc00',
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true, title: { display: true, text: 'Count' } }
            }
        }
    });

    // create transaction type pie chart
    new Chart(document.getElementById('typeChart').getContext('2d'), {
        type: 'pie',
        data: {
            labels: typeLabels,
            datasets: [{
                label: 'Transaction Types (%)',
                data: typeDataPercent,
                backgroundColor: mtnColors,
            }]
        },
        options: {
            plugins: {
                tooltip: {
                    callbacks: {
                        label: ctx => `${ctx.label}: ${ctx.parsed.toFixed(2)}%`
                    }
                }
            }
        }
    });
}

// initialize & start the dashboard:
// fetch transactions with authentication
// create charts on successful data fetch
// handle auth failures and errors
function initDashboard() {
    fetchWithStoredAuth(API_URL)
        .then(response => {
            if (response.status === 401) {
                alert("Authentication failed, please enter credentials again.");
                localStorage.removeItem('momoAuth'); // clear saved credentials
                initDashboard(); // retry fetching
                return null;
            }
            if (!response.ok) throw new Error(`API error: ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (data) createCharts(data);
        })
        .catch(err => {
            console.error(err);
            alert("Error fetching data.");
        });
}

// start dashboard on page load
initDashboard();

