# keras-dvc-demo
Train an image classification keras model using DVC to define pipeline and store dataset

## Details

Create a example repository to train a keras model using DVC to define pipeline and store dataset. 

The dataset should be stored at the data folder in different subfolders for each class and the split between train, validation and test will be done as the first step of the pipeline.

The image classification model will be a efficientnetb0.


## DVC Pipeline

```
$ dvc dag

        +-------------------+           
        | data/raw_data.dvc |           
        +-------------------+           
                   *                    
                   *                    
                   *                    
           +--------------+             
           | make_dataset |             
           +--------------+             
             **         **              
           **             **            
          *                 **          
    +-------+                 *         
    | train |*                *         
    +-------+ ****            *         
        *         ***         *         
        *            ****     *         
        *                **   *         
+---------------+         +------+      
| model-to-onnx |         | test |      
+---------------+         +------+      
                              *         
                              *         
                              *         
                    +-----------------+ 
                    | generate_report | 
                    +-----------------+ 
```

