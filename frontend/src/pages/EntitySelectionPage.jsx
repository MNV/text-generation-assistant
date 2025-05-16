import {useState} from 'react';
import {useLoaderData, useParams} from 'react-router-dom';
import axios from 'axios';
import config from '../config.js';

function deepEqual(obj1, obj2) {
    return JSON.stringify(obj1) === JSON.stringify(obj2);
}

function EntitySelectionPage() {
    const {id} = useParams();
    const {entities, selected} = useLoaderData();

    const [selectedEntities, setSelectedEntities] = useState(selected || {});
    const [initialEntities, setInitialEntities] = useState(selected || {});
    const [submitMessage, setSubmitMessage] = useState('');
    const [researchResults, setResearchResults] = useState({});
    const [researching, setResearching] = useState(false);
    const [saving, setSaving] = useState(false);

    const hasChanges = !deepEqual(selectedEntities, initialEntities);

    const handleCheckboxChange = (label, entity) => {
        setSelectedEntities((prev) => {
            const selected = prev[label] || [];
            const isSelected = selected.some((e) => e.text === entity.text);
            const updated = isSelected
                ? selected.filter((e) => e.text !== entity.text)
                : [...selected, entity];
            return {...prev, [label]: updated};
        });
    };

    const handleSubmit = async () => {
        setSaving(true);
        try {
            await axios.post(`${config.API_BASE_URL}/entities/resume/${id}/select`, selectedEntities);
            setInitialEntities(selectedEntities);
            setSubmitMessage('Entities saved successfully.');
        } catch (error) {
            console.error('Failed to submit entities', error);
            setSubmitMessage('Submission failed.');
        } finally {
            setSaving(false);
        }
    };

    const handleResearch = async () => {
        setResearching(true);
        setSubmitMessage('');
        setResearchResults({});
        try {
            const response = await axios.post(`${config.API_BASE_URL}/research/resume/${id}`);
            setResearchResults(response.data.data || {});
            setSubmitMessage('Research completed successfully.');
        } catch (error) {
            console.error('Research failed', error);
            setSubmitMessage('Research failed.');
        } finally {
            setResearching(false);
        }
    };

    return (
        <div className="p-6 max-w-4xl mx-auto">
            <h1 className="text-2xl font-bold mb-6">Select Entities for Research</h1>
            <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded-md mb-6 shadow-sm">
                <p className="text-sm text-yellow-700">
                    Select the most relevant skills, organizations, locations, and projects that you
                    believe should be emphasized in the recommendation letter.
                    These selected entities will be researched and used to enrich the generated content with
                    personalized and context-aware information.
                </p>
            </div>
            {Object.entries(entities).map(([label, items]) => (
                <div key={label} className="mb-4">
                    <h2 className="text-lg font-semibold mb-2">{label}</h2>
                    <ul className="space-y-1">
                        {items.map((entity, index) => (
                            <li key={`${entity.text}-${index}`} className="flex items-center gap-2">
                                <input
                                    type="checkbox"
                                    onChange={() => handleCheckboxChange(label, entity)}
                                    checked={selectedEntities[label]?.some((e) => e.text === entity.text)}
                                />
                                <span className="font-mono">{entity.text}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            ))}

            <div className="mt-6 flex gap-4">
                <button
                    onClick={handleSubmit}
                    className="btn-primary"
                    disabled={!hasChanges || saving}
                >
                    {saving ? 'Saving...' : 'Save Selection'}
                </button>

                <button
                    onClick={handleResearch}
                    className="btn-primary"
                    disabled={hasChanges || researching}
                >
                    {researching ? 'Researching...' : 'Start Research'}
                </button>
            </div>

            {submitMessage && <p className="mt-4 text-blue-600">{submitMessage}</p>}

            {Object.keys(researchResults).length > 0 && (
                <div className="mt-8">
                    <h2 className="text-xl font-bold mb-4">Research Results</h2>
                    <ul className="space-y-3">
                        {Object.entries(researchResults).map(([entity, summary]) => (
                            <li key={entity} className="bg-gray-100 p-3 rounded">
                                <strong className="text-gray-800">{entity}</strong>:<br/>
                                <span className="text-gray-700">{summary}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default EntitySelectionPage;
