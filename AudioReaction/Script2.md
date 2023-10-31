To modify the script for multi-class classification, you should adjust the prediction function and the action that is triggered based on the prediction. This is because multi-class classification means the model will now return a class label instead of a binary output. You should also change the way you interpret the model's output. You can use the `torch.argmax` function to get the class with the highest probability from the model's output.

Here's how you could adjust your script:

```python
class WakeWordEngine:

    # ... existing code ...

    def predict(self, audio):
        with torch.no_grad():
            fname = self.save(audio)
            waveform, _ = torchaudio.load(fname)  # don't normalize on train
            mfcc = self.featurizer(waveform).transpose(1, 2).transpose(0, 1)

            out = self.model(mfcc)
            print(torch.softmax(out, dim=1))
            pred = torch.argmax(torch.softmax(out, dim=1))
            return pred.item()

class DemoAction:
    """This demo action will just randomly say Arnold Schwarzenegger quotes

        args: sensitivty. the lower the number the more sensitive the
        wakeword is to activation.
    """
    # ... existing code ...

    def __call__(self, prediction):
        if prediction == 1:  # change this to the class label you're interested in
            self.detect_in_row += 1
            if self.detect_in_row == self.sensitivity:
                self.play()
                self.detect_in_row = 0
        else:
            self.detect_in_row = 0

    # ... remaining code ...
```

Note that in the `DemoAction` class, the `__call__` method is triggered when the predicted class is 1. You should adjust this to the class label that corresponds to the action you want to trigger. Also, the `torch.softmax` function is used in the `predict` method to convert the model's output to a probability distribution over the classes [Source 2](https://pytorch.org/audio/stable/index.html), [Source 3](https://pytorch.org/tutorials/beginner/audio_preprocessing_tutorial.html).