import tensorflow as tf
from tensorflow.keras import Model, Input
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers
from tensorflow.keras.losses import SparseCategoricalCrossentropy

from graphgallery.nn.layers import DenseConvolution, Gather
from graphgallery.nn.models import SemiSupervisedModel
from graphgallery.sequence import FullBatchNodeSequence
from graphgallery.utils.decorators import EqualVarLength
from graphgallery import transformers as T


class DenseGCN(SemiSupervisedModel):
    """
        Implementation of Dense version of Graph Convolutional Networks (GCN).
        `[`Semi-Supervised Classification with Graph Convolutional Networks <https://arxiv.org/abs/1609.02907>`
        Tensorflow 1.x `Sparse version` implementation: <https://github.com/tkipf/gcn>
        Pytorch `Sparse version` implementation: <https://github.com/tkipf/pygcn>

    """

    def __init__(self, *graph, adj_transformer="normalize_adj", attr_transformer=None,
                 device='cpu:0', seed=None, name=None, **kwargs):
        """Creat a Dense Graph Convolutional Networks (DenseGCN) model.


        This can be instantiated in several ways:

            model = DenseGCN(graph)
                with a `graphgallery.data.Graph` instance representing
                A sparse, attributed, labeled graph.

            model = DenseGCN(adj_matrix, attr_matrix, labels)
                where `adj_matrix` is a 2D Scipy sparse matrix denoting the graph,
                 `attr_matrix` is a 2D Numpy array-like matrix denoting the node 
                 attributes, `labels` is a 1D Numpy array denoting the node labels.


        Parameters:
        ----------
        graph: An instance of `graphgallery.data.Graph` or a tuple (list) of inputs.
            A sparse, attributed, labeled graph.
        adj_transformer: string, `transformer`, or None. optional
            How to transform the adjacency matrix. See `graphgallery.transformers`
            (default: :obj:`'normalize_adj'` with normalize rate `-0.5`.
            i.e., math:: \hat{A} = D^{-\frac{1}{2}} A D^{-\frac{1}{2}}) 
        attr_transformer: string, transformer, or None. optional
            How to transform the node attribute matrix. See `graphgallery.transformers`
            (default :obj: `None`)
        device: string. optional 
            The device where the model is running on. You can specified `CPU` or `GPU` 
            for the model. (default: :str: `CPU:0`, i.e., running on the 0-th `CPU`)
        seed: interger scalar. optional 
            Used in combination with `tf.random.set_seed` & `np.random.seed` 
            & `random.seed` to create a reproducible sequence of tensors across 
            multiple calls. (default :obj: `None`, i.e., using random seed)
        name: string. optional
            Specified name for the model. (default: :str: `class.__name__`)
        kwargs: other customed keyword Parameters.
        """
        super().__init__(*graph, device=device, seed=seed, name=name, **kwargs)

        self.adj_transformer = T.get(adj_transformer)
        self.attr_transformer = T.get(attr_transformer)
        self.process()

    def process_step(self):
        graph = self.graph
        adj_matrix = self.adj_transformer(graph.adj_matrix).toarray()
        attr_matrix = self.attr_transformer(graph.attr_matrix)

        with tf.device(self.device):
            self.feature_inputs, self.structure_inputs = T.astensors(
                attr_matrix, adj_matrix)

    # use decorator to make sure all list arguments have the same length
    @EqualVarLength()
    def build(self, hiddens=[16], activations=['relu'], dropouts=[0.5],
              l2_norms=[5e-4], lr=0.01, use_bias=False):

        with tf.device(self.device):

            x = Input(batch_shape=[None, self.graph.n_attrs],
                      dtype=self.floatx, name='attr_matrix')
            adj = Input(batch_shape=[None, None],
                        dtype=self.floatx, name='adj_matrix')
            index = Input(batch_shape=[None],
                          dtype=self.intx, name='node_index')

            h = x
            for hid, activation, dropout, l2_norm in zip(hiddens, activations, dropouts, l2_norms):
                h = DenseConvolution(hid, use_bias=use_bias,
                                     activation=activation,
                                     kernel_regularizer=regularizers.l2(l2_norm))([h, adj])

                h = Dropout(rate=dropout)(h)

            h = DenseConvolution(self.graph.n_classes,
                                 use_bias=use_bias)([h, adj])
            h = Gather()([h, index])

            model = Model(inputs=[x, adj, index], outputs=h)
            model.compile(loss=SparseCategoricalCrossentropy(from_logits=True),
                          optimizer=Adam(lr=lr), metrics=['accuracy'])

            self.model = model

    def train_sequence(self, index):
        index = T.asintarr(index)
        labels = self.graph.labels[index]
        with tf.device(self.device):
            sequence = FullBatchNodeSequence(
                [self.feature_inputs, self.structure_inputs, index], labels)
        return sequence
