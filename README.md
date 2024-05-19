# nn-sim
Neural Network Simulator and Visualization Tool written in Python for Educational Purposes



```bash
python -m pip install pyside6 pyqtgraph pyopengl pydyantic opencv-python matplotlib jupyterlab
```

# TODO

Functions:

- Create Train Widget
    - select learning rate
    - select optimization algorithm (SGD, stochastic SGD, mini batch)
        - select momentum parameters, delta, decay
        - batch size, full batch
    - view learning plots (train plot window)
    - run training in a new thread => at every epoch emit an update event
    - update weights colors

- train plot window
    - show the training plot (curve1=train loss (green), curve2=validation (red))

- net graph view window 
    - update activation neurons during learning (color map -1, 0, 1)
    - update weights

- neuron activation
    - show neuron activity in plot view
    - show neuron activity in table view

- test sample variations
    - set input sample for network input
