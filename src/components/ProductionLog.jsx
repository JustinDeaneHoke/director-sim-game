import React from 'react';

/**
 * ProductionLog renders a list of production notes as a styled timeline.
 * @param {{notes: string[]}} props
 */
const ProductionLog = ({ notes = [] }) => {
  return (
    <ul className="ml-4 border-l-2 border-gray-300 pl-4">
      {notes.map((note, idx) => (
        <li key={idx} className="mb-2">
          <div className="relative pb-2">
            <span className="absolute -left-2.5 w-2 h-2 bg-blue-500 rounded-full top-1"></span>
            {note}
          </div>
        </li>
      ))}
    </ul>
  );
};

export default ProductionLog;
