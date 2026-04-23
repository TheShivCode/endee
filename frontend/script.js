document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("upload-form");
    const queryForm = document.getElementById("query-form");
    const uploadStatus = document.getElementById("upload-status");
    const resultsDiv = document.getElementById("results");

    const API_BASE = "http://127.0.0.1:8000";

    // PDF UPLOAD
    uploadForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const fileInput = document.getElementById("pdf-file");

        if (!fileInput.files[0]) {
            uploadStatus.innerText = "Please select a file.";
            return;
        }

        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        uploadStatus.innerText = "Processing & Embedding...";

        try {
            const response = await fetch(`${API_BASE}/upload-pdf`, {
                method: "POST",
                body: formData
            });
            const data = await response.json();

            if (data.error) {
                uploadStatus.innerText = "Error: " + data.error;
            } else {
                uploadStatus.innerText = `Success! ${data.chunks_uploaded} chunks stored.`;
            }
        } catch (error) {
            uploadStatus.innerText = "Connection error. Ensure backend is running.";
        }
    });

    // SEARCH
    queryForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const queryText = document.getElementById("query-input").value;

        resultsDiv.innerText = "Searching vectors...";

        try {
            // Using URLSearchParams to handle the ?query= part correctly
            const response = await fetch(`${API_BASE}/search?query=${encodeURIComponent(queryText)}`, {
                method: "POST"
            });
            const data = await response.json();

            if (data.error || !data.matches) {
                resultsDiv.innerText = "No results found or error occurred.";
                return;
            }

            let html = "<h3>Top Results:</h3>";
            data.matches.forEach(match => {
                const score = match.score ? match.score.toFixed(3) : "N/A";
                html += `
                    <div style="background: white; padding: 10px; margin: 10px 0; border-left: 4px solid #2563eb;">
                        <small>Similarity Score: ${score}</small>
                        <p>${match.meta.text}</p>
                    </div>`;
            });
            resultsDiv.innerHTML = html;

        } catch (error) {
            resultsDiv.innerText = "Search failed. Check backend connection.";
        }
    });
});