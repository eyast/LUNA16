from LUNA16.utils.LUNAdatastore import LUNAdatastore_position
from LUNA16.utils.xyz_net import xyz_net2
import torch
from torch.utils.data import DataLoader
from torch.optim import Adam
from torch.nn import BCELoss
from sklearn.metrics import accuracy_score, precision_score, recall_score
ds = LUNAdatastore_position()
dl = DataLoader(ds, 4)
val = DataLoader(ds, 4)

model_test = xyz_net2().to('cuda')
opt = Adam(model_test.parameters(), lr=1e-3)
criterion = BCELoss()

for i in range(20):
    epoch_loss = 0
    eval_loss = 0
    count = 0
    eval_count = 0
    correct = 0
    torch.set_grad_enabled(True)
    for j, mini_batch in enumerate(dl):
        opt.zero_grad()
        model_test.train()
        data = mini_batch["data"].to('cuda')
        label = mini_batch["label"].to('cuda')
        preds = model_test(data)
        loss = criterion(preds, label).mean()
        epoch_loss += loss
        count += 1
        loss.backward()
        opt.step()
        preds_thr = (preds > 0.5).float()
        accuracy = precision_score(label.cpu().numpy(), preds_thr.cpu().numpy())
        print(accuracy)
        #correct += (preds == label).float().sum()
    accuracy = 100 * correct / len(ds)
    print (f"{i}:\t{j}:\t{epoch_loss/count}:\t{accuracy}")