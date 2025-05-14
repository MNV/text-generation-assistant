import React, {DragEvent, useRef, useState} from 'react';
import axios from 'axios';
import config from '../config.ts';

interface ResumeFile {
    file_id: string;
    filename: string;
}

export default function UploadPage() {
    const [file, setFile] = useState<File | null>(null);
    const [message, setMessage] = useState('');
    const [fileId, setFileId] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [isDragging, setIsDragging] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleDrop = (e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDragging(false);
        const droppedFile = e.dataTransfer.files?.[0];
        if (droppedFile && (droppedFile.type === 'application/pdf' || droppedFile.name.endsWith('.docx'))) {
            setFile(droppedFile);
            setMessage('');
        } else {
            setMessage('Only PDF or DOCX files are allowed.');
        }
    };

    const handleUpload = async () => {
        if (!file) return;
        setLoading(true);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post(`${config.API_BASE_URL}/files/resume`, formData);
            setFileId(response.data.file_id);
            setMessage('✅ Upload successful!');
            setFile(null);
        } catch (err) {
            console.error('Upload failed', err);
            setMessage('❌ Upload failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => setIsDragging(false);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files?.[0];
        if (selectedFile) {
            setFile(selectedFile);
            setMessage('');
        }
    };

    return (
        <div className="p-6 max-w-xl mx-auto">
            <h1 className="text-3xl font-bold mb-6 text-center">Upload Resume</h1>

            <div
                className={`border-2 border-dashed p-10 rounded-lg text-center transition-all duration-300 cursor-pointer ${
                    isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-white'
                }`}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onClick={() => fileInputRef.current?.click()}
            >
                <p className="text-gray-600 mb-2">
                    Drag and drop your <strong>.pdf</strong> or <strong>.docx</strong> file here
                </p>
                <p className="text-sm text-gray-400">or click to select a file</p>
                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,.docx"
                    onChange={handleFileChange}
                    hidden
                />
            </div>

            {file && (
                <div className="mt-4 text-sm text-gray-700">
                    <p>📄 Selected: <span className="font-semibold">{file.name}</span></p>
                </div>
            )}

            <button
                onClick={handleUpload}
                className="mt-6 w-full btn-primary disabled:opacity-50"
                disabled={!file || loading}
            >
                {loading ? 'Uploading...' : 'Upload'}
            </button>

            {message && (
                <div className="mt-6 bg-green-50 border border-green-300 text-green-700 px-4 py-3 rounded space-y-2">
                    <p className="font-semibold">Upload successful!</p>
                    <p>
                        You can now continue working with this resume on the{' '}
                        <a
                            href="/resumes"
                            className="text-blue-600 underline hover:text-blue-800 transition"
                        >
                            Research
                        </a> page.
                    </p>
                </div>
            )}
        </div>
    );
}
