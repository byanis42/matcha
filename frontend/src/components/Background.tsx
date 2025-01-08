import React from "react";
import "./Background.css"; // Créez un fichier CSS pour les styles

const Background = () => {
  return (
    <div className="background">
      {[...Array(20)].map((_, i) => (
        <div key={i} className="heart" />
      ))}
    </div>
  );
};

export default Background;
