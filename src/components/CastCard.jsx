import React from 'react';
import PropTypes from 'prop-types';

function CastCard({ talent, selected, onSelect }) {
  const handleClick = () => {
    onSelect(talent.id);
  };

  return (
    <div
      className={`border p-4 rounded shadow cursor-pointer mb-2 ${
        selected ? 'bg-blue-100 border-blue-500' : 'bg-white'
      }`}
      onClick={handleClick}
    >
      <h3 className="text-lg font-semibold">{talent.name}</h3>
      <p className="text-sm italic">{talent.role}</p>
      <p>Star Power: {talent.starPower}</p>
      <p>Skill: {talent.skill}</p>
      <p>Cost: ${talent.cost}</p>
      <p
        className={`text-sm ${talent.available ? 'text-green-600' : 'text-red-600'}`}
      >
        {talent.available ? 'Available' : 'Unavailable'}
      </p>
    </div>
  );
}

CastCard.propTypes = {
  talent: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    role: PropTypes.string.isRequired,
    starPower: PropTypes.number,
    skill: PropTypes.number,
    cost: PropTypes.number,
    available: PropTypes.bool,
  }).isRequired,
  selected: PropTypes.bool,
  onSelect: PropTypes.func.isRequired,
};

export default CastCard;
