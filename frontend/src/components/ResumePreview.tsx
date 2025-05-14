import React from 'react';
import {Viewer, Worker} from '@react-pdf-viewer/core';
import {defaultLayoutPlugin} from '@react-pdf-viewer/default-layout';

import '@react-pdf-viewer/core/lib/styles/index.css';
import '@react-pdf-viewer/default-layout/lib/styles/index.css';

interface ResumePreviewProps {
    fileId: string;
    onClose: () => void;
}

const ResumePreview: React.FC<ResumePreviewProps> = ({fileId, onClose}) => {
    const defaultLayoutPluginInstance = defaultLayoutPlugin();

    const fileUrl = `${import.meta.env.VITE_API_BASE_URL}/files/resume/${fileId}`;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex justify-center items-center z-50">
            <div className="bg-white rounded shadow-lg w-11/12 h-5/6 relative overflow-hidden">
                <button
                    onClick={onClose}
                    className="absolute top-2 right-2 bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 z-10"
                >
                    Close
                </button>

                <div className="h-full overflow-hidden pt-12">
                    <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js">
                        <Viewer fileUrl={fileUrl} plugins={[defaultLayoutPluginInstance]}/>
                    </Worker>
                </div>
            </div>
        </div>
    );
};

export default ResumePreview;
