import * as React from 'react';
import {useEffect, useRef, useState} from 'react';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';
import {Eye, FileText, Trash2} from 'lucide-react';
import DeleteConfirmationModal from '../components/DeleteConfirmationModal.js';
import LoadingOverlay from "../components/LoadingOverlay.js";

import config from "../config.ts";
import ResumePreview from "../components/ResumePreview.js";

interface ResumeFile {
    file_id: string;
    filename: string;
    file_extension: string;
    created_at: string;
}

export default function ResumesPage() {
    const [resumes, setResumes] = useState<ResumeFile[]>([]);
    const [loading, setLoading] = useState(true);
    const [parsingId, setParsingId] = useState<string | null>(null);
    const [error, setError] = useState('');
    const [showModal, setShowModal] = useState(false);
    const [targetResume, setTargetResume] = useState<ResumeFile | null>(null);
    const [previewFileId, setPreviewFileId] = useState<string | null>(null);
    const [deletingId, setDeletingId] = useState<string | null>(null);
    const hasFetched = useRef(false);
    const navigate = useNavigate();

    useEffect(() => {
        if (hasFetched.current) return;
        hasFetched.current = true;

        const fetchResumes = async () => {
            try {
                const response = await axios.get(`${config.API_BASE_URL}/files/resume`);
                setResumes(response.data);
            } catch (err) {
                setError('Failed to load resumes');
            } finally {
                setLoading(false);
            }
        };

        fetchResumes();
    }, []);

    const handleParse = (fileId: string) => {
        setParsingId(fileId);
        navigate(`/resumes/${fileId}/entities`);
    };

    const formatDate = (dateStr: string): string => {
        const date = new Date(dateStr);

        const year = date.getFullYear();
        const month = date.toLocaleString('en-US', {month: 'short'});
        const day = date.getDate();
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');

        return `Uploaded on ${month} ${day}, ${year}, at ${hours}:${minutes}:${seconds}`;
    };

    const handleDeleteClick = (resume: ResumeFile) => {
        setTargetResume(resume);
        setShowModal(true);
    };

    const handleConfirmDelete = async () => {
        if (!targetResume) return;

        try {
            await axios.delete(`${config.API_BASE_URL}/files/resume/${targetResume.file_id}`);
            setResumes((prev) => prev.filter((r) => r.file_id !== targetResume.file_id));
        } catch (error) {
            console.error("Failed to delete resume", error);
            alert("An error occurred while deleting the resume.");
        } finally {
            setShowModal(false);
            setTargetResume(null);
        }
    };

    return (
        <div className="p-6 max-w-3xl mx-auto">
            <h1 className="text-2xl font-bold mb-4">Research Resume</h1>
            {loading ? (
                <p>Loading...</p>
            ) : error ? (
                <p className="text-red-500">{error}</p>
            ) : (
                <ul className="space-y-4">
                    {resumes.map((resume) => (
                        <li key={resume.file_id} className="border p-4 rounded-lg shadow-sm hover:shadow-md transition">
                            <div className="flex justify-between items-center">
                                <div>
                                    <p className="font-medium">{resume.filename}</p>
                                    <p className="text-sm text-gray-500">
                                        {resume.file_extension.toUpperCase()} • {formatDate(resume.created_at)}
                                    </p>
                                </div>
                                <div className="flex space-x-3">
                                    <button
                                        onClick={() => handleParse(resume.file_id)}
                                        title="Parse & Research"
                                        className="text-gray-600 hover:text-blue-600 transition"
                                    >
                                        <FileText className="w-5 h-5"/>
                                    </button>

                                    <button
                                        onClick={() => setPreviewFileId(resume.file_id)}
                                        title="Preview Resume"
                                        className="text-gray-600 hover:text-blue-600 transition"
                                    >
                                        <Eye className="w-5 h-5"/>
                                    </button>

                                    <button
                                        onClick={() => handleDeleteClick(resume)}
                                        title="Delete"
                                        className="text-gray-600 hover:text-red-600 transition"
                                    >
                                        <Trash2 className="w-5 h-5"/>
                                    </button>
                                </div>
                            </div>
                        </li>
                    ))}
                </ul>
            )}

            {previewFileId && (
                <div className="mt-8">
                    <h2 className="text-xl font-bold mb-4">Resume Preview</h2>
                    <ResumePreview
                        fileId={previewFileId!}
                        onClose={() => setPreviewFileId(null)}
                    />
                </div>
            )}

            <DeleteConfirmationModal
                isOpen={showModal}
                onClose={() => setShowModal(false)}
                onConfirm={handleConfirmDelete}
                filename={targetResume?.filename || ''}
            />

            {parsingId && <LoadingOverlay message="Parsing resume and extracting entities..."/>}
        </div>
    );
}
