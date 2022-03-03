import torch.nn as nn
from torch.optim import Adam
from torch.nn import BCELoss

class xyz_net2(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc_1 = nn.Linear(3, 128)
        self.sig_1 = nn.Sigmoid()
        self.fc_2 = nn.Linear(128, 512)
        self.sig_2 = nn.Sigmoid()
        self.fc_3 = nn.Linear(512, 10)
        self.sig_3 = nn.Sigmoid()
        self.fc_4 = nn.Linear(10, 1)
        self.sig_4 = nn.Sigmoid()

    def forward(self, x):
        passed = self.fc_1(x)
        passed = self.sig_1(passed)
        passed = self.fc_2(passed)
        passed = self.sig_2(passed)
        passed = self.fc_3(passed)
        passed = self.sig_3(passed)
        passed = self.fc_4(passed)
        passed = self.sig_4(passed)
        return passed
