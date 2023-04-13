import  torch

print("CUDA IS AVAILABLE???::::",torch.cuda.is_available())

if not torch.cuda.is_available():
    raise "No cuda availabe"