import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import glob
from tqdm import tqdm

# --- Dataset Definition ---

class StructureDataset(Dataset):
    """
    Generalized dataset for 1D (temporal) or 3D (Hopfion) simulations.
    """
    def __init__(self, data_dirs):
        self.file_list = []
        if isinstance(data_dirs, str):
            data_dirs = [data_dirs]
        for d in data_dirs:
            if os.path.exists(d):
                self.file_list.extend(glob.glob(os.path.join(d, "*.npz")))
        
    def __len__(self):
        return len(self.file_list)
    
    def __getitem__(self, idx):
        file_path = self.file_list[idx]
        data = np.load(file_path, allow_pickle=True)
        
        # Load intensity
        if 'animation_history' in data:
            sequence = data['animation_history'].astype(np.float32)
        elif 'stored_fields' in data:
            stored = data['stored_fields']
            # Reconstruction for old data
            if isinstance(stored[0], (list, tuple, np.ndarray)) and len(stored[0]) == 2:
                sequence = np.array([np.abs(f[0])**2 + np.abs(f[1])**2 for f in stored]).astype(np.float32)
            else:
                sequence = np.abs(stored).astype(np.float32)
        else:
            return torch.zeros((1, 8, 8)), torch.tensor([0.0]), "unknown", file_path
        
        # Determine Type and Dims
        # sequence shape is (steps, ...)
        steps = sequence.shape[0]
        data_dims = sequence.ndim - 1 # 1D temporal -> ndim 2, 3D Hopfion -> ndim 4
        
        # 1. Universal Stability Heuristic
        flat_spatial = sequence.reshape(steps, -1)
        peaks = np.max(flat_spatial, axis=1)
        stability_score = 1.0 / (1.0 + np.std(peaks) / (np.mean(peaks) + 1e-9))
        
        # 2. Tensor Prep
        if data_dims == 1:
            data_type = "Soliton"
            # Keep full evolution for 1D/2D
            norm_seq = sequence / (np.max(sequence) + 1e-9)
            tensor = torch.from_numpy(norm_seq).unsqueeze(0)
        else:
            data_type = "Hopfion"
            # For 3D, take only the final state to keep memory low
            final_frame = sequence[-1]
            final_frame /= (np.max(final_frame) + 1e-9)
            tensor = torch.from_numpy(final_frame).unsqueeze(0)
            
        return tensor, torch.tensor([stability_score], dtype=torch.float32), data_type, file_path

# --- Simple Models ---

class SolitonModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d((4, 4)),
            nn.Flatten(), nn.Linear(16*4*4, 1)
        )
    def forward(self, x): return self.net(x)

class HopfionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv3d(1, 8, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool3d((2, 2, 2)),
            nn.Flatten(), nn.Linear(8*2*2*2, 1)
        )
    def forward(self, x): return self.net(x)

# --- Analysis Logic ---

def analyze_all(paths):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dataset = StructureDataset(paths)
    if not dataset: return
    loader = DataLoader(dataset, batch_size=1)
    
    soliton_net = SolitonModel().to(device)
    hopfion_net = HopfionModel().to(device)
    
    results = {'Soliton': [], 'Hopfion': []}
    
    print(f"Analyzing {len(dataset)} simulations...")
    
    for tensor, heuristic, data_type, file_path in tqdm(loader, desc="Processing files"):
        dtype = data_type[0]
        if dtype not in results: continue
        
        # For this turn, we just use the heuristic for ranking
        results[dtype].append({
            'file': os.path.basename(file_path[0]),
            'stability': heuristic.item()
        })

    for category in ['Soliton', 'Hopfion']:
        cat_results = results[category]
        cat_results.sort(key=lambda x: x['stability'], reverse=True)
        
        print(f"\n--- TOP 5 STABLE {category.upper()}S ---")
        if not cat_results:
            print("No data found.")
            continue
            
        for i, res in enumerate(cat_results[:5]):
            print(f"{i+1}. {res['file']} | Stability: {res['stability']:.4f}")

if __name__ == "__main__":
    PATHS = [
        "results/sweep_temporal",
        "results/sweep_hopfion_single",
        "results/sweep_hopfion_interaction"
    ]
    analyze_all(PATHS)