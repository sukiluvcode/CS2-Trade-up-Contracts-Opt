import numpy as np
import matplotlib.pyplot as plt

def trade_up_score(net_income, cost, income_threshold=1000, profit_threshold=3.0):
    """
    Calculate a score for CS2 trade-up contracts that rewards EITHER:
    - High net income (>threshold), OR
    - High profit percentage (>threshold)
    
    Parameters:
    -----------
    net_income : float
        Net income from the trade-up (can be positive or negative)
    cost : float
        Cost of the trade-up (should be positive)
    income_threshold : float, default=1000
        Net income above this is considered "high"
    profit_threshold : float, default=3.0
        Profit multiplier above this is considered "high" (e.g., 3.0 = 300% profit)
    
    Returns:
    --------
    float : Score (higher is better)
    
    Logic:
    ------
    Uses a "soft maximum" approach - if either metric is good, the score is good.
    This ensures recipes with one strong feature get recommended.
    """
    if cost <= 0:
        raise ValueError("Cost must be positive")
    
    profit_percentage = net_income / cost
    
    # Normalize both metrics to similar scales
    # Net income component: sigmoid that approaches 1 as income increases
    income_score = net_income / (income_threshold + abs(net_income))
    
    # Profit percentage component: sigmoid that approaches 1 as profit % increases
    profit_score = profit_percentage / (profit_threshold + abs(profit_percentage))
    
    # Soft maximum: takes the best of both, with some contribution from the other
    # This ensures if either is high, the total score is high
    alpha = 3.0  # Higher alpha = closer to "hard max", lower = more blending
    score = (income_score * np.exp(alpha * income_score) + 
             profit_score * np.exp(alpha * profit_score)) / \
            (np.exp(alpha * income_score) + np.exp(alpha * profit_score))
    
    # Scale to make scores more interpretable (0-100 range roughly)
    score = score * 100
    
    return score


def trade_up_score_v2(net_income, cost, income_threshold=1000, profit_threshold=3.0):
    """
    Alternative simpler version using actual soft-max
    """
    if cost <= 0:
        raise ValueError("Cost must be positive")
    
    profit_percentage = net_income / cost
    
    # Normalize metrics
    income_normalized = net_income / income_threshold
    profit_normalized = profit_percentage / profit_threshold
    
    # Soft maximum with temperature parameter
    temperature = 0.5  # Lower = closer to hard max, higher = more averaging
    exp_income = np.exp(income_normalized / temperature)
    exp_profit = np.exp(profit_normalized / temperature)
    
    score = (income_normalized * exp_income + profit_normalized * exp_profit) / \
            (exp_income + exp_profit)
    
    # Scale to percentage-like range
    score = score * 100
    
    return score


# Visualization
def plot_trade_up_analysis():
    """Visualize how the scoring works for trade-ups"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # Test case 1: Fixed cost, varying income - show both versions
    cost = 100
    incomes = np.linspace(0, 2000, 500)
    scores_v1 = [trade_up_score(inc, cost) for inc in incomes]
    scores_v2 = [trade_up_score_v2(inc, cost) for inc in incomes]
    profit_pcts = [(inc/cost) * 100 for inc in incomes]
    
    ax = axes[0, 0]
    ax.plot(incomes, scores_v1, 'b-', linewidth=2, label='Score v1')
    ax.plot(incomes, scores_v2, 'g--', linewidth=2, label='Score v2')
    ax.axvline(100, color='gray', linestyle=':', alpha=0.5, label='Low income')
    ax.axvline(1000, color='gray', linestyle=':', alpha=0.5, label='High income')
    ax.set_xlabel('Net Income')
    ax.set_ylabel('Score')
    ax.set_title(f'Score vs Net Income (Cost = {cost})')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Test case 2: Show profit percentage scale
    ax = axes[0, 1]
    ax2 = ax.twinx()
    ax.plot(incomes, scores_v1, 'b-', linewidth=2, label='Score')
    ax2.plot(incomes, profit_pcts, 'r--', alpha=0.6, label='Profit %')
    ax.set_xlabel('Net Income')
    ax.set_ylabel('Score', color='b')
    ax2.set_ylabel('Profit %', color='r')
    ax.set_title('Score vs Profit Percentage')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left')
    ax2.legend(loc='lower right')
    
    # Test case 3: Heatmap - score across income and cost
    costs = np.linspace(50, 500, 100)
    incomes = np.linspace(0, 2000, 100)
    score_matrix = np.zeros((len(incomes), len(costs)))
    
    for i, inc in enumerate(incomes):
        for j, c in enumerate(costs):
            score_matrix[i, j] = trade_up_score(inc, c)
    
    ax = axes[0, 2]
    im = ax.imshow(score_matrix, aspect='auto', origin='lower', 
                   extent=[costs[0], costs[-1], incomes[0], incomes[-1]],
                   cmap='viridis')
    ax.set_xlabel('Cost')
    ax.set_ylabel('Net Income')
    ax.set_title('Score Heatmap')
    plt.colorbar(im, ax=ax, label='Score')
    
    # Test case 4: Compare recipes with different profiles
    recipes = [
        ("High income\nLow profit%", 1500, 500),
        ("Moderate income\nHigh profit%", 300, 50),
        ("Low income\nVery high profit%", 150, 30),
        ("Moderate both", 500, 150),
        ("Low both", 50, 100),
    ]
    
    ax = axes[1, 0]
    labels = [r[0] for r in recipes]
    scores = [trade_up_score(r[1], r[2]) for r in recipes]
    profit_pcts = [(r[1]/r[2]) * 100 for r in recipes]
    
    x_pos = np.arange(len(recipes))
    bars = ax.bar(x_pos, scores, alpha=0.8, color='steelblue')
    ax.set_xlabel('Recipe Type')
    ax.set_ylabel('Score')
    ax.set_title('Scores for Different Recipe Profiles')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for i, (bar, score) in enumerate(zip(bars, scores)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{score:.1f}',
                ha='center', va='bottom', fontsize=9)
    
    # Test case 5: Show how profit % affects score at different income levels
    ax = axes[1, 1]
    fixed_incomes = [50, 200, 500, 1000, 1500]
    costs_range = np.linspace(10, 500, 100)
    
    for inc in fixed_incomes:
        scores = [trade_up_score(inc, c) if c < inc else trade_up_score(inc, c) 
                  for c in costs_range]
        ax.plot(costs_range, scores, linewidth=2, label=f'Income={inc}')
    
    ax.set_xlabel('Cost')
    ax.set_ylabel('Score')
    ax.set_title('Score vs Cost for Different Income Levels')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Test case 6: Profit % threshold comparison
    ax = axes[1, 2]
    profit_multiples = np.linspace(0.5, 10, 100)
    cost_fixed = 100
    
    for inc_mult in [0.5, 1, 2, 5, 10, 20]:
        scores = [trade_up_score(pm * cost_fixed, cost_fixed) for pm in profit_multiples]
        ax.plot(profit_multiples, scores, linewidth=2, 
                label=f'{inc_mult}x profit', alpha=0.7)
    
    ax.axvline(3.0, color='red', linestyle='--', alpha=0.5, label='Profit threshold')
    ax.set_xlabel('Profit Multiple (income/cost)')
    ax.set_ylabel('Score')
    ax.set_title('Score vs Profit Multiple')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('tradeup_score_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()


# Example usage
if __name__ == "__main__":
    print("CS2 Trade-Up Contract Scoring System\n" + "="*60)
    
    print("\nScenario 1: High income, low profit%")
    print(f"  Income=1500, Cost=500 (300% profit)")
    print(f"  Score: {trade_up_score(1500, 500):.2f}")
    
    print("\nScenario 2: Moderate income, high profit%")
    print(f"  Income=300, Cost=50 (600% profit)")
    print(f"  Score: {trade_up_score(300, 50):.2f}")
    
    print("\nScenario 3: Low income, very high profit%")
    print(f"  Income=150, Cost=30 (500% profit)")
    print(f"  Score: {trade_up_score(150, 30):.2f}")
    
    print("\nScenario 4: Moderate both")
    print(f"  Income=500, Cost=150 (333% profit)")
    print(f"  Score: {trade_up_score(500, 150):.2f}")
    
    print("\nScenario 5: Low both")
    print(f"  Income=50, Cost=100 (50% profit)")
    print(f"  Score: {trade_up_score(50, 100):.2f}")
    
    print("\nScenario 6: Very high income, low profit%")
    print(f"  Income=2000, Cost=800 (250% profit)")
    print(f"  Score: {trade_up_score(2000, 800):.2f}")
    
    print("\nScenario 7: Small income, extreme profit%")
    print(f"  Income=100, Cost=10 (1000% profit)")
    print(f"  Score: {trade_up_score(100, 10):.2f}")
    
    # Demonstrate ranking
    print("\n" + "="*60)
    print("RANKING EXAMPLE - Top trade-up opportunities:")
    print("="*60)
    
    trade_ups = [
        ("AWP Safari Mesh → Dragon Lore", 1500, 500),
        ("Five-Seven → Case Hardened", 300, 50),
        ("P250 → Fade", 150, 30),
        ("AK Blue Laminate", 500, 150),
        ("Glock Sand Dune", 50, 100),
        ("M4A4 → Howl", 2500, 1000),
        ("Dual Berettas", 80, 10),
    ]
    
    ranked = sorted(trade_ups, 
                   key=lambda x: trade_up_score(x[1], x[2]), 
                   reverse=True)
    
    for i, (name, income, cost) in enumerate(ranked, 1):
        score = trade_up_score(income, cost)
        profit_pct = (income/cost) * 100
        print(f"{i}. {name:30} | Score: {score:6.2f} | "
              f"Income: ${income:5.0f} | Profit: {profit_pct:6.1f}%")
    
    # Generate visualization
    print("\nGenerating visualization...")
    plot_trade_up_analysis()
    print("Done! Check 'tradeup_score_analysis.png' for detailed analysis.")