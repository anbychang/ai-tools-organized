"""Train a DQN agent on No-Limit Texas Hold'em for 1 hour."""
import os
import time
import torch
import rlcard
from rlcard.agents import RandomAgent, DQNAgent
from rlcard.utils import get_device, set_seed, tournament, reorganize, Logger, plot_curve

os.environ["CUDA_VISIBLE_DEVICES"] = ""

TRAIN_TIME = 3600  # 1 hour in seconds
EVAL_EVERY = 1000  # evaluate every N episodes
EVAL_GAMES = 1000
SEED = 42
LOG_DIR = "experiments/texas_holdem_1hr/"

device = get_device()
set_seed(SEED)
print(f"Running on: {device}")
print(f"Training for {TRAIN_TIME} seconds ({TRAIN_TIME//60} minutes)...")

env = rlcard.make("no-limit-holdem", config={"seed": SEED})

agent = DQNAgent(
    num_actions=env.num_actions,
    state_shape=env.state_shape[0],
    mlp_layers=[64, 64],
    device=device,
    save_path=LOG_DIR,
    save_every=500,
)

agents = [agent, RandomAgent(num_actions=env.num_actions)]
env.set_agents(agents)

start_time = time.time()
episode = 0

with Logger(LOG_DIR) as logger:
    while True:
        elapsed = time.time() - start_time
        if elapsed >= TRAIN_TIME:
            break

        # Train one episode
        trajectories, payoffs = env.run(is_training=True)
        trajectories = reorganize(trajectories, payoffs)
        for ts in trajectories[0]:
            agent.feed(ts)

        # Evaluate
        if episode % EVAL_EVERY == 0:
            reward = tournament(env, EVAL_GAMES)[0]
            logger.log_performance(episode, reward)
            mins = int(elapsed // 60)
            secs = int(elapsed % 60)
            print(f"  [{mins:02d}:{secs:02d}] Episode {episode:>6d} | Reward: {reward:>+.3f}")

        episode += 1

    # Final evaluation
    reward = tournament(env, EVAL_GAMES)[0]
    logger.log_performance(episode, reward)
    csv_path, fig_path = logger.csv_path, logger.fig_path

# Save
plot_curve(csv_path, fig_path, "dqn")
save_path = os.path.join(LOG_DIR, "model.pth")
torch.save(agent, save_path)

total_time = time.time() - start_time
print(f"\n{'='*50}")
print(f"  Training complete!")
print(f"  Total episodes: {episode}")
print(f"  Total time: {int(total_time//60)}m {int(total_time%60)}s")
print(f"  Final reward: {reward:+.3f}")
print(f"  Model saved: {save_path}")
print(f"  Chart saved: {fig_path}")
print(f"{'='*50}")
