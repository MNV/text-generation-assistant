import React from 'react';

export default function LoadingOverlay({message = "Please wait..."}: { message?: string }) {
    return (
        <div className="fixed inset-0 bg-white/60 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="text-center space-y-4">
                <div
                    className="loader ease-linear rounded-full border-4 border-t-blue-600 border-gray-200 h-12 w-12 mx-auto animate-spin"></div>
                <p className="text-lg text-gray-700 font-medium">{message}</p>
            </div>
        </div>
    );
}
