// frontend/src/components/Background.tsx

import React from 'react';
import Heart from './Heart';

const Background: React.FC = () => {
  const numberOfHearts = 15; // Nombre de cœurs à générer
  const hearts = Array.from({ length: numberOfHearts }).map((_, index) => {
    const size = Math.floor(Math.random() * 40) + 20; // Taille entre 20px et 60px
    const top = `${Math.floor(Math.random() * 100)}%`;
    const left = `${Math.floor(Math.random() * 100)}%`;
    const animationDelay = `${Math.random() * 5}s`;
    const animationDuration = `${Math.random() * 10 + 10}s`; // Durée entre 10s et 20s
    const direction = Math.random() > 0.5 ? 'left' : 'right';

    return (
      <Heart
        key={index}
        size={size}
        top={top}
        left={left}
        animationDelay={animationDelay}
        animationDuration={animationDuration}
        direction={direction}
      />
    );
  });

  return <div className="fixed inset-0 overflow-hidden z-0 bg-black">{hearts}</div>;
};

export default Background;
