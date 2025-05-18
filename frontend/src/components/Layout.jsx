import React, {useState} from 'react';
import {NavLink, Outlet} from 'react-router-dom';
import {Menu} from 'lucide-react';

export default function Layout() {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    const baseClass =
        'block px-3 py-1.5 rounded-full transition text-gray-700 hover:bg-gray-100 text-sm font-medium';
    const activeClass =
        'bg-blue-100 text-blue-700 font-semibold shadow-inner';

    return (
        <div>
            <nav className="sticky top-0 z-50 bg-white border-b shadow-sm">
                <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
                    <NavLink
                        to="/"
                        className="text-lg font-bold text-gray-800 tracking-wide cursor-pointer"
                        title="Go to Upload page"
                    >
                        Recommendation Letter Assistant
                    </NavLink>
                    <div className="hidden md:flex space-x-2">
                        <NavLink
                            to="/"
                            className={({isActive}) =>
                                isActive ? `${baseClass} ${activeClass}` : baseClass
                            }
                        >
                            Upload
                        </NavLink>
                        <NavLink
                            to="/resumes"
                            className={({isActive}) =>
                                isActive ? `${baseClass} ${activeClass}` : baseClass
                            }
                        >
                            Research
                        </NavLink>
                        <NavLink
                            to="/generate"
                            className={({isActive}) =>
                                isActive ? `${baseClass} ${activeClass}` : baseClass
                            }
                        >
                            Generate
                        </NavLink>
                        <NavLink
                            to="/letters"
                            className={({isActive}) =>
                                isActive ? `${baseClass} ${activeClass}` : baseClass
                            }
                        >
                            Letters
                        </NavLink>
                    </div>
                    <button
                        className="md:hidden text-gray-700 focus:outline-none"
                        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                    >
                        <Menu className="w-6 h-6"/>
                    </button>
                </div>
                {isMobileMenuOpen && (
                    <div className="md:hidden px-4 pb-4 space-y-2">
                        <NavLink
                            to="/"
                            onClick={() => setIsMobileMenuOpen(false)}
                            className={({isActive}) =>
                                isActive ? `${baseClass} ${activeClass}` : baseClass
                            }
                        >
                            Upload
                        </NavLink>
                        <NavLink
                            to="/resumes"
                            onClick={() => setIsMobileMenuOpen(false)}
                            className={({isActive}) =>
                                isActive ? `${baseClass} ${activeClass}` : baseClass
                            }
                        >
                            Research
                        </NavLink>
                        <NavLink
                            to="/generate"
                            onClick={() => setIsMobileMenuOpen(false)}
                            className={({isActive}) =>
                                isActive ? `${baseClass} ${activeClass}` : baseClass
                            }
                        >
                            Generate
                        </NavLink>
                        <NavLink
                            to="/letters"
                            onClick={() => setIsMobileMenuOpen(false)}
                            className={({isActive}) =>
                                isActive ? `${baseClass} ${activeClass}` : baseClass
                            }
                        >
                            Letters
                        </NavLink>
                    </div>
                )}
            </nav>
            <main className="p-6 max-w-6xl mx-auto">
                <Outlet/>
            </main>
        </div>
    );
}
