# storeweights
Storing PyTorch checkpoints in efficient way.

## Install
`pip install storeweights`

## Running

`from storeweights import weights`


```
##PyTorch code ....
model = TheModelClass()
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

....
```

### Saving model (local)

`weights.save('model_name',model,optimizer,extra_info={'epoch':40})`

### Loading model (local)

`weights.load('model_name',model,optimizer,return_extra_info=True)`

### Saving model (gdrive colab)

`weights.save('model_name',model,optimizer,extra_info={'epoch':40},gdrive=True)`

### Loading model (gdrive colab)

`weights.load('model_name',model,optimizer,return_extra_info=True,gdrive=True)`



