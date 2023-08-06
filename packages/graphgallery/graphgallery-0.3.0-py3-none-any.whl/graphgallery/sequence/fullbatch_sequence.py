from graphgallery import transformers as T
from graphgallery.sequence.base_sequence import Sequence


class FullBatchNodeSequence(Sequence):

    def __init__(self, x, y=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.x = T.astensors(x, device=self.device)
        self.y = T.astensor(y, device=self.device)

    def __len__(self):
        return 1

    def __getitem__(self, index):
        return self.x, self.y

    def on_epoch_end(self):
        ...

    def _shuffle_batches(self):
        ...
