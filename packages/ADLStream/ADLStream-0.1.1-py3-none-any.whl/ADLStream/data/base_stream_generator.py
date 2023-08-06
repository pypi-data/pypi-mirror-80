"""Implements an abstract object representing a Stream Generator."""

from abc import ABC, abstractmethod


class BaseStreamGenerator(ABC):
    """Abstract Base Stream Generator

    This is the base class for implementing stream generators with custom behavior.

    Every `StreamGenerator` must have the properties below and implement `preprocess` with
    the signature `(x, y) = preprocess(message)`.

    Examples:
    ```python
        class MinimalBaseGenerator(BaseStreamGenerator):

            def __init__(self, stream, class_index=-1, **kwargs):
                self.class_index = class_index
                super().__init__(stream, **kwargs)
            
            def preprocess(message):
                x = message
                y = x.pop(self.class_index)
                return x, y
    ```

    Arguments:
        stream (inherits ADLStream.data.stream.BaseStream): 
            Stream source to be feed to the ADLStream framework.
    """

    def __init__(self, stream):
        self.stream = stream
        self.num_messages = 0

    @property
    def num_messages(self):
        return self._num_messages

    @num_messages.setter
    def num_messages(self, value):
        self._num_messages = value

    def next(self, context):
        message = None
        try:
            message = self.stream.next()
            self.num_messages += 1
        except StopIteration:
            context.log("INFO", "GENERATOR-PROCESS - Stream has finished")
            context.set_time_out()
        except Exception as e:
            context.log(
                "ERROR",
                "GENERATOR-PROCESS - Error getting messages from stream {}".format(
                    str(e)
                ),
            )
            context.set_time_out()

        return message

    @abstractmethod
    def preprocess(self, message):
        """The function that contains the logic to transform a stream message into 
        model imput and target data `(x ,y)`. 
        
        Both output, `x` or `y`, can be `None` what means it should not be added to
        the context. 
        
        The target data `y` can be delayed. Although we are sending `x` and `y` at 
        the same time, it does not mean that `y` is the corresponding target value
        of `x`. However, input data and target data should be in order: `y_i` is the
        target value of `x_i`. So the first target data sent (`y_0`) corresponds with
        the first input sent (`x_0`).

        Args:
            message (list): message received from the stream

        Raises:
            NotImplementedError: This is an abstract method which should be implemented.
        
        Returns:
            x (list): instance of model's input data.
            y (list): instance of model's target data.
        """
        raise NotImplementedError("Abstract method")

    def run(self, context):
        """The function that sends data to ADLStream framework

        It gets messages from the stream, preprocesses them and sends to the specific 
        ADLStream context.

        Args:
            context (ADLStream.ADLStreamContext): context where to send the stream data
        """
        self.stream.start()
        message = self.next(context)
        while message is not None:
            (x, y) = self.preprocess(message)
            if x is not None or y is not None:
                context.add(x, y)
            message = self.next(context)
