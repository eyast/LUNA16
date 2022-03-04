from LUNA16.utils.LUNAdatastore import LUNAdatastore_position
from LUNA16.utils.xyz_net import xyz_net2
import torch
from torch.utils.data import DataLoader
from torch.optim import Adam
from torch.nn import BCELoss
import wandb

wandb.init(project="LUNA_xyz")

train_size = 100000
val_size = 7500
epochs = 200
ds = LUNAdatastore_position(len=train_size)

vs = LUNAdatastore_position(len=val_size)
dl = DataLoader(ds, 4, shuffle=True)
val = DataLoader(ds, 4, shuffle=True)

model_test = xyz_net2().to('cuda')
opt = Adam(model_test.parameters(), lr=1e-3)
criterion = BCELoss()

for i in range(epochs):
    epoch_loss = 0
    val_loss = 0
    count = 0
    eval_count = 0
    correct = 0
    val_correct = 0
    accuracy = 0
    val_accuracy = 0
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
        correct += (preds_thr == label).float().sum()
    epoch_loss = epoch_loss / count
    accuracy = 100 * correct / len(ds)
    torch.set_grad_enabled(False)
    for k, mini_batch in enumerate(val):
        model_test.eval()
        data = mini_batch["data"].to('cuda')
        label = mini_batch["label"].to('cuda')
        preds = model_test(data)
        loss = criterion(preds, label).mean()
        val_loss += loss
        eval_count += 1
        preds_thr = (preds > 0.5).float()
        val_correct += (preds_thr == label).float().sum()
    val_loss = val_loss / eval_count
    val_accuracy = 100 * val_correct / len(vs)
    wandb.log(data={
        't_loss': epoch_loss,
        'v_loss': val_loss,
        't_acc': accuracy,
        'v_acc': val_accuracy
    })
    print (f"{i}:\t t_loss: {epoch_loss}:\t \
                t_acc: {accuracy}:\t val_loss: {val_loss}:\t val_acc: {val_accuracy}")