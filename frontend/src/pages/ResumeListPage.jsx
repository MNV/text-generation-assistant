import { useEffect, useState } from 'react';
import { listResumes } from '../api/files';

export default function ResumeList() {
  const [resumes, setResumes] = useState([]);

  useEffect(() => {
    const fetchResumes = async () => {
      const data = await listResumes();
      setResumes(data);
    };

    fetchResumes();
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-2">Uploaded Resumes</h2>
      <ul className="space-y-2">
        {resumes.map((resume) => (
          <li key={resume.file_id} className="border p-2 rounded">
            <span className="font-mono text-sm">{resume.filename}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
