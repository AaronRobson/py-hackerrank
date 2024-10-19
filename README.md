# py-hackerrank
My solutions to some https://www.hackerrank.com challenges (spoilers)

## Run checks
```sh
make check
```

## Run unit tests
```sh
make unittest
```

### Run a specific unit test
```sh
make unittest testcase=test_synchronous_shopping.TestShop.test_case_6
```

### Run performance check
```sh
make run
```

### Run it

#### Output to screen

```sh
python3 synchronous_shopping.py input06.txt
```

Or pass in via stdin:
```sh
cat input06.txt | python3 synchronous_shopping.py
```

#### Output to file

```sh
python3 synchronous_shopping.py input06.txt --output output06-tmp.txt
```

Or pass in via stdin:
```sh
cat input06.txt | python3 synchronous_shopping.py
```

#### Output passthrough

```sh
python3 synchronous_shopping.py input06.txt --output input06-tmp.txt --output-type passthrough
```

#### Output graphviz

```sh
python3 synchronous_shopping.py input06.txt --output input06-tmp.gv --output-type graph
```

```sh
neato input06-tmp.gv -Tsvg -o output06.svg
```