# split-pdf

```bash

python3 -m venv .venv

. .venv/bin/activate

pip install -r requirements.txt

python3 <input> <pages> <output>
```

## Example usage
```bash
# Pages: 1,2,3,5,100
python3 init.py file.pdf "1-3,5,100" out.pdf
```
