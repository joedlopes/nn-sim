# nn-sim: Neural Network Simulator

Neural Network Simulator and Visualization Tool written in Python3 for Educational Purposes.

The project is currently under development.

[![nn-sim youtube](https://img.youtube.com/vi/2GsTY-X6W-Q/0.jpg)](https://www.youtube.com/watch?v=2GsTY-X6W-Q)

## Setup and Run

Tested on Python 3.10 on Windows 10, Windows 11, MacOS M2, Ubuntu 22.

Install required packages:
```bash
python3 -m pip install -r requirements.txt
```

Run:
```
python3 run.py
```

Select one dataset from datasets folder and start modelling and training your network :)


### Build to Executable and Portalble File (.exe)

First install setuptools and PyInstaller

```bash
python3 -m pip install setuptools pyinstaller
```

Then run the following command to build the executable file:
```bash
pyinstaller --name="nn-sim" --onefile --icon=icon.ico run.py
```
The output will be in the path *dist/nn-sim.exe*.


## License

This is a educational tool, but you are free to do what you want.

If it is useful for you, I will be happy to hear it from you. You can also cite the project:

```
@misc{nnsimjojo,
  author = {Joed Lopes da Silva},
  title = {nn-sim: neural network simulator - educational and visualization tool},
  year = {2024},
  howpublished = {\url{https://github.com/joedlopes/nn-sim}},
}
```

This repository, project, and code is provided as MIT License. The libraries and packages have their own License. The UI helper is part of pydarc from D'Arc Framework.

```
MIT License

Copyright (c) 2024 Joed Lopes da Silva

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Contact and suggestions

Feel free to contact me at [Twitter or X](https://x.com/_jo_ed_) :).

If you find some bug or have some suggestion, you can create an issue. I will be happy to help you.
