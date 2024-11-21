import torch  
import torch.nn as nn  
import torch.optim as optim  
import torchvision  
import torchvision.transforms as transforms  
import matplotlib.pyplot as plt  
  
# ハイパーパラメータ  
batch_size = 64  
learning_rate = 0.0002  
num_epochs = 200  
latent_size = 100  
image_size = 784 # 28x28  
hidden_size = 256  
  
# データロード  
transform = transforms.Compose([  
    transforms.ToTensor(),  
    transforms.Normalize(mean=(0.5,), std=(0.5,))  
])  
  
mnist = torchvision.datasets.MNIST(root='./data', train=True, transform=transform, download=True)  
dataloader = torch.utils.data.DataLoader(mnist, batch_size=batch_size, shuffle=True)  
  
# 生成器の定義  
class Generator(nn.Module):  
    def __init__(self):  
        super(Generator, self).__init__()  
        self.model = nn.Sequential(  
            nn.Linear(latent_size, hidden_size),  
            nn.ReLU(True),  
            nn.Linear(hidden_size, hidden_size),  
            nn.ReLU(True),  
            nn.Linear(hidden_size, image_size),  
            nn.Tanh()  
        )  
  
    def forward(self, x):  
        return self.model(x)  
  
# 識別器の定義  
class Discriminator(nn.Module):  
    def __init__(self):  
        super(Discriminator, self).__init__()  
        self.model = nn.Sequential(  
            nn.Linear(image_size, hidden_size),  
            nn.LeakyReLU(0.2, inplace=True),  
            nn.Linear(hidden_size, hidden_size),  
            nn.LeakyReLU(0.2, inplace=True),  
            nn.Linear(hidden_size, 1),  
            nn.Sigmoid()  
        )  
  
    def forward(self, x):  
        return self.model(x)  
  
# モデルの初期化  
generator = Generator()  
discriminator = Discriminator()  
  
# ロス関数と最適化  
criterion = nn.BCELoss()  
optimizer_g = optim.Adam(generator.parameters(), lr=learning_rate)  
optimizer_d = optim.Adam(discriminator.parameters(), lr=learning_rate)  
  
# トレーニングループ  
for epoch in range(num_epochs):  
    for i, (images, _) in enumerate(dataloader):  
        # 本物のデータ  
        real_images = images.view(batch_size, -1)  
        real_labels = torch.ones(batch_size, 1)  
  
        # 偽のデータ  
        z = torch.randn(batch_size, latent_size)  
        fake_images = generator(z)  
        fake_labels = torch.zeros(batch_size, 1)  
  
        # 識別器のトレーニング  
        outputs = discriminator(real_images)  
        d_loss_real = criterion(outputs, real_labels)  
        real_score = outputs  
  
        outputs = discriminator(fake_images.detach())  
        d_loss_fake = criterion(outputs, fake_labels)  
        fake_score = outputs   
        d_loss = d_loss_real + d_loss_fake  
  
        # 識別器の最適化  
        optimizer_d.zero_grad()  
        d_loss.backward()  
        optimizer_d.step()  
  
        # 生成器のトレーニング  
        z = torch.randn(batch_size, latent_size)  
        fake_images = generator(z)  
        outputs = discriminator(fake_images)  
        g_loss = criterion(outputs, real_labels)  
  
        # 生成器の最適化  
        optimizer_g.zero_grad()  
        g_loss.backward()  
        optimizer_g.step()  
  
        if (i+1) % 200 == 0:  
            print(f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{len(dataloader)}], D Loss: {d_loss.item():.4f}, G Loss: {g_loss.item():.4f}, D(x): {real_score.mean().item():.2f}, D(G(z)): {fake_score.mean().item():.2f}')  
  
    # 生成画像の表示  
    if (epoch+1) % 10 == 0:  
        with torch.no_grad():  
            fake_images = fake_images.reshape(fake_images.size(0), 1, 28, 28)  
            fake_images = fake_images / 2 + 0.5  # デノーマライズ  
            grid = torchvision.utils.make_grid(fake_images)  
            plt.imshow(grid.permute(1, 2, 0).cpu().numpy())  
            plt.show()  
  
# モデルの保存  
torch.save(generator.state_dict(), 'generator.pth')  
torch.save(discriminator.state_dict(), 'discriminator.pth')  

