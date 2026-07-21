import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ChevronRight, Home } from 'lucide-react';

export const Breadcrumb: React.FC = () => {
  const location = useLocation();
  const pathnames = location.pathname.split('/').filter((x) => x);

  return (
    <nav className="flex items-center space-x-1.5 text-[11px] font-medium text-slate-400 mb-2">
      <Link to="/dashboard" className="flex items-center space-x-1 hover:text-cyan-300 transition-colors">
        <Home className="w-3.5 h-3.5" />
        <span>KSP Central</span>
      </Link>
      {pathnames.map((name, index) => {
        const routeTo = `/${pathnames.slice(0, index + 1).join('/')}`;
        const isLast = index === pathnames.length - 1;
        const formattedName = name.replace('-', ' ').replace(/\b\w/g, (l) => l.toUpperCase());

        return (
          <React.Fragment key={name}>
            <ChevronRight className="w-3 h-3 text-slate-600" />
            {isLast ? (
              <span className="text-cyan-400 font-bold tracking-wide">{formattedName}</span>
            ) : (
              <Link to={routeTo} className="hover:text-cyan-300 transition-colors">
                {formattedName}
              </Link>
            )}
          </React.Fragment>
        );
      })}
    </nav>
  );
};
