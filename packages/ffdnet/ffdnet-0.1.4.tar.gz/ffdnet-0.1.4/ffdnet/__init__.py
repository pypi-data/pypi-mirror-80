"""
code from the IPOL publication:
    Denoise an image with the FFDNet denoising method
    Copyright (C) 2018, Matias Tassano <matias.tassano@parisdescartes.fr>
    This program is free software: you can use, modify and/or
    redistribute it under the terms of the GNU General Public
    License as published by the Free Software Foundation, either
    version 3 of the License, or (at your option) any later
    version. You should have received a copy of this license along
    this program. If not, see <http://www.gnu.org/licenses/>.
"""

import os
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

def remove_dataparallel_wrapper(state_dict):
    """
        Converts a DataParallel model to a normal one by removing the "module."
        wrapper in the module dictionary

        args:
            state_dict: a torch.nn.DataParallel state dictionary
    """
    from collections import OrderedDict

    new_state_dict = OrderedDict()
    for k, vl in state_dict.items():
        name = k[7:]  # remove 'module.' of DataParallel
        new_state_dict[name] = vl

    return new_state_dict

def concatenate_input_noise_map(input, noise_sigma):
    """
        Implements the first layer of FFDNet. This function returns a
        torch.autograd.Variable composed of the concatenation of the downsampled
        input image and the noise map. Each image of the batch of size CxHxW gets
        converted to an array of size 4*CxH/2xW/2. Each of the pixels of the
        non-overlapped 2x2 patches of the input image are placed in the new array
        along the first dimension.

        args:
            input: batch containing CxHxW images
            noise_sigma: the value of the pixels of the CxH/2xW/2 noise map
    """
    # noise_sigma is a list of length batch_size
    N, C, H, W = input.size()
    dtype = input.type()
    sca = 2
    sca2 = sca*sca
    Cout = sca2*C
    Hout = H//sca
    Wout = W//sca
    idxL = [[0, 0], [0, 1], [1, 0], [1, 1]]

    # Fill the downsampled image with zeros
    if 'cuda' in dtype:
        downsampledfeatures = torch.cuda.FloatTensor(N, Cout, Hout, Wout).fill_(0)
    else:
        downsampledfeatures = torch.FloatTensor(N, Cout, Hout, Wout).fill_(0)

    # Build the CxH/2xW/2 noise map
    noise_map = noise_sigma.view(N, 1, 1, 1).repeat(1, C, Hout, Wout)

    # Populate output
    for idx in range(sca2):
        downsampledfeatures[:, idx:Cout:sca2, :, :] = input[:, :, idxL[idx][0]::sca, idxL[idx][1]::sca]

    # concatenate de-interleaved mosaic with noise map
    return torch.cat((noise_map, downsampledfeatures), 1)

class UpSampleFeaturesFunction(torch.autograd.Function):
    """
        Extends PyTorch's modules by implementing a torch.autograd.Function.
        This class implements the forward and backward methods of the last layer
        of FFDNet. It basically performs the inverse of
        concatenate_input_noise_map(): it converts each of the images of a
        batch of size CxH/2xW/2 to images of size C/4xHxW
    """

    @staticmethod
    def forward(ctx, input):
        N, Cin, Hin, Win = input.size()
        dtype = input.type()
        sca = 2
        sca2 = sca*sca
        Cout = Cin//sca2
        Hout = Hin*sca
        Wout = Win*sca
        idxL = [[0, 0], [0, 1], [1, 0], [1, 1]]

        assert (Cin%sca2 == 0), 'Invalid input dimensions: number of channels should be divisible by 4'

        result = torch.zeros((N, Cout, Hout, Wout)).type(dtype)
        for idx in range(sca2):
            result[:, :, idxL[idx][0]::sca, idxL[idx][1]::sca] = \
                    input[:, idx:Cin:sca2, :, :]

        return result

    @staticmethod
    def backward(ctx, grad_output):
        N, Cg_out, Hg_out, Wg_out = grad_output.size()
        dtype = grad_output.data.type()
        sca = 2
        sca2 = sca*sca
        Cg_in = sca2*Cg_out
        Hg_in = Hg_out//sca
        Wg_in = Wg_out//sca
        idxL = [[0, 0], [0, 1], [1, 0], [1, 1]]

        # Build output
        grad_input = torch.zeros((N, Cg_in, Hg_in, Wg_in)).type(dtype)
        # Populate output
        for idx in range(sca2):
            grad_input[:, idx:Cg_in:sca2, :, :] = \
                    grad_output.data[:, :, idxL[idx][0]::sca, idxL[idx][1]::sca]
        return grad_input

upsamplefeatures = UpSampleFeaturesFunction.apply


class IntermediateDnCNN(nn.Module):

    def __init__(self, input_features, middle_features, num_conv_layers):
        super(IntermediateDnCNN, self).__init__()
        self.kernel_size = 3
        self.padding = 1
        self.input_features = input_features
        self.num_conv_layers = num_conv_layers
        self.middle_features = middle_features
        if self.input_features == 5:
            self.output_features = 4 #Grayscale image
        elif self.input_features == 15:
            self.output_features = 12 #RGB image
        else:
            raise Exception('Invalid number of input features')

        layers = []
        layers.append(nn.Conv2d(in_channels=self.input_features,\
                out_channels=self.middle_features,\
                kernel_size=self.kernel_size,\
                padding=self.padding,\
                bias=False))
        layers.append(nn.ReLU(inplace=True))
        for _ in range(self.num_conv_layers-2):
            layers.append(nn.Conv2d(in_channels=self.middle_features,\
                    out_channels=self.middle_features,\
                    kernel_size=self.kernel_size,\
                    padding=self.padding,\
                    bias=False))
            layers.append(nn.BatchNorm2d(self.middle_features))
            layers.append(nn.ReLU(inplace=True))
        layers.append(nn.Conv2d(in_channels=self.middle_features,\
                out_channels=self.output_features,\
                kernel_size=self.kernel_size,\
                padding=self.padding,\
                bias=False))
        self.itermediate_dncnn = nn.Sequential(*layers)

    def forward(self, x):
        out = self.itermediate_dncnn(x)
        return out


class FFDNet(nn.Module):

    def __init__(self, num_input_channels):
        super(FFDNet, self).__init__()
        self.num_input_channels = num_input_channels
        if self.num_input_channels == 1:
            self.num_feature_maps = 64
            self.num_conv_layers = 15
            self.downsampled_channels = 5
            self.output_features = 4
        elif self.num_input_channels == 3:
            self.num_feature_maps = 96
            self.num_conv_layers = 12
            self.downsampled_channels = 15
            self.output_features = 12
        else:
            raise Exception('Invalid number of input features')

        self.intermediate_dncnn = IntermediateDnCNN(\
                input_features=self.downsampled_channels,\
                middle_features=self.num_feature_maps,\
                num_conv_layers=self.num_conv_layers)

    def forward(self, x, noise_sigma):
        # Handle odd sizes
        expanded_h = x.shape[2] % 2
        expanded_w = x.shape[3] % 2
        x = F.pad(x, (0,expanded_w,0,expanded_h), 'reflect')

        concat_noise_x = concatenate_input_noise_map(x.data, noise_sigma.data)
        h_dncnn = self.intermediate_dncnn(concat_noise_x)
        denoised = x - upsamplefeatures(h_dncnn)

        if expanded_h:
            denoised = denoised[:,:,:-1,:]
        if expanded_w:
            denoised = denoised[:,:,:,:-1]

        return denoised

    def load(self):
        root = os.path.abspath(os.path.dirname(__file__))
        if self.num_input_channels == 3:
            model_fn = 'ffdnet_weights_rgb.pth'
        else:
            model_fn = 'ffdnet_weights_gray.pth'
        model_fn = os.path.join(root, model_fn)
        state_dict = torch.load(model_fn, map_location='cpu')
        state_dict = remove_dataparallel_wrapper(state_dict)
        self.load_state_dict(state_dict)


def run(img, sigma, normalization=None, gpu=False):
    img = img.transpose(2, 0, 1)
    img = np.expand_dims(img, 0)
    img = torch.Tensor(img)

    nsigma = torch.FloatTensor([sigma])

    if gpu:
        img = img.cuda()
        nsigma = nsigma.cuda()

    if normalization is None:
        normalization = img.max()
    img /= normalization
    nsigma /= normalization

    net = FFDNet(num_input_channels=img.shape[1])
    net.load()
    net.eval()
    if gpu:
        net.cuda()

    with torch.no_grad():
        denoised = net(img, nsigma)

    denoised = denoised * normalization
    denoised = denoised.cpu().numpy()[0]
    denoised = denoised.transpose(1, 2, 0)
    return denoised

def cli(input, sigma, output, gpu=False):
    import imageio
    if gpu and not torch.cuda.is_available():
        print('Asked for GPU but not available, falling back to CPU.')
        gpu = False
    img = imageio.imread(input)
    img = np.atleast_3d(img)
    denoised = run(img, sigma, gpu=gpu)
    imageio.imwrite(output, denoised)

def cli_main():
    import fire
    fire.Fire(cli)

if __name__ == "__main__":
    cli_main()

