// pages/home.tsx
import React from 'react';
import './home.styles.css';

const Home: React.FC = () => {
    return (
        <div className="container">
            <div className="header">
                <h1>Welcome to the Home Panel</h1>
                <div className="buttons">
                    <span className="loginText">Login</span>
                    <button className="signupButton">Signup</button>
                </div>
            </div>
            {/* Add your user-friendly content here */}
        </div>
    );
};

export default Home;
