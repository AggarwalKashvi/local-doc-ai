document.body.innerHTML = `
  <div style="font-family: sans-serif; padding: 20px; max-width: 900px; margin: auto;">
    <h2>Offline PDF Chat</h2>

    <input type="file" id="fileInput" />
    <button id="uploadBtn">Upload PDF</button>
    <p id="uploadStatus"></p>

    <hr/>

    <textarea id="question" rows="4" style="width:100%" placeholder="Ask a question about your PDFs..."></textarea>
    <button id="askBtn">Ask</button>

    <h3>Answer:</h3>
    <pre id="answer" style="
      background:#1e1e1e;
      color:#ffffff;
      padding:15px;
      border-radius:8px;
      white-space: pre-wrap;
      font-size:14px;
    "></pre>
  </div>
`

const uploadBtn = document.getElementById("uploadBtn")!
const fileInput = document.getElementById("fileInput") as HTMLInputElement
const uploadStatus = document.getElementById("uploadStatus")!
const askBtn = document.getElementById("askBtn")!
const questionInput = document.getElementById("question") as HTMLTextAreaElement
const answerBox = document.getElementById("answer")!

uploadBtn.onclick = async () => {
  if (!fileInput.files || fileInput.files.length === 0) return

  const formData = new FormData()
  formData.append("file", fileInput.files[0])

  uploadStatus.textContent = "Uploading..."

  const res = await fetch("http://127.0.0.1:9000/upload", {
    method: "POST",
    body: formData
  })

  const data = await res.json()
  uploadStatus.textContent = data.status
}

askBtn.onclick = async () => {
  const question = questionInput.value

  answerBox.textContent = "Thinking..."
  await new Promise(r => setTimeout(r, 50))

  const res = await fetch("http://127.0.0.1:9000/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  })

  const data = await res.json()
  answerBox.textContent = data.answer
}
