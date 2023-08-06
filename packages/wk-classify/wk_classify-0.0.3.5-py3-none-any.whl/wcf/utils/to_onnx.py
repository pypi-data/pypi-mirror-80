import torch
import os

def to_onnx(model, input_size, out_path, batch_size=1, num_channels=3, device='cpu', input_names=None,output_names=None,verbose=True):
    if output_names is None:
        output_names = ['output']
    if input_names is None:
        input_names = ['input']
    w, h = input_size
    dummy_input = torch.randn(batch_size, num_channels, h, w, device=device)
    model.eval()
    torch.onnx.export(model, dummy_input, out_path, verbose=verbose, input_names=input_names,
                      output_names=output_names)
