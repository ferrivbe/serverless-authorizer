import React from "react";
import Image from 'next/image'
import "./login.styles.css";


const LoginScreen = () => {
    return (
        <div className="login-container">
            <div className="login-box">
                <Image
                    src="/logo.svg"
                    alt="logo"
                    className="logo"
                    width={100}
                    height={24}
                    priority
                />
                <h2>Welcome back!</h2>
                <form>
                    <input type="text" placeholder="email" />
                    <input type="password" placeholder="password" />
                    <a href="#" className="forgot-password">
                        Forgot password
                    </a>
                    <button className="login-button">Login</button>
                </form>
            </div>
        </div>
    );
};

export default LoginScreen;
