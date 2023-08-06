import keras #for one-hot-encoding
import math 

class InMemoryImgHandler:
    """
    Handles image data available in RAM
    """
    def __init__(self, X, y, y_info, ratio=(60,20,20)):
        """
        + `X` is 4-D ndarray of (n_samples, w, h, c)
        + `y` is  either one-hot-encoded (n_smaple, n_classes) bin 
           numeric (n_smaple, 1) ndarray
        + y_info is tuple
            - idx 2{INT}  : num_classes
            - idx 1{BOOL} : True if one-hot-encoded already
        + `ratio` is tuple (train_ratio, val_ratio, test_ratio)
        """
        # 1. one hot encode targets if not already
        if y_info[1] is False:
            y = self.one_hot_encode(y, y_info[0])
        # 2. Normalize X
        X = InMemoryImgHandler.normalize_img_data(X)
        # 3. gen train, val and test dataset and store
        (self.x_train, self.y_train), (self.x_val, self.y_val), (self.x_test, self.y_test) = \
            InMemoryImgHandler.train_val_test_split(X, y, ratio)

    # ============================================================================================
    # BEG: static methods 
    # ============================================================================================
    @staticmethod
    def train_val_test_split(X, y, ratio):
        """ 
        + `X` is 4-D array of (n_samples, w, h, c) 
        + `y` is one-hot-ecoded
        + `ratio` is tuple (train_ratio, val_ratio, test_ratio)
        + returns tuple (X_tr, y_tr), (X_val, y_val), (X_te, y_te)

        Note: not shufflind cz, it will be taken care by fit function
        """
        if (ratio[0] + ratio[1] + ratio[2]) != 100:
            raise Exception('Split percents\' sum must be 100!')

        n_samples = X.shape[0]
        n_train   =  math.floor( (ratio[0]/100) * n_samples )
        n_val     =  math.floor( (ratio[1]/100) * n_samples )
        n_test    =  math.floor( (ratio[2]/100) * n_samples )
        
        train_l, train_r   =             0, n_train
        val_l, val_r       =       n_train, n_train+n_val
        test_l, test_r     = n_train+n_val, n_train+n_val+n_test
        
        return (
            ( X[train_l:train_r], y[train_l:train_r] ), 
            ( X[val_l:val_r]    , y[val_l:val_r] ), 
            ( X[test_l:test_r]  , y[test_l:test_r] ), 
        )
    
    @staticmethod
    def normalize_img_data(ndarray, div_val=255):
        """ ndarray is 4-D (n_samples, w, h, c) x_train """
        ndarray = ndarray.astype('float32')
        ndarray /= div_val
        return ndarray
    
    @staticmethod
    def one_hot_encode(y, num_classes):
        """ y (is n_samples, 1) 2-D vector. Not a flat array"""
        return keras.utils.to_categorical(y, num_classes)
    # ============================================================================================
    # END: static methods 
    # ============================================================================================