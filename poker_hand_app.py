import streamlit as st
import random
from collections import Counter
import matplotlib.pyplot as plt
import os

# --- Setup ---
ranks = '23456789TJQKA'
suits_symbols = {'S': '♠️', 'H': '♥️', 'D': '♦️', 'C': '♣️'}
suits_list = ['S', 'H', 'D', 'C']
deck = [r + s for r in ranks for s in suits_list]
card_folder = "cards"

hand_probabilities = {
    "Royal Flush": 0.000154,
    "Straight Flush": 0.00139,
    "Four of a Kind": 0.02401,
    "Full House": 0.1441,
    "Flush": 0.197,
    "Straight": 0.3925,
    "Three of a Kind": 2.1128,
    "Two Pair": 4.7539,
    "One Pair": 42.2569,
    "High Card": 50.1177
}

# --- Functions ---
def classify_hand(hand):
    ranks_only = [card[0] for card in hand]
    suits_only = [card[1] for card in hand]
    rank_counts = Counter(ranks_only).values()
    is_flush = len(set(suits_only)) == 1
    sorted_indices = sorted([ranks.index(r) for r in ranks_only])
    is_straight = sorted_indices == list(range(min(sorted_indices), min(sorted_indices) + 5))
    
    if is_straight and is_flush and 'T' in ranks_only:
        return "Royal Flush"
    elif is_straight and is_flush:
        return "Straight Flush"
    elif 4 in rank_counts:
        return "Four of a Kind"
    elif 3 in rank_counts and 2 in rank_counts:
        return "Full House"
    elif is_flush:
        return "Flush"
    elif is_straight:
        return "Straight"
    elif 3 in rank_counts:
        return "Three of a Kind"
    elif list(rank_counts).count(2) == 2:
        return "Two Pair"
    elif 2 in rank_counts:
        return "One Pair"
    else:
        return "High Card"

def draw_hand():
    return random.sample(deck, 5)

def simulate(num_simulations=100000):
    counts = {key: 0 for key in hand_probabilities.keys()}
    for _ in range(num_simulations):
        hand = draw_hand()
        hand_type = classify_hand(hand)
        counts[hand_type] += 1
    return {k: (v / num_simulations) * 100 for k, v in counts.items()}

def display_card_images(hand):
    cols = st.columns(len(hand))
    for idx, card in enumerate(hand):
        card_filename = f"{card}.png"
        card_path = os.path.join(card_folder, card_filename)
        cols[idx].image(card_path, use_column_width=True)

# --- UI ---
st.set_page_config("Ultimate Poker Hand Calculator", page_icon="🃏", layout="centered")
st.title("🃏 Ultimate Poker Hand Probability Calculator")
st.markdown("Deal a hand, visualize it, analyze probabilities, and simulate outcomes!")

if st.button("🎲 Deal Hand"):
    hand = draw_hand()
    hand_type = classify_hand(hand)
    probability = hand_probabilities[hand_type]

    st.subheader("🎴 Your Hand:")
    display_card_images(hand)

    st.success(f"🧠 Hand Type: **{hand_type}**")
    st.info(f"📊 Theoretical Probability: **{probability:.5f}%**")

    with st.expander("📈 Show Simulation (100,000 Hands)"):
        with st.spinner("Simulating hands..."):
            sim_result = simulate()
            fig, ax = plt.subplots(figsize=(10, 4))
            labels = list(sim_result.keys())
            values = list(sim_result.values())
            bars = ax.barh(labels, values, color='lightgreen')
            for bar in bars:
                ax.text(bar.get_width(), bar.get_y() + 0.1, f"{bar.get_width():.3f}%", va='center')
            ax.set_xlabel("Simulated Probability (%)")
            ax.set_title("Simulated Poker Hand Probabilities")
            st.pyplot(fig)
else:
    st.info("👆 Click the button to deal a new hand!")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align:center; font-size: 0.9em;'>Made with ❤️ using Streamlit</div>",
    unsafe_allow_html=True
)
