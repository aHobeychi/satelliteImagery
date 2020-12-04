import torch.nn as nn


class Block(nn.Module):
    """
    Residual Block
    """
    def __init__(
        self, n_in, n_out, iden_downsample=None, stride=1
    ):
        super(Block, self).__init__()
        self.expansion = 4
        self.cnn_layers = nn.Sequential(
          nn.Conv2d(n_in, n_out, kernel_size=1, stride=1, padding=0),
          nn.BatchNorm2d(n_out),
          nn.ReLU(inplace=True),
          nn.Conv2d(n_out, n_out, kernel_size=3, stride=stride, padding=1),
          nn.BatchNorm2d(n_out),
          nn.ReLU(inplace=True),
          nn.Conv2d(n_out, n_out * self.expansion, kernel_size=1, stride=1,
                    padding=0),
          nn.BatchNorm2d(n_out * self.expansion),
        )
        self.relu = nn.ReLU()
        self.iden_downsample = iden_downsample
        self.stride = stride

    def forward(self, x):
        """
        Forward Pass of the residual block
        """
        identity = x.clone()
        x = self.cnn_layers(x)
        if self.iden_downsample is not None:
            identity = self.iden_downsample(identity)
        x += identity
        x = self.relu(x)
        return x


class ResNet(nn.Module):
    """
    Resnet Model
    """
    def __init__(self, block, layers, image_channels, num_classes):
        super(ResNet, self).__init__()
        self.in_channels = 64
        self.name = 'Resnet.pt'

        self.cnn_layers = nn.Sequential(
          nn.Conv2d(image_channels, 64, kernel_size=7, stride=2, padding=3),
          nn.BatchNorm2d(64),
          nn.ReLU(),
          nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
        )

        self.residual_layers = nn.Sequential(
          self.create_layer(block, layers[0], inter_chan=64, stride=1),
          self.create_layer(block, layers[1], inter_chan=128, stride=2),
          self.create_layer(block, layers[2], inter_chan=256, stride=2),
          self.create_layer(block, layers[3], inter_chan=512, stride=2)
        )

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * 4, num_classes)

    def forward(self, x):
        """
        Forward Propagate
        """
        x = self.cnn_layers(x)
        x = self.residual_layers(x)
        x = self.avgpool(x)
        x = x.reshape(x.shape[0], -1)
        x = self.fc(x)

        return x


    def create_layer(self, Block, num_residual_blocks, inter_chan, stride):
        """
        Creates Residual Layer.
        """
        iden_downsample = None
        layers = []

        if stride != 1 or self.in_channels != inter_chan * 4:
            iden_downsample = nn.Sequential(
                nn.Conv2d(self.in_channels, inter_chan * 4,
                          kernel_size=1, stride=stride,),
                nn.BatchNorm2d(inter_chan * 4),
            )

        layers.append(
            Block(self.in_channels, inter_chan, iden_downsample, stride)
        )

        self.in_channels = inter_chan * 4

        for _ in range(num_residual_blocks - 1):
            layers.append(Block(self.in_channels, inter_chan))

        return nn.Sequential(*layers)


def ResNet50(img_channel=3, num_classes=10):
    """
    Returns A ResNet50.
    """
    return ResNet(Block, [3, 4, 6, 3], img_channel, num_classes)


def ResNet101(img_channel=3, num_classes=10):
    """
    Returns A ResNet101
    """
    return ResNet(Block, [3, 4, 23, 3], img_channel, num_classes)


def ResNet152(img_channel=3, num_classes=10):
    """
    Returns A ResNet152
    """
    return ResNet(Block, [3, 8, 36, 3], img_channel, num_classes)


class Net(nn.Module):
    """
    Standard Cnn Model
    """
    def __init__(self):
        super(Net, self).__init__()
        self.name = 'cnn.pt'

        self.cnn_layers = nn.Sequential(
          nn.BatchNorm2d(3),
          nn.Conv2d(3, 32, kernel_size=5, stride=1, padding=1),  # 62 x 62
          nn.ReLU(inplace=True),
          nn.MaxPool2d(kernel_size=2, stride=2),  # 31 x 31
          nn.Dropout2d(0.1, inplace=True),
          nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
          nn.ReLU(inplace=True),  # 31 x 31
          nn.MaxPool2d(kernel_size=2, stride=2),
          nn.Conv2d(64, 128, kernel_size=5, padding=1, stride=1),
          nn.Dropout2d(0.1, inplace=True),
          nn.ReLU(inplace=True)
        )

        self.linear_layers = nn.Sequential(
          nn.Linear(13*13*128, 256),
          nn.ReLU(inplace=True),
          nn.Linear(256, 128),
          nn.ReLU(inplace=True),
          nn.Linear(128, 64),
          nn.ReLU(inplace=True),
          nn.Linear(64, 10),
        )

    def forward(self, x):
        """
        Forward Propagate
        """
        x = self.cnn_layers(x)
        x = x.view(x.size(0), -1)
        x = self.linear_layers(x)
        return x
