import formidable from 'formidable-serverless';
import fs from 'fs';
export const config = { api: { bodyParser: false } };

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ detail: 'Method not allowed' });
  const form = new formidable.IncomingForm();
  form.parse(req, async (err, fields, files) => {
    if (err) return res.status(500).json({ detail: 'Form parse error' });
    // Forward files to backend upload endpoint (local backend: http://localhost:8000/upload)
    // Save files temporarily and send via fetch to backend
    try {
      const fileList = Array.isArray(files.pdfs) ? files.pdfs : [files.pdfs];
      const boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW';
      const parts = [];
      const FormData = require('form-data');
      const formdata = new FormData();
      for (const f of fileList) {
        const buffer = fs.readFileSync(f.path);
        formdata.append('pdfs', buffer, { filename: f.name });
      }
      const fetchRes = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formdata
      });
      const j = await fetchRes.json();
      return res.status(fetchRes.status).json(j);
    } catch (e) {
      console.error(e);
      return res.status(500).json({ detail: 'Upload proxy failed' });
    }
  });
}
