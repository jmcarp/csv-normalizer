# CSV Normalizer

## Usage

Note: tested on macos 11.5 with python 3.9.

- Installation:

    ```bash
    pip install -r requirements.txt
    ```

- Normalize a csv:

    ```bash
    ./normalize.py < $INPUT_PATH > $OUTPUT_PATH
    ```

- Run tests:
 
    ```bash
    pip install -r dev-requirements.txt
    pytest tests.py
    ```

## Next steps

- Dockerize
- Better test coverage
- Add integration tests
- Enforce type correctness with mypy or similar
- Generate lockfiles with pip-tools or similar
- Consider using serialization or validation helpers like marshmallow or
    pydantic
- Collect all validation errors for each row rather than bailing after
    the first error
