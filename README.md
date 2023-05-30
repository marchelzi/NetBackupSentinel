
# NetBackupSentinel [W.I.P]

This is a Django-based project that utilizes the Poetry tool for dependency management.

## Prerequisites

Before running this project, ensure that you have the following installed:

- Python 3.7 or higher
- Poetry (installation instructions: https://python-poetry.org/docs/#installation)

## Installation

1. Clone the repository:

```shell
cd <project-directory>
```

2. Install project dependencies using Poetry:

```shell
poetry install
```

3. Activate the virtual environment:

```shell
poetry shell
```

## Configuration

1. Create a `.env` file in the project root directory and set the following environment variables:

```plaintext
SECRET_KEY=your-secret-key
DEBUG=True
# Add other configuration variables as needed
```

2. Apply database migrations:

```shell
python manage.py migrate
```

## Usage

To start the development server, run the following command:

```shell
python manage.py runserver
```

Access the application by visiting `http://localhost:8000` in your web browser.

## Testing

To run the tests, use the following command:

```shell
python manage.py test
```

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit them
4. Push your changes to the branch: `git push origin feature/your-feature-name`
5. Submit a pull request

## License

This project is licensed under the [MIT License](LICENSE).

```
