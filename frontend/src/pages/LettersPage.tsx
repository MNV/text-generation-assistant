import React, {useEffect, useState} from 'react';
import axios from 'axios';
import {useSearchParams} from 'react-router-dom';
import Select, {OptionProps, SingleValue} from 'react-select';
import config from '../config.js';
import {Download, Eye, Trash2} from 'lucide-react';
import ResumePreview from '../components/ResumePreview.js';
import DeleteConfirmationModal from '../components/DeleteConfirmationModal.js';

interface Resume {
    file_id: string;
    filename: string;
    file_extension: string;
    created_at: string;
}

interface Letter {
    letter_id: string;
    filename: string;
    file_extension: string;
    created_at: string;
}

interface ResumeOption {
    value: string;
    label: string;
    meta: Resume;
}

export default function LettersPage() {
    const [searchParams] = useSearchParams();
    const [resumes, setResumes] = useState<Resume[]>([]);
    const [selectedResume, setSelectedResume] = useState<ResumeOption | null>(null);
    const [letters, setLetters] = useState<Letter[]>([]);
    const [loading, setLoading] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [letterToDelete, setLetterToDelete] = useState<Letter | null>(null);
    const [previewResumeId, setPreviewResumeId] = useState<string | null>(null);

    useEffect(() => {
        axios.get(`${config.API_BASE_URL}/files/resume`)
            .then(res => {
                const resumeList = res.data;
                setResumes(resumeList);

                const resumeId = searchParams.get('resume');
                const found = resumeList.find((r: { file_id: string | null; }) => r.file_id === resumeId);
                if (found) {
                    const selected = {
                        value: found.file_id,
                        label: found.filename,
                        meta: found,
                    };
                    setSelectedResume(selected);
                    handleResumeChange(selected);
                }
            })
            .catch(err => console.error('Failed to fetch resumes', err));
    }, []);

    const handleResumeChange = async (option: SingleValue<ResumeOption>) => {
        if (!option) return;

        setSelectedResume(option);
        setLetters([]);
        setLoading(true);
        setPreviewResumeId(null);

        try {
            const res = await axios.get(`${config.API_BASE_URL}/recommendation/resume/${option.value}/letters`);
            setLetters(res.data.letters || []);
        } catch (error) {
            console.error('Failed to load letters', error);
        } finally {
            setLoading(false);
        }
    };

    const resumeOptions: ResumeOption[] = resumes.map(r => ({
        value: r.file_id,
        label: r.filename,
        meta: r,
    }));

    const customOption = (props: OptionProps<ResumeOption>) => {
        const {data, innerRef, innerProps} = props;
        return (
            <div ref={innerRef} {...innerProps} className="p-2 hover:bg-gray-100 rounded cursor-pointer">
                <div className="font-medium">{data.label}</div>
                <div className="text-sm text-gray-500">
                    {data.meta.file_extension.toUpperCase()} • {new Date(data.meta.created_at).toLocaleString()}
                </div>
            </div>
        );
    };

    const downloadLetter = async (letterId: string, filename: string, extension: string) => {
        try {
            const response = await axios.get(`${config.API_BASE_URL}/recommendation/letter/${letterId}`, {
                responseType: 'blob',
            });

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `${filename}.${extension}`);
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Failed to download letter:', error);
        }
    };

    const formatDate = (dateStr: string): string => {
        const date = new Date(dateStr);
        const year = date.getFullYear();
        const month = date.toLocaleString('en-US', {month: 'short'});
        const day = date.getDate();
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
        return `Created on ${month} ${day}, ${year}, at ${hours}:${minutes}:${seconds}`;
    };

    const handleDeleteClick = (letter: Letter) => {
        setLetterToDelete(letter);
        setShowModal(true);
    };

    const handleConfirmDelete = async () => {
        if (!letterToDelete) return;
        try {
            await axios.delete(`${config.API_BASE_URL}/recommendation/letter/${letterToDelete.letter_id}`);
            setLetters(prev => prev.filter(l => l.letter_id !== letterToDelete.letter_id));
        } catch (err) {
            console.error('Failed to delete letter:', err);
        } finally {
            setShowModal(false);
            setLetterToDelete(null);
        }
    };

    return (
        <div className="p-6 max-w-3xl mx-auto space-y-6">
            <h1 className="text-2xl font-bold">Generated Letters</h1>

            <div>
                <label className="block font-medium mb-2">Select Resume</label>
                <div className="flex items-center gap-2">
                    <div className="flex-1">
                        <Select
                            options={resumeOptions}
                            components={{Option: customOption}}
                            value={selectedResume}
                            onChange={handleResumeChange}
                            placeholder="Type to search resumes..."
                            isClearable
                        />
                    </div>
                    {selectedResume && (
                        <button
                            onClick={() => setPreviewResumeId(selectedResume.value)}
                            className="text-gray-500 hover:text-gray-800"
                            title="Preview resume"
                        >
                            <Eye className="w-5 h-5"/>
                        </button>
                    )}
                </div>
                <p className="text-sm text-gray-500 mt-1">
                    Select grantee's resume to find generated recommendation letters
                </p>
            </div>

            {loading && <p className="text-gray-600">Loading letters...</p>}

            {!loading && selectedResume && letters.length === 0 && (
                <p className="text-gray-500 italic">No letters found for this resume.</p>
            )}

            {letters.length > 0 && (
                <div className="space-y-4">
                    {letters.map(letter => (
                        <div key={letter.letter_id}
                             className="border p-4 rounded shadow flex justify-between items-center">
                            <div>
                                <p className="font-medium">{letter.filename}</p>
                                <p className="text-sm text-gray-500">
                                    {letter.file_extension.toUpperCase()} • {formatDate(letter.created_at)}
                                </p>
                            </div>
                            <div className="flex space-x-3">
                                <button
                                    onClick={() => downloadLetter(letter.letter_id, letter.filename, letter.file_extension)}
                                    className="text-gray-600 hover:text-blue-600"
                                    title="Download Letter"
                                >
                                    <Download className="w-5 h-5"/>
                                </button>
                                <button
                                    onClick={() => handleDeleteClick(letter)}
                                    className="text-gray-600 hover:text-red-600"
                                    title="Delete Letter"
                                >
                                    <Trash2 className="w-5 h-5"/>
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {previewResumeId && (
                <div className="mt-8">
                    <h2 className="text-lg font-semibold mb-2">Resume Preview</h2>
                    <ResumePreview fileId={previewResumeId} onClose={() => setPreviewResumeId(null)}/>
                </div>
            )}

            <DeleteConfirmationModal
                isOpen={showModal}
                onClose={() => setShowModal(false)}
                onConfirm={handleConfirmDelete}
                filename={letterToDelete?.filename || ''}
            />
        </div>
    );
}
