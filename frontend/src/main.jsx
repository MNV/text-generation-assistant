import {StrictMode} from 'react';
import {createRoot} from 'react-dom/client';
import {createBrowserRouter, RouterProvider} from 'react-router-dom';

import './index.css';

import Layout from './components/Layout.jsx';
import UploadPage from './pages/UploadPage.jsx';
import ResumesPage from './pages/ResumesPage.tsx';
import EntitySelectionPage from './pages/EntitySelectionPage.jsx';
import { entityLoader } from './pages/EntitySelectionPageLoader.js'; // new

import LetterGeneratorPage from './pages/LetterGenerationPage.jsx';
import LettersPage from './pages/LettersPage.tsx';

const router = createBrowserRouter([
    {
        path: '/',
        element: <Layout/>,
        children: [
            {path: '', element: <UploadPage/>},
            {path: 'resumes', element: <ResumesPage/>},
            {path: 'resumes/:id/entities', element: <EntitySelectionPage/>, loader: entityLoader},
            {path: 'generate', element: <LetterGeneratorPage/>},
            {path: 'letters', element: <LettersPage/>},
        ],
    },
]);

createRoot(document.getElementById('root')).render(
    <StrictMode>
        <RouterProvider router={router}/>
    </StrictMode>
);
