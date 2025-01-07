// frontend/src/components/Input.tsx

import React from 'react';

interface InputProps {
  label: string;
  type: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  required?: boolean;
}

const Input: React.FC<InputProps> = ({ label, type, value, onChange, required = false }) => {
  return (
    <div className="mb-4">
      <label className="block text-gray-300 text-sm font-bold mb-2">
        {label}
      </label>
      <input
        type={type}
        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-300 leading-tight focus:outline-none focus:shadow-outline bg-gray-800"
        value={value}
        onChange={onChange}
        required={required}
      />
    </div>
  );
};

export default Input;
