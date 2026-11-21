# A deliberately small testable tutorial

This is an invented sample, **not** a user-authored script or a claim about any third-party product. Run `python3 examples/python-hello/demo.py` to verify the output.

**Hook:** "Here's a one-file Python program that prints a greeting. I'll show you the whole thing, then change one line to prove what it does."

**Narration:** "Open `demo.py`. This function returns a greeting. And the last two lines only run when we execute the file directly. Let's run it. We get `Hello, tutorial!`. Now change the greeting and run it again. That's the whole pattern: define a result, call it, verify the output."

**Shots:** 1. Open actual `demo.py` code. 2. Highlight `greet()`. 3. Show terminal `python3 examples/python-hello/demo.py`; display actual stdout. 4. Modify greeting, rerun, show changed result (record after testing).

**Claim ledger:** C001 observed output from test, as recorded only after running in environment.
