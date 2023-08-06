import matplotlib.pyplot as plt # plotting
import os # for file/folder creations
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, BatchNormalization, Input, Dense
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Model

# =======================================================================================
# BEG: build custom model based on args
# =======================================================================================
class TestModel:
    def __init__(self, args):
        # build model
        self.args = args
        self.model = self.build_model(args)    
    
    def build_model(self, args):
        # define input dims
        input_dims = Input(shape=args.input_shape)#(32,32,3)) # flexible batch size
        
        x = self.convs_from_seq(args.conv_seq, input_dims)
        x = Flatten()(x)
        x = self.fcs_from_seq(args.fcs_seq, x)
        
        return Model(inputs=input_dims, outputs=x)
    
    def compile(self, args):
        # configure optimizer
        # rmsprop
        if args.optimizer == 'RMSprop':
            opt = keras.optimizers.RMSprop(
                lr     = args.lr, 
                decay  = args.rms_decay
            )
        elif args.optimizer == 'SGD':
            opt = keras.optimizers.SGD(
                learning_rate  = args.lr, 
                momentum       = args.sgd_momentum, 
                nesterov       = args.sgd_nesterov, 
            )

        # Create our model by compiling
        self.model.compile(
            loss       = args.loss,
            optimizer  = opt,
            metrics    = args.metrics,
        )
    
    # ----------------------------------------------------------
    # Training and evaluation
    # ----------------------------------------------------------
    def fit(self, train_data, val_data, v, args):
        """train_data, val_data are tuples of X and y"""
        if v==0:
            print("Wait for the big picture ☕️\n\nTrainng started ...")
        num_samples = train_data[0].shape[0] #X
        num_batches = num_samples / args.batch_size
        
        callbacks_list = []
        if 'CustomCallback' in args.__dict__:
            callbacks_list.append(args.CustomCallback(num_batches))
        
        self.history = self.model.fit(
            train_data[0], #X
            train_data[1], #y
            validation_data = val_data,
            batch_size      = args.batch_size,
            epochs          = args.epochs,
            shuffle         = args.shuffle,
            verbose         = v,
            callbacks       = callbacks_list
            
        )
    
    # evaluation
    def evaluate(self, x_test, y_test, v=1):
        print("Evaluating on test data...\n")
        test_loss, test_acc = \
            self.model.evaluate(x_test, y_test, verbose=v)
        print(f"+ Test Loss\t:{test_loss}\n+ Test Acc\t:{test_acc}")
    
    # save
    def save_to(self, save_dir):
        self.model.save(save_dir)
    
    # -----------------------------------------------------------
    # plot
    # -----------------------------------------------------------
    def plot(self):
        history_dict = self.history.history
        
        # Plot loss chart
        loss_values     = history_dict['loss']
        val_loss_values = history_dict['val_loss']
        epochs          = range(1, len(loss_values) + 1)
        
        line1 = plt.plot(epochs, val_loss_values, label='Validation/Test Loss')
        line2 = plt.plot(epochs, loss_values, label='Training Loss')
        
        plt.setp(line1, linewidth=2.0, marker = '+', markersize=10.0)
        plt.setp(line2, linewidth=2.0, marker = '4', markersize=10.0)
        plt.xlabel('Epochs') 
        plt.ylabel('Loss')
        plt.grid(True)
        plt.legend()
        
        # Plot acc chart
        acc_values      = history_dict['accuracy']
        val_acc_values  = history_dict['val_accuracy']
        epochs          = range(1, len(loss_values) + 1)

        line1 = plt.plot(epochs, val_acc_values, label='Validation/Test Accuracy')
        line2 = plt.plot(epochs, acc_values, label='Training Accuracy')
        
        plt.setp(line1, linewidth=2.0, marker = '+', markersize=10.0)
        plt.setp(line2, linewidth=2.0, marker = '4', markersize=10.0)
        plt.xlabel('Epochs') 
        plt.ylabel('Accuracy')
        plt.grid(True)
        plt.legend()        
        
        # display
        plt.show()
    
    def summary(self):
        keras.utils.plot_model(
            self.model,
            to_file="model.png",
            show_shapes=False,
            #show_dtype=False,
            show_layer_names=True,
            rankdir="TB",
            expand_nested=False,
            dpi=96,
        )
        return self.model.summary()    
    # ===========================================================
    # BEG: build_model helpers
    # ===========================================================
    def convs_from_seq(self, seq, x):
        """
        + x is input which will be forwarded in series 
        + seq is of format
            [
                {"out_ch": int, "z": int, 'act': 'relu', 'bn': True, 'p': 0.5, 'L1': 1e-4},
                {"out_ch": int, "z": int, 'act': 'relu', "maxpool_z": 2},
                # -------------------------------------------------------
                {"out_ch": int, "z": int, 'act': 'relu'},
                ....
            ]
        + regularize all if `args.regularize_all = L1 / L2 / L1L2` 
        """
        # bulid series
        series = []
        for config in seq:
            
            # append convs and nonlin one-by-one                
            # regularize all
            kernel_regularizer = None
            if ('L1' in self.args.__dict__):
                kernel_regularizer =  keras.regularizers.l1(l1=self.args.__dict__['L1'])
            elif ('L2' in self.args.__dict__):
                kernel_regularizer =  keras.regularizers.l2(l2=self.args.__dict__['L2'])
            elif ('L1L2' in self.args.__dict__):
                kernel_regularizer =  keras.regularizers.l1_l2(
                    l1=self.args.__dict__['L1L2'][0], 
                    l2=self.args.__dict__['L1L2'][1]
                )
            # regularize >>>individually<<<
            # (OVERWRITE `kernel_regularizer` created by regularize all)
            if 'L1' in config:
                kernel_regularizer =  keras.regularizers.l1(l1=config['L1'])
            elif 'L2' in config:
                kernel_regularizer =  keras.regularizers.l2(l2=config['L2'])
            elif 'L1L2' in config:
                kernel_regularizer =  keras.regularizers.l1_l2(
                    l1=config['L1L2'][0],
                    l2=config['L1L2'][1],
                )
            
            series.append(
                self.__get_conv(
                    out_ch              = config['out_ch'],
                    z                   = config['z'],
                    padding             = 'same',
                    kernel_regularizer  = kernel_regularizer
                )
            )
            
            # activation function
            series.append(self.__get_act(config['act']))
            
            # pool if specified
            if 'maxpool_z' in config.keys():
                # append pool one-by-one
                series.append(self.__get_pool(config['maxpool_z']))
            
            # (before bn)
            if 'p' in config.keys():
                series.append(self.__get_dropout(config["p"]))
                
            # batchnorm (after dropout)
            if 'bn' in config.keys():
                if config['bn'] is True:
                    # append bn one-by-one
                    series.append(self.__get_bn())

        # forward through series
        """ #OVERKILL
        return Sequential(series)
        """
        for layer in series:
            x = layer(x)
        return x

    def fcs_from_seq(self, seq, x):
        """
        + x is input
        + seq is of format
            [
                {"out_nodes": int, "act": 'relu', 'bn': True},
                {"out_nodes": int, "act": 'relu', 'bn': Fale, 'p': 0.5 },
                ....
            ]
        """
        # build series
        series = []
        for config in seq:
            
            # regularize all
            kernel_regularizer = None
            if ('L1' in self.args.__dict__):
                kernel_regularizer =  keras.regularizers.l1(l1=self.args.__dict__['L1'])
            elif ('L2' in self.args.__dict__):
                kernel_regularizer =  keras.regularizers.l2(l2=self.args.__dict__['L2'])
            elif ('L1L2' in self.args.__dict__):
                kernel_regularizer =  keras.regularizers.l1_l2(
                    l1=self.args.__dict__['L1L2'][0], 
                    l2=self.args.__dict__['L1L2'][1]
                )
            # regularize >>>individually<<<
            # (OVERWRITE `kernel_regularizer` created by regularize all)
            if 'L1' in config:
                kernel_regularizer =  keras.regularizers.l1(l1=config['L1'])
            elif 'L2' in config:
                kernel_regularizer =  keras.regularizers.l2(l2=config['L2'])
            elif 'L1L2' in config:
                kernel_regularizer =  keras.regularizers.l1_l2(
                    l1=config['L1L2'][0],
                    l2=config['L1L2'][1],
                )
                
            series.append(
                self.__get_dense(
                    out_nodes           = config["out_nodes"], 
                    act                 = config["act"],
                    kernel_regularizer  = kernel_regularizer
                )
            )
            
            # batchnorm (before dropout)
            if 'bn' in config:
                if config['bn'] is True:
                    # append bn one-by-one
                    series.append(self.__get_bn())
                    
            # dropout (after batchnorm)
            if 'p' in config:
                series.append(self.__get_dropout(config["p"]))
        
        # forward through series
        """ # OVERKILL
        return Sequential(series)
        """
        for layer in series:
            x = layer(x)
        return x

        
    # helpers start ---------------------------------
    # general
    def __get_bn(self):
        return BatchNormalization()
        
    def __get_act(self, name):
        """`name` is a string. eg. 'relu'"""
        return Activation(name)
    
    # for convs_seq
    def __get_conv(self, out_ch, z, padding, kernel_regularizer):
        """
        For "SAME" padding, if you use a stride of 1, 
        the layer's outputs will have the same spatial 
        dimensions as its inputs.
        """
        return Conv2D(out_ch, (z, z), padding=padding, 
                      strides=(1, 1), kernel_regularizer=kernel_regularizer)
    
    def __get_pool(self, z):
        return MaxPooling2D(pool_size=(z, z))
    
    # for fcs_Seq
    def __get_dense(self, out_nodes, act, kernel_regularizer):
        """out_nodes is int and act is string """
        print(kernel_regularizer)
        return Dense(out_nodes, activation=act, kernel_regularizer=kernel_regularizer)
    
    def __get_dropout(self, p):
        """ p if float [0, 1]"""
        return Dropout(p)
    # helpers end ------------------------------------
    # ===========================================================
    # END: build_model helpers 
    # ===========================================================
# =======================================================================================
# END: build custom model based on args
# =======================================================================================
