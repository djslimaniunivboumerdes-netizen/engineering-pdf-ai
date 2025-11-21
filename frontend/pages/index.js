import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [files, setFiles] = useState(null);
  const [q, setQ] = useState('');
  const [results, setResults] = useState(null);

  const upload = async (e) => {
    e.preventDefault();
    if (!files) return alert('Select files first');
    const form = new FormData();
    for (const f of files) form.append('pdfs', f);
    const res = await axios.post('/api/upload', form, { headers: {'Content-Type':'multipart/form-data'}});
    alert(res.data.detail || 'Uploaded');
  };

  const search = async (e) => {
    e.preventDefault();
    if (!q) return alert('Query empty');
    const res = await axios.get('/api/search', { params: { q }});
    setResults(res.data.results);
  };

  return (
    <div style={{ padding: 20, fontFamily: 'Arial' }}>
      <h1>AI P&amp;ID PDF Search — Starter</h1>

      <section style={{ marginBottom: 20 }}>
        <h3>Upload PDFs (multiple)</h3>
        <form onSubmit={upload}>
          <input type="file" multiple accept="application/pdf" onChange={e=>setFiles(e.target.files)} />
          <button type="submit">Upload</button>
        </form>
      </section>

      <section style={{ marginBottom: 20 }}>
        <h3>Search</h3>
        <form onSubmit={search}>
          <input placeholder="Search..." value={q} onChange={e=>setQ(e.target.value)} style={{width:400}} />
          <button type="submit">Search</button>
        </form>
        <div>
          {results && results.map((r, i)=>(
            <div key={i} style={{border:'1px solid #ddd', padding:8, marginTop:8}}>
              <b>Page {r.page}</b>: {r.text}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
