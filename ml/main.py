import torch
import torch.nn as nn
import torch.optim as optim

# 定义训练数据
training_data = [
    ('打开百度网页', 'python main.py open_url --url=https://www.baidu.com'),
    ('关闭网页', 'python main.py close_url')
]

# 定义词汇表
vocab = {}
for data in training_data:
    for token in data[0].split():
        if token not in vocab:
            vocab[token] = len(vocab)
    for token in data[1].split():
        if token not in vocab:
            vocab[token] = len(vocab)

# 定义模型
class CommandClassifier(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super(CommandClassifier, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.fc1 = nn.Linear(embedding_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = self.embedding(x)
        x = x.mean(dim=1)
        x = nn.functional.relu(self.fc1(x))
        x = nn.functional.log_softmax(self.fc2(x), dim=1)
        return x

# 定义模型超参数
EMBEDDING_DIM = 100
HIDDEN_DIM = 100
OUTPUT_DIM = 2
LEARNING_RATE = 0.01
EPOCHS = 100

# 初始化模型、损失函数和优化器
model = CommandClassifier(len(vocab), EMBEDDING_DIM, HIDDEN_DIM, OUTPUT_DIM)
criterion = nn.NLLLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# 训练模型
for epoch in range(EPOCHS):
    for data in training_data:
        command = data[0]
        target = data[1]

        # 将指令和目标转换为数字序列
        command_sequence = [vocab[token] for token in command.split()]
        target_sequence = [vocab[token] for token in target.split()]

        # 将数字序列转换为PyTorch张量
        command_tensor = torch.LongTensor(command_sequence).unsqueeze(0)
        target_tensor = torch.LongTensor(target_sequence).unsqueeze(0)

        # 将张量输入模型进行预测
        optimizer.zero_grad()
        output = model(command_tensor)

        # 计算损失并反向传播误差
        loss = criterion(output, target_tensor)
        loss.backward()
        optimizer.step()

        # 打印训练结果
        if epoch % 10 == 0:
            print('Epoch:', epoch, 'Loss:', loss.item())

# 测试模型
test_data = [
    '打开百度网页',
    '关闭网页'
    '打开百度'
]

for data in test_data:
    command = data
    command_sequence = [vocab[token] for token in command.split()]
    command_tensor = torch.LongTensor(command_sequence).unsqueeze(0)
    output = model(command_tensor)
    pred = torch.argmax(output, dim=1).item()
    if pred == 0:
        print('执行命令：', training_data[0][1])
    elif pred == 1:
        print('执行命令：',training_data[1][1])