// Attach your referral URL with UTM tags everywhere
const BASE_REF = "https://record.coinpokeraffiliates.com/_W8N9Np6OF21fWQTENI37dGNd7ZgqdRLk/1/";
function withUTM(source, medium) {
const url = new URL(BASE_REF);
url.searchParams.set('utm_source', source);
url.searchParams.set('utm_medium', medium);
url.searchParams.set('utm_campaign', 'coinpoker');
return url.toString();
}


const cta = document.getElementById('cta');
if (cta) cta.href = withUTM('seo', 'landing');


// If you add more buttons/links, call withUTM('seo','landing') or appropriate channel.