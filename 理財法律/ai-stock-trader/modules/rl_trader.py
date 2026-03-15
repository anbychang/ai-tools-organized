"""模組 C：RL 交易決策 — Q-Learning 學習買賣（純 numpy，無需 torch）"""
import numpy as np
import random
from collections import deque


class TradingEnvironment:
    """股票交易環境"""

    def __init__(self, df, feature_cols, initial_balance=100000):
        self.df = df
        self.feature_cols = feature_cols
        self.initial_balance = initial_balance
        self.reset()

    def reset(self):
        self.step_idx = 0
        self.balance = self.initial_balance
        self.shares = 0
        self.total_trades = 0
        self.history = []
        return self._get_state()

    def _get_state(self):
        row = self.df.iloc[self.step_idx]
        features = row[self.feature_cols].values.astype(np.float64)
        price = row["Close"]
        portfolio = np.array([
            self.balance / self.initial_balance,
            self.shares * price / self.initial_balance,
            self.shares / 100,
        ])
        return np.concatenate([features, portfolio])

    @property
    def state_size(self):
        return len(self.feature_cols) + 3

    def step(self, action):
        """action: 0=持有, 1=買, 2=賣"""
        price = self.df.iloc[self.step_idx]["Close"]
        prev_value = self.balance + self.shares * price

        if action == 1 and self.balance >= price:
            qty = int(self.balance * 0.5 / price)
            if qty > 0:
                self.shares += qty
                self.balance -= qty * price
                self.total_trades += 1
        elif action == 2 and self.shares > 0:
            self.balance += self.shares * price
            self.shares = 0
            self.total_trades += 1

        self.step_idx += 1
        done = self.step_idx >= len(self.df) - 1

        new_price = self.df.iloc[self.step_idx]["Close"]
        new_value = self.balance + self.shares * new_price
        reward = (new_value - prev_value) / self.initial_balance * 100

        self.history.append({
            "step": self.step_idx,
            "action": action,
            "price": float(new_price),
            "balance": self.balance,
            "shares": self.shares,
            "portfolio_value": new_value,
        })

        return self._get_state(), reward, done

    @property
    def portfolio_value(self):
        price = self.df.iloc[self.step_idx]["Close"]
        return self.balance + self.shares * price

    @property
    def total_return(self):
        return (self.portfolio_value - self.initial_balance) / self.initial_balance


class SimpleNN:
    """簡單的 numpy 神經網路（不需要 torch）"""

    def __init__(self, input_size, hidden=64, output_size=3, lr=0.001):
        self.lr = lr
        scale1 = np.sqrt(2.0 / input_size)
        scale2 = np.sqrt(2.0 / hidden)
        self.w1 = np.random.randn(input_size, hidden) * scale1
        self.b1 = np.zeros(hidden)
        self.w2 = np.random.randn(hidden, output_size) * scale2
        self.b2 = np.zeros(output_size)

    def predict(self, x):
        self.z1 = x @ self.w1 + self.b1
        self.a1 = np.maximum(0, self.z1)  # ReLU
        return self.a1 @ self.w2 + self.b2

    def train_step(self, x, target):
        # Forward
        pred = self.predict(x)
        error = pred - target

        # Backward
        dw2 = self.a1.T @ error / len(x)
        db2 = error.mean(axis=0)
        da1 = error @ self.w2.T
        da1[self.z1 <= 0] = 0
        dw1 = x.T @ da1 / len(x)
        db1 = da1.mean(axis=0)

        # Clip gradients
        for g in [dw1, db1, dw2, db2]:
            np.clip(g, -1, 1, out=g)

        self.w1 -= self.lr * dw1
        self.b1 -= self.lr * db1
        self.w2 -= self.lr * dw2
        self.b2 -= self.lr * db2

    def copy_from(self, other):
        self.w1 = other.w1.copy()
        self.b1 = other.b1.copy()
        self.w2 = other.w2.copy()
        self.b2 = other.b2.copy()


class DQNTrader:
    """DQN 交易 Agent（純 numpy）"""

    def __init__(self, state_size, lr=0.001, gamma=0.95):
        self.state_size = state_size
        self.action_size = 3
        self.gamma = gamma
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.memory = deque(maxlen=10000)
        self.model = SimpleNN(state_size, 64, 3, lr)
        self.target_model = SimpleNN(state_size, 64, 3, lr)
        self.target_model.copy_from(self.model)

    def act(self, state, training=True):
        if training and random.random() < self.epsilon:
            return random.randrange(self.action_size)
        q = self.model.predict(state.reshape(1, -1))
        return int(np.argmax(q[0]))

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size=64):
        if len(self.memory) < batch_size:
            return

        batch = random.sample(self.memory, batch_size)
        states = np.array([b[0] for b in batch])
        actions = np.array([b[1] for b in batch])
        rewards = np.array([b[2] for b in batch])
        next_states = np.array([b[3] for b in batch])
        dones = np.array([b[4] for b in batch])

        current_q = self.model.predict(states)
        next_q = self.target_model.predict(next_states)

        target_q = current_q.copy()
        for i in range(batch_size):
            if dones[i]:
                target_q[i][actions[i]] = rewards[i]
            else:
                target_q[i][actions[i]] = rewards[i] + self.gamma * np.max(next_q[i])

        self.model.train_step(states, target_q)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target(self):
        self.target_model.copy_from(self.model)


def train_trader(env, episodes=50):
    """訓練 RL 交易員"""
    print(f"[RL交易] 訓練 DQN Agent（{episodes} 回合）...")
    agent = DQNTrader(env.state_size)
    results = []

    for ep in range(episodes):
        state = env.reset()
        total_reward = 0

        while True:
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            agent.replay()
            state = next_state
            total_reward += reward
            if done:
                break

        agent.update_target()
        ret = env.total_return
        results.append(ret)

        if (ep + 1) % 10 == 0:
            print(f"  Episode {ep+1}/{episodes} | Return: {ret:+.1%} | Trades: {env.total_trades} | eps: {agent.epsilon:.3f}")

    return agent, results
