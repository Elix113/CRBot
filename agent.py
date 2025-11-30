import os
import pickle
import torch
import torch.nn as nn
import torch.nn.functional as F
import random
import numpy as np
from collections import deque

# 1. Q-Network
class QNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super().__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_size)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)  # Q-Werte für jede Aktion

# 2. DQN Agent
class DQNAgent:
    def __init__(self, state_size, action_size, lr=1e-3):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=10000)
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = QNetwork(state_size, action_size)

        self.target_model = QNetwork(state_size, action_size)
        self.target_model.load_state_dict(self.model.state_dict())
        self.update_rate = 1000
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        self.step_count = 0

    # 3. Aktionswahl
    def act(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.action_size)
        state = torch.tensor(state, dtype=torch.float32)
        q_values = self.model(state)
        return torch.argmax(q_values).item()

    # 4. Erfahrung speichern
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    # 5. Training
    def replay(self, batch_size=32):
        if len(self.memory) < batch_size:
            return

        batch = random.sample(self.memory, batch_size)

        # States und Next States in Batch Tensor
        states = torch.tensor([s for s, a, r, ns, d in batch], dtype=torch.float32)
        next_states = torch.tensor([ns for s, a, r, ns, d in batch], dtype=torch.float32)
        actions = torch.tensor([a for s, a, r, ns, d in batch])
        rewards = torch.tensor([r for s, a, r, ns, d in batch], dtype=torch.float32)
        dones = torch.tensor([d for s, a, r, ns, d in batch], dtype=torch.bool)

        # Q-Values des aktuellen Netzwerks
        q_values = self.model(states)
        # Q-Values des Target Netzwerks für next_state
        next_q_values = self.target_model(next_states)

        # Double DQN: best_action via model, target via target_model
        next_actions = torch.argmax(self.model(next_states), dim=1)
        target = rewards + self.gamma * next_q_values[range(batch_size), next_actions] * (~dones)

        # Berechne Loss
        loss = F.mse_loss(q_values[range(batch_size), actions], target)

        # Update
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Epsilon decay
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        # Target Network aktualisieren
        self.step_count += 1
        if self.step_count % self.update_rate == 0:
            self.target_model.load_state_dict(self.model.state_dict())

    def save(self, folder="save"):
        os.makedirs(folder, exist_ok=True)

        # 1. Modell speichern
        model_path = os.path.join(folder, "model.pth")
        torch.save(self.model.state_dict(), model_path)

        # 2. Replay Memory speichern
        memory_path = os.path.join(folder, "memory.pkl")
        with open(memory_path, "wb") as f:
            pickle.dump(self.memory, f)

        # 3. Epsilon speichern
        epsilon_path = os.path.join(folder, "epsilon.pkl")
        with open(epsilon_path, "wb") as f:
            pickle.dump(self.epsilon, f)

        print("[✔] Agent erfolgreich gespeichert.")


    def load(self, folder="save"):
        model_path = os.path.join(folder, "model.pth")
        memory_path = os.path.join(folder, "memory.pkl")
        epsilon_path = os.path.join(folder, "epsilon.pkl")

        loaded_anything = False

        # 1. Modell laden
        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path))
            loaded_anything = True

        # 2. Replay Memory laden
        if os.path.exists(memory_path):
            with open(memory_path, "rb") as f:
                self.memory = pickle.load(f)
            loaded_anything = True

        # 3. Epsilon laden
        if os.path.exists(epsilon_path):
            with open(epsilon_path, "rb") as f:
                self.epsilon = pickle.load(f)
            loaded_anything = True

        if loaded_anything:
            print("[✔] Agent erfolgreich geladen.")
        else:
            print("[ℹ] Keine gespeicherten Daten gefunden – frischer Start.")
