// Variable to store the ID so the download function knows which video we are talking about
let currentVideoId = "";

//GENERATE SUMMARY
document.getElementById('summarizeBtn').addEventListener('click', async () => {
  const summaryDiv = document.getElementById('summary');
  const downloadBtn = document.getElementById('downloadBtn');
  
  //Show loading state
  summaryDiv.innerHTML = '<p class="loading">Fetching summary...</p>';
  downloadBtn.style.display = 'none'; 

  //Get the current YouTube tab
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = new URL(tab.url);
  currentVideoId = url.searchParams.get('v');

  if (!currentVideoId) {
    summaryDiv.innerHTML = 'Please open a YouTube video page.';
    return;
  }

  //Request summary from FastAPI
  try {
    const formData = new FormData();
    formData.append('video_id', currentVideoId);

    const response = await fetch('http://127.0.0.1:8000/generate', {
      method: 'POST',
      body: formData
    });

    const html = await response.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const result = doc.querySelector('.output').innerText;
    
    //Display the result and download button
    summaryDiv.innerText = result;
    downloadBtn.style.display = 'flex';
  } catch (error) {
    summaryDiv.innerHTML = 'Error: Make sure FastAPI is running at http://127.0.0.1:8000';
  }
});

//DOWNLOAD PDF
document.getElementById('downloadBtn').addEventListener('click', async () => {
  try {
    //Calling FastAPI download endpoint
    const response = await fetch(`http://127.0.0.1:8000/download?video_id=${currentVideoId}`);
    
    if (!response.ok) throw new Error("Download failed");

    const blob = await response.blob();
    
    //virtual link to trigger the browser's download manager
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `YouTube_Summary_${currentVideoId}.pdf`;
    document.body.appendChild(a);
    a.click();
    
    // Cleanup
    window.URL.revokeObjectURL(url);
    a.remove();
  } catch (error) {
    alert("Could not download PDF. Is the server still running?");
  }
});