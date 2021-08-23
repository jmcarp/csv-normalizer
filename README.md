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

## Notes

- I didn't try to write especially DRY or abstracted code. If
    requirements change such that we have to normalize many different
    formats, we'd likely need to refactor.
- I decided to print a message to stderr and skip the current row on
    validation errors. It's possible that some errors should cause the
    normalizer to crash.
- I tried to rely on the python stdlib or widely-used third-party
    libraries where possible. I used the `codecs` package to handle
    UTF-8 complications and `pendulum` for datetimes.
- The normalize script only reads one line into memory at a time, so it
    should be able to run over a large input, although it might take a
    while.

## Next steps

- Dockerize
- Better test coverage
- Add integration tests
- Add property-based tests with hypothesis or similar
- Enforce type correctness with mypy or similar
- Generate lockfiles with pip-tools or similar
- Consider using serialization or validation helpers like marshmallow or
    pydantic
- Collect all validation errors for each row rather than bailing after
    the first error
