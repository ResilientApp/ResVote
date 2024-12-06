from typing import List
from .datatype import Vote
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

def visualize_votes(votes: List[Vote], output_image: str = "data/chart.png"):
    

    election_dict = defaultdict(lambda: Counter())
    for v in votes:
        election_dict[v.election_id][v.candidate_name] += 1

    # For demonstration: only process the first election_id
    for election_id, counts in election_dict.items():
        candidates = list(counts.keys())
        votes_counts = list(counts.values())

        plt.figure(figsize=(6,4))
        plt.bar(candidates, votes_counts)
        plt.title(f"Election: {election_id}")
        plt.xlabel("Candidates")
        plt.ylabel("Votes")

        # Save the chart as an image file
        plt.savefig(f"{election_id}_{output_image}")
        plt.close()
