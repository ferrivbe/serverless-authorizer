![workflow](https://github.com/ferrivbe/serverless-authorizer/actions/workflows/main.yml/badge.svg)

# Serverless Authorizer

This repository contains a serverless authorizer built using FastAPI as the REST API core, AWS Lambda for deployment, and Cognito for user pool management. The authorizer provides methods for creating users, verifying users, creating session tokens, and verifying tokens.

## Features

- User creation: Allows the creation of new users with specified credentials.
- User verification: Verifies the existence and validity of a user in the user pool.
- Session token creation: Generates a session token for authenticated users.
- Token verification: Validates the authenticity and integrity of a session token.

## Technologies Used

- FastAPI: A modern, fast (high-performance) web framework for building APIs with Python.
- AWS Lambda: A serverless compute service that lets you run your code without provisioning or managing servers.
- AWS Cognito: A fully managed user identity and authentication service provided by AWS.

## Prerequisites

To run the serverless authorizer locally or deploy it using the Serverless Framework, you need the following prerequisites:

- Node.js and npm
- Serverless Framework (installed globally)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/serverless-authorizer.git
   ```

2. Change to the project's directory:

   ```bash
   cd serverless-authorizer
   ```

## Configuration

Before deploying the serverless authorizer, you may need to configure certain settings depending on your requirements. Update the `config.py` file with your desired configurations:

```python
# config.py

COGNITO_REGION = "your-cognito-region"
COGNITO_USER_POOL_ID = "your-cognito-user-pool-id"
```

## Deployment

To deploy the serverless authorizer using the Serverless Framework, follow these steps:

1. Install the necessary Serverless Framework plugins (if not already installed):

   ```bash
   npm install
   ```

2. Deploy the application:

   ```bash
   sls deploy
   ```

   The Serverless Framework will package and deploy the application to AWS Lambda. After deployment, you will receive the API endpoint URL to use for making requests.

## Local Development

To run the serverless authorizer locally for development purposes, use the following command:

```bash
sls offline
```

The authorizer API will be available at `http://localhost:3000`.

## API Documentation

The API documentation for the serverless authorizer is available at `http://localhost:3000/docs` when running locally or at the deployed API endpoint URL.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to modify and distribute it as per the terms of the license.

## Contributions

Contributions to this project are welcome. Feel free to open issues and submit pull requests to enhance the functionality or fix any existing issues.

## Contact

For any questions or inquiries, please contact the project maintainer:

- Name: John Doe
- Email: johndoe@example.com

Feel free to reach out with any questions or suggestions!

Enjoy using the serverless authorizer!
