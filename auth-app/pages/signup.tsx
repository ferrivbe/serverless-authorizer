"use-client"

import React, { useState, ChangeEvent, FormEvent } from "react";
import Image from "next/image";
import "./signup.styles.css";

interface ApiResponse {
    error_code: string;
    message: string;
    target: string;
    detail: {
        [key: string]: string;
    };
}

const SignUpScreen: React.FC = () => {
    const [email, setEmail] = useState<string>("");
    const [username, setUsername] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [errorMessage, setErrorMessage] = useState<string>("");

    const handleSignUp = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        const requestBody = {
            email,
            username,
            password,
        };

        try {
            const response = await fetch(
                "https://z8g9btn11c.execute-api.us-east-1.amazonaws.com/v1/users",
                {
                    method: "POST",
                    headers: {
                        accept: "application/json",
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(requestBody),
                }
            );

            const data: ApiResponse = await response.json();

            if (!response.ok) {
                // If there's an error response, set the error message
                setErrorMessage(data.message);
            } else {
                // Handle successful signup here (e.g., redirect, show success message)
                console.log("Signup successful!");
            }
        } catch (error) {
            console.error("Error occurred:", error);
            // Handle any other errors as needed
        }
    };

    return (
        <div className="signup-container">
            <div className="signup-box">
                <div className="logo-container">
                    <Image
                        src="/logo.svg"
                        alt="logo"
                        className="logo"
                        width={100}
                        height={24}
                        priority
                    />
                </div>
                <h2 className="signup-heading">Welcome!</h2>
                <form className="signup-form" onSubmit={handleSignUp}>
                    <input
                        type="text"
                        placeholder="Email"
                        required
                        value={email}
                        onChange={(e: ChangeEvent<HTMLInputElement>) =>
                            setEmail(e.target.value)
                        }
                    />
                    <input
                        type="text"
                        placeholder="Username"
                        required
                        value={username}
                        onChange={(e: ChangeEvent<HTMLInputElement>) =>
                            setUsername(e.target.value)
                        }
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        required
                        value={password}
                        onChange={(e: ChangeEvent<HTMLInputElement>) =>
                            setPassword(e.target.value)
                        }
                    />
                    <button type="submit" className="signup-button">
                        Sign Up
                    </button>
                </form>
                {errorMessage && (
                    <div className="error-box" style={{ color: "red" }}>
                        {errorMessage}
                    </div>
                )}
            </div>
        </div>
    );
};

export default SignUpScreen;
