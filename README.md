# keras-dvc-demo
Train a keras model using DVC to define pipeline and store dataset

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
             **        **          
           **            **        
          *                **      
    +-------+                *     
    | train |*               *     
    +-------+ ****           *     
        *         ***        *     
        *            ****    *     
        *                **  *     
+---------------+        +------+  
| model-to-onnx |        | test |  
+---------------+        +------+  
```