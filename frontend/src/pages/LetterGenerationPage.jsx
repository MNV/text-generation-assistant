import React, {useEffect, useState} from 'react';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';
import Select from 'react-select';
import config from '../config';
import ResumePreview from '../components/ResumePreview.js';
import {Eye} from 'lucide-react';

export default function LetterGenerationPage() {
    const navigate = useNavigate();

    const [resumes, setResumes] = useState([]);
    const [principalId, setPrincipalId] = useState(null);
    const [granteeId, setGranteeId] = useState(null);
    const [circumstances, setCircumstances] = useState('');
    const [recommendationType, setRecommendationType] = useState('job');
    const [directives, setDirectives] = useState('');
    const [letterFileId, setLetterFileId] = useState('');
    const [previewFileId, setPreviewFileId] = useState(null);
    const [selectionError, setSelectionError] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        axios.get(`${config.API_BASE_URL}/files/resume`)
            .then(res => setResumes(res.data))
            .catch(err => console.error('Failed to fetch resumes', err));
    }, []);

    const resumeOptions = resumes.map(r => ({
        value: r.file_id,
        label: r.filename,
        meta: r
    }));

    const customOption = ({data, innerRef, innerProps}) => (
        <div ref={innerRef} {...innerProps} className="p-2 hover:bg-gray-100 rounded cursor-pointer">
            <div className="font-medium">{data.label}</div>
            <div className="text-sm text-gray-500">
                {data.meta.file_extension.toUpperCase()} • {new Date(data.meta.created_at).toLocaleString()}
            </div>
        </div>
    );

    const recommendationTypeOptions = [
        {value: 'job', label: 'Job'},
        {value: 'enrollment', label: 'Enrollment'},
        {value: 'visa', label: 'Visa'},
    ];

    const selectedRecommendationType = recommendationTypeOptions.find(
        (opt) => opt.value === recommendationType
    );

    const handlePrincipalChange = (selected) => {
        setPrincipalId(selected);
        if (selected?.value === granteeId?.value) {
            setSelectionError('Principal and grantee cannot be the same resume.');
        } else {
            setSelectionError('');
        }
    };

    const handleGranteeChange = (selected) => {
        setGranteeId(selected);
        if (selected?.value === principalId?.value) {
            setSelectionError('Principal and grantee cannot be the same resume.');
        } else {
            setSelectionError('');
        }
    };

    const handleGenerate = async () => {
        if (!principalId || !granteeId) return;

        setError('');
        setLoading(true);

        try {
            const payload = {
                personalities: {
                    principal: {resume: {file_id: principalId.value}},
                    grantee: {resume: {file_id: granteeId.value}},
                    circumstances
                },
                recommendation: {
                    type: recommendationType,
                    directives
                }
            };

            const response = await axios.post(`${config.API_BASE_URL}/recommendation`, payload);
            setLetterFileId(response.data.letter_id);
            navigate(`/letters?resume=${granteeId.value}`);
        } catch (err) {
            console.error(err);
            setError('Failed to generate the recommendation letter.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="px-4 sm:px-6 py-6 max-w-3xl mx-auto space-y-5">
            <h1 className="text-2xl font-bold">Generate Recommendation Letter</h1>

            <div>
                <label className="block font-medium mb-1">Select Principal Resume</label>
                <div className="flex flex-col sm:flex-row sm:items-center gap-2">
                    <div className="flex-1">
                        <Select
                            options={resumeOptions}
                            components={{Option: customOption}}
                            value={principalId}
                            onChange={handlePrincipalChange}
                            placeholder="Type to search..."
                        />
                    </div>
                    {principalId && (
                        <button
                            onClick={() => setPreviewFileId(principalId.value)}
                            className="text-gray-500 hover:text-gray-800"
                            title="Preview resume"
                        >
                            <Eye className="w-5 h-5"/>
                        </button>
                    )}
                </div>
                <p className="text-sm text-gray-500">Person who writes the letter</p>
            </div>

            <div>
                <label className="block font-medium mb-1">Select Grantee Resume</label>
                <div className="flex flex-col sm:flex-row sm:items-center gap-2">
                    <div className="flex-1">
                        <Select
                            options={resumeOptions}
                            components={{Option: customOption}}
                            value={granteeId}
                            onChange={handleGranteeChange}
                            placeholder="Type to search..."
                        />
                    </div>
                    {granteeId && (
                        <button
                            onClick={() => setPreviewFileId(granteeId.value)}
                            className="text-gray-500 hover:text-gray-800"
                            title="Preview resume"
                        >
                            <Eye className="w-5 h-5"/>
                        </button>
                    )}
                </div>
                <p className="text-sm text-gray-500">Person who is being recommended</p>
            </div>

            {selectionError && (
                <p className="text-red-500 text-sm">{selectionError}</p>
            )}

            <div>
                <label className="block font-medium mb-1">Circumstances</label>
                <textarea
                    value={circumstances}
                    onChange={(e) => setCircumstances(e.target.value)}
                    className="w-full border p-2 rounded"
                    rows={2}
                />
                <p className="text-sm text-gray-500">How you met the candidate</p>
            </div>

            <div>
                <label className="block font-medium mb-1">Recommendation Type</label>
                <Select
                    options={recommendationTypeOptions}
                    value={selectedRecommendationType}
                    onChange={(selected) => setRecommendationType(selected.value)}
                    className="w-full"
                />
                <p className="text-sm text-gray-500">Type of recommendation to generate</p>
            </div>

            <div>
                <label className="block font-medium mb-1">Optional Directives</label>
                <textarea
                    value={directives}
                    onChange={(e) => setDirectives(e.target.value)}
                    className="w-full border p-2 rounded"
                    rows={3}
                />
                <p className="text-sm text-gray-500">Special instructions, tone, etc.</p>
            </div>

            {error && <p className="text-red-600">{error}</p>}

            <button
                onClick={handleGenerate}
                disabled={loading || !principalId || !granteeId || !!selectionError}
                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
                {loading ? 'Generating...' : 'Generate Letter'}
            </button>

            {letterFileId && (
                <div className="mt-6">
                    <h2 className="text-lg font-semibold">Generated Letter</h2>
                    <a
                        href={`${config.API_BASE_URL}/recommendation/letter/${letterFileId}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 underline"
                    >
                        Download Recommendation Letter
                    </a>
                </div>
            )}

            {previewFileId && (
                <div className="mt-8">
                    <h2 className="text-xl font-semibold mb-2">Resume Preview</h2>
                    <button
                        onClick={() => setPreviewFileId(null)}
                        className="mb-2 px-3 py-1 bg-red-500 text-white rounded"
                    >
                        Close Preview
                    </button>
                    <ResumePreview fileId={previewFileId} onClose={() => setPreviewFileId(null)}/>
                </div>
            )}
        </div>
    );
}
