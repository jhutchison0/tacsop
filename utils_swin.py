# -*- coding: utf-8 -*-
"""
Created on Tue Oct 07 11:00:00 2023

@author: jhutchison

"""

# %% Packages
""" Third party and local imports """

import pathlib
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# %% Functions
""" Define functions """


def window_partition(x, window_size):
    """
    Partition input into non-overlapping windows.

    Args:
        x (torch.Tensor): Input tensor of shape (B, D, H, W, C)
        window_size (int): Size of the window

    Returns:
        torch.Tensor: Windows of shape (num_windows * B, window_size, window_size, window_size, C)
    """
    B, D, H, W, C = x.shape
    x = x.view(
        B,
        D // window_size,
        window_size,
        H // window_size,
        window_size,
        W // window_size,
        window_size,
        C,
    )
    windows = x.permute(0, 1, 3, 5, 2, 4, 6, 7).contiguous()
    windows = windows.view(-1, window_size, window_size, window_size, C)
    return windows


def window_reverse(windows, window_size, D, H, W):
    """
    Reverse the window partition to reconstruct the original tensor.

    Args:
        windows (torch.Tensor): Windows of shape (num_windows * B, window_size, window_size, window_size, C)
        window_size (int): Size of the window
        D, H, W (int): Original depth, height, and width

    Returns:
        torch.Tensor: Reconstructed tensor of shape (B, D, H, W, C)
    """
    B = int(windows.shape[0] / (D * H * W / window_size**3))
    x = windows.view(
        B,
        D // window_size,
        H // window_size,
        W // window_size,
        window_size,
        window_size,
        window_size,
        -1,
    )
    x = x.permute(0, 1, 4, 2, 5, 3, 6, 7).contiguous()
    x = x.view(B, D, H, W, -1)
    return x


class MLP(nn.Module):
    """
    Multilayer Perceptron (MLP) with GELU activation and dropout.
    """

    def __init__(self, dim, hidden_dim, dropout=0.0):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(dim, hidden_dim)
        self.act = nn.GELU()
        self.fc2 = nn.Linear(hidden_dim, dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        x = self.dropout(self.act(self.fc1(x)))
        x = self.dropout(self.fc2(x))
        return x


class WindowAttention3D(nn.Module):
    """
    3D Window-based Multi-head Self-Attention module with relative position bias.
    """

    def __init__(self, dim, window_size, num_heads, dropout=0.0):
        super(WindowAttention3D, self).__init__()
        self.dim = dim
        self.window_size = window_size  # Window size (int)
        self.num_heads = num_heads
        head_dim = dim // num_heads
        self.scale = head_dim**-0.5

        # Relative position bias table
        self.relative_position_bias_table = nn.Parameter(
            torch.zeros(
                (2 * window_size - 1) ** 3,
                num_heads,
            )
        )

        # Compute relative position index
        coords_d = torch.arange(window_size)
        coords_h = torch.arange(window_size)
        coords_w = torch.arange(window_size)
        coords = torch.stack(
            torch.meshgrid([coords_d, coords_h, coords_w], indexing="ij")
        )
        coords_flatten = coords.reshape(3, -1)
        relative_coords = coords_flatten[:, :, None] - coords_flatten[:, None, :]
        relative_coords = relative_coords.permute(1, 2, 0).contiguous()
        relative_coords += window_size - 1
        relative_coords[:, :, 0] *= (2 * window_size - 1) ** 2
        relative_coords[:, :, 1] *= 2 * window_size - 1
        relative_position_index = relative_coords.sum(-1)
        self.register_buffer("relative_position_index", relative_position_index)

        self.qkv = nn.Linear(dim, dim * 3, bias=True)
        self.attn_dropout = nn.Dropout(dropout)
        self.proj = nn.Linear(dim, dim)
        self.proj_dropout = nn.Dropout(dropout)

    def forward(self, x):
        B_, N, C = x.shape  # N = window_size^3
        qkv = self.qkv(x).reshape(B_, N, 3, self.num_heads, C // self.num_heads)
        qkv = qkv.permute(2, 0, 3, 1, 4)  # Shape: (3, B_, num_heads, N, head_dim)
        q, k, v = qkv[0], qkv[1], qkv[2]

        q = q * self.scale
        attn = q @ k.transpose(-2, -1)  # Shape: (B_, num_heads, N, N)

        relative_position_bias = self.relative_position_bias_table[
            self.relative_position_index.view(-1)
        ]
        relative_position_bias = relative_position_bias.view(
            self.window_size**3, self.window_size**3, -1
        )
        relative_position_bias = relative_position_bias.permute(
            2, 0, 1
        )  # Shape: (num_heads, N, N)
        attn = attn + relative_position_bias.unsqueeze(0)

        attn = F.softmax(attn, dim=-1)
        attn = self.attn_dropout(attn)

        x = (attn @ v).transpose(1, 2).reshape(B_, N, C)
        x = self.proj_dropout(self.proj(x))
        return x


class SwinTransformerBlock3D(nn.Module):
    """
    Swin Transformer Block for 3D data with shifted windows.
    """

    def __init__(
        self,
        dim,
        input_resolution,
        num_heads,
        window_size,
        shift_size=0,
        mlp_ratio=4.0,
        dropout=0.0,
    ):
        super(SwinTransformerBlock3D, self).__init__()
        self.dim = dim
        self.input_resolution = input_resolution  # (D, H, W)
        self.num_heads = num_heads
        self.window_size = window_size
        self.shift_size = shift_size

        self.norm1 = nn.LayerNorm(dim)
        self.attn = WindowAttention3D(
            dim, window_size=window_size, num_heads=num_heads, dropout=dropout
        )

        self.norm2 = nn.LayerNorm(dim)
        mlp_hidden_dim = int(dim * mlp_ratio)
        self.mlp = MLP(dim, mlp_hidden_dim, dropout=dropout)

    def forward(self, x):
        # x: (B, D, H, W, C)
        D, H, W = self.input_resolution
        B, Dp, Hp, Wp, C = x.shape

        shortcut = x
        x = self.norm1(x)

        # Pad feature maps to be divisible by window size
        pad_d = (self.window_size - Dp % self.window_size) % self.window_size
        pad_h = (self.window_size - Hp % self.window_size) % self.window_size
        pad_w = (self.window_size - Wp % self.window_size) % self.window_size
        x = F.pad(x, (0, 0, 0, pad_w, 0, pad_h, 0, pad_d))

        _, Dp, Hp, Wp, _ = x.shape

        # Cyclic shift
        if self.shift_size > 0:
            shifted_x = torch.roll(
                x,
                shifts=(-self.shift_size, -self.shift_size, -self.shift_size),
                dims=(1, 2, 3),
            )
        else:
            shifted_x = x

        # Partition windows
        x_windows = window_partition(
            shifted_x, self.window_size
        )  # Shape: (num_windows * B, ws, ws, ws, C)
        x_windows = x_windows.view(
            -1, self.window_size**3, C
        )  # Shape: (num_windows * B, ws^3, C)

        # Attention
        attn_windows = self.attn(x_windows)

        # Merge windows
        attn_windows = attn_windows.view(
            -1, self.window_size, self.window_size, self.window_size, C
        )
        shifted_x = window_reverse(
            attn_windows, self.window_size, Dp, Hp, Wp
        )  # Shape: (B, Dp, Hp, Wp, C)

        # Reverse cyclic shift
        if self.shift_size > 0:
            x = torch.roll(
                shifted_x,
                shifts=(self.shift_size, self.shift_size, self.shift_size),
                dims=(1, 2, 3),
            )
        else:
            x = shifted_x

        # Remove padding
        x = x[:, :D, :H, :W, :]

        # Residual connection
        x = shortcut + x

        # Feed-forward network
        x = x + self.mlp(self.norm2(x))
        return x


class BasicLayer(nn.Module):
    """
    A basic Swin Transformer layer for one stage.
    """

    def __init__(
        self,
        dim,
        input_resolution,
        depth,
        num_heads,
        window_size,
        mlp_ratio=4.0,
        dropout=0.0,
    ):
        super(BasicLayer, self).__init__()
        self.blocks = nn.ModuleList()
        for i in range(depth):
            shift_size = 0 if (i % 2 == 0) else window_size // 2
            block = SwinTransformerBlock3D(
                dim=dim,
                input_resolution=input_resolution,
                num_heads=num_heads,
                window_size=window_size,
                shift_size=shift_size,
                mlp_ratio=mlp_ratio,
                dropout=dropout,
            )
            self.blocks.append(block)

    def forward(self, x):
        for block in self.blocks:
            x = block(x)
        return x


class SwinTransformer3D(nn.Module):
    """
    Swin Transformer Model for 3D data.
    """

    def __init__(
        self,
        input_channels=2,
        embed_dim=96,
        depths=[2, 2, 6, 2],
        num_heads=[3, 6, 12, 24],
        window_size=4,
        mlp_ratio=4.0,
        dropout=0.0,
        num_classes=1,
    ):
        super(SwinTransformer3D, self).__init__()

        self.embed_dim = embed_dim
        self.patch_embed = nn.Conv3d(
            input_channels, embed_dim, kernel_size=4, stride=4, padding=0
        )
        self.pos_drop = nn.Dropout(p=dropout)

        # Build layers
        self.layers = nn.ModuleList()
        for i_layer in range(len(depths)):
            input_res = (
                (64 // (2**i_layer)) // 4,  # Adjusted for patch embedding
                (64 // (2**i_layer)) // 4,
                (64 // (2**i_layer)) // 4,
            )
            layer = BasicLayer(
                dim=int(embed_dim * 2**i_layer),
                input_resolution=input_res,
                depth=depths[i_layer],
                num_heads=num_heads[i_layer],
                window_size=window_size,
                mlp_ratio=mlp_ratio,
                dropout=dropout,
            )
            self.layers.append(layer)

        self.norm = nn.LayerNorm(int(embed_dim * 2 ** (len(depths) - 1)))
        self.head = nn.Linear(int(embed_dim * 2 ** (len(depths) - 1)), num_classes)

    def forward(self, x):
        # x: (B, C, D, H, W)
        x = self.patch_embed(x)  # Shape: (B, embed_dim, D', H', W')
        x = x.permute(0, 2, 3, 4, 1).contiguous()  # Shape: (B, D', H', W', C)
        x = self.pos_drop(x)

        for layer in self.layers:
            x = layer(x)

        x = self.norm(x)
        x = x.mean(dim=(1, 2, 3))  # Global average pooling
        x = self.head(x)
        return x


# %% Variables
""" Set script (global) variables """

path_data = pathlib.Path("data/")

# Hyperparameters and configurations
input_channels = 2  # Number of input features (e.g., precipitation and soil moisture)
embed_dim = 96
depths = [2, 2, 6, 2]
num_heads = [3, 6, 12, 24]
window_size = 4
mlp_ratio = 4.0
dropout = 0.1
num_classes = 1  # Predicting runoff
learning_rate = 1e-4
num_epochs = 10  # Adjust as needed
batch_size = 2  # Adjust based on hardware capabilities
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Data dimensions (adjust according to your data)
D = 64  # Temporal dimension (number of time steps)
H = 64  # Spatial height
W = 64  # Spatial width

# %% Main
""" Main execution code """


def main():
    # Placeholder for data loading and preprocessing
    # Replace with your actual data loading logic
    x = torch.randn(batch_size, input_channels, D, H, W).to(device)
    target = torch.randn(batch_size, num_classes).to(
        device
    )  # Replace with actual targets

    # Initialize the model
    model = SwinTransformer3D(
        input_channels=input_channels,
        embed_dim=embed_dim,
        depths=depths,
        num_heads=num_heads,
        window_size=window_size,
        mlp_ratio=mlp_ratio,
        dropout=dropout,
        num_classes=num_classes,
    ).to(device)

    # Define loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # Training loop
    try:
        for epoch in range(num_epochs):
            model.train()
            optimizer.zero_grad()
            output = model(x)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

            print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}")

    except Exception as e:
        print(f"An error occurred during training: {e}")

    print("Training complete")


if __name__ == "__main__":
    main()
