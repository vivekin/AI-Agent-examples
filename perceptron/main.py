import torch
import torch.nn as nn
import torch.nn.functional as F
torch.manual_seed(0)

X = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
AND = torch.tensor([0., 0., 0., 1.])  # yes only when both are 1
XOR = torch.tensor([0., 1., 1., 0.])  # yes when exactly one is 1

def train_perceptron(y, steps=100):
    w = torch.tensor([1., 0.], requires_grad=True)  # a guess: w1, w2
    b = torch.tensor(0., requires_grad=True)        # and the bias
    opt = torch.optim.SGD([w, b], lr=1.0)           # gradient descent
    for step in range(steps):
        total = X @ w + b                           # the weighted sums
        loss = F.binary_cross_entropy_with_logits(total, y)
        opt.zero_grad()
        loss.backward()                             # backpropagation
        opt.step()                                  # w = w - lr * grad
    answer = (X @ w + b >= 0).float()               # the step activation
    return w, b, loss, int((answer != y).sum())

for name, y in [("AND", AND), ("XOR", XOR)]:
    w, b, loss, mistakes = train_perceptron(y)
    print(f"{name}: loss {loss:.2f}, mistakes {mistakes}")

# OUTPUT
# https://colab.research.google.com/drive/1NlA_JC5jis--wwXFfTDGXl6NGYuGueF4#scrollTo=zTe_V81eqBDQ
# AND: loss 0.14, mistakes 0
# XOR: loss 0.69, mistakes 3
