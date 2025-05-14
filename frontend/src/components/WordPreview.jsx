import React, {useEffect, useState} from 'react';
import mammoth from 'mammoth';
import axios from 'axios';

export default function WordPreview({fileId, onClose}) {
    const [content, setContent] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchDocx = async () => {
            try {
                const response = await axios.get(
                    `${import.meta.env.VITE_API_BASE_URL}/recommendation/letter/${fileId}`,
                    {responseType: 'arraybuffer'}
                );

                const result = await mammoth.convertToHtml({arrayBuffer: response.data});
                setContent(result.value);
            } catch (error) {
                console.error("Failed to preview DOCX", error);
                setContent('<p class="text-red-600">Failed to load document.</p>');
            } finally {
                setLoading(false);
            }
        };

        fetchDocx();
    }, [fileId]);

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4 overflow-auto">
            <div className="bg-white rounded shadow-lg max-w-4xl w-full h-[90%] relative overflow-y-auto p-6">
                <button
                    onClick={onClose}
                    className="absolute top-3 right-3 bg-red-500 text-white px-3 py-1 rounded"
                >
                    Close
                </button>
                {loading ? (
                    <p className="text-gray-700">Loading preview...</p>
                ) : (
                    <div
                        className="prose max-w-none"
                        dangerouslySetInnerHTML={{__html: content}}
                    />
                )}
            </div>
        </div>
    );
}
