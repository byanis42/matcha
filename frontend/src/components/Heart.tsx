// frontend/src/components/Heart.tsx

import React from 'react';

interface HeartProps {
  size: number; // Taille du cœur en pixels
  top: string; // Position verticale
  left: string; // Position horizontale
  animationDelay: string; // Délai de démarrage de l'animation
  animationDuration: string; // Durée de l'animation
  direction: 'left' | 'right'; // Direction du mouvement
}

const Heart: React.FC<HeartProps> = ({
  size,
  top,
  left,
  animationDelay,
  animationDuration,
  direction,
}) => {
  return (
    <div
      className="absolute"
      style={{
        width: size,
        height: size,
        top: top,
        left: left,
        animationDelay: animationDelay,
        animationDuration: animationDuration,
      }}
    >
      <svg
        viewBox="0 0 32 29.6"
        className="w-full h-full text-neon-red stroke-neon-red"
      >
        <path
          fill="none"
          strokeWidth="2"
          d="M23.6,0c-3.4,0-6.3,2.6-7.6,6.1C14.7,2.6,11.8,0,8.4,0C3.8,0,0,3.8,0,8.4c0,7.5,8,14.5,16,21.2c8-6.7,16-13.7,16-21.2C32,3.8,28.2,0,23.6,0z"
        />
      </svg>
      <style jsx>{`
        svg {
          filter: drop-shadow(0 0 10px rgba(255, 7, 58, 0.7))
                  drop-shadow(0 0 20px rgba(255, 7, 58, 0.5));
          transform: rotate(0deg);
          animation: move-${direction} infinite linear;
        }

        @keyframes move-left {
          0% {
            transform: translate(0, 0) rotate(0deg);
            opacity: 1;
          }
          50% {
            transform: translate(-50px, -150px) rotate(-180deg);
            opacity: 0.7;
          }
          100% {
            transform: translate(-100px, -300px) rotate(-360deg);
            opacity: 0;
          }
        }

        @keyframes move-right {
          0% {
            transform: translate(0, 0) rotate(0deg);
            opacity: 1;
          }
          50% {
            transform: translate(50px, -150px) rotate(180deg);
            opacity: 0.7;
          }
          100% {
            transform: translate(100px, -300px) rotate(360deg);
            opacity: 0;
          }
        }
      `}</style>
    </div>
  );
};

export default Heart;
