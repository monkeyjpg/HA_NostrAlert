import matplotlib.pyplot as plt
import numpy as np

# Set up the figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# MVP Feature Distribution
mvp_labels = ['Core Nostr Integration', 'Home Assistant Integration', 'Error Handling & Reliability', 
              'Security', 'Testing', 'Documentation']
mvp_sizes = [25, 25, 20, 15, 10, 5]
mvp_colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0']

# Create MVP donut chart
wedges1, texts1, autotexts1 = ax1.pie(mvp_sizes, labels=mvp_labels, colors=mvp_colors,
                                      autopct='%1.1f%%', startangle=90, pctdistance=0.85,
                                      wedgeprops=dict(width=0.3))

# Draw circle for donut effect
centre_circle1 = plt.Circle((0,0),0.70,fc='white')
ax1.add_artist(centre_circle1)

ax1.set_title('HA Nostr Alert System - MVP Feature Distribution', fontsize=14, pad=20)

# Future Releases Breakdown
future_labels = ['Release 2 Enhancements', 'Release 3 Advanced Features']
future_sizes = [60, 40]
future_colors = ['#ffcc99', '#66b3ff']

# Create Future Releases donut chart
wedges2, texts2, autotexts2 = ax2.pie(future_sizes, labels=future_labels, colors=future_colors,
                                      autopct='%1.1f%%', startangle=90, pctdistance=0.85,
                                      wedgeprops=dict(width=0.3))

# Draw circle for donut effect
centre_circle2 = plt.Circle((0,0),0.70,fc='white')
ax2.add_artist(centre_circle2)

ax2.set_title('HA Nostr Alert System - Future Releases Breakdown', fontsize=14, pad=20)

# Adjust layout and save
plt.tight_layout()
plt.savefig('/tmp/ha_nostr_alert_charts.png', dpi=300, bbox_inches='tight')
print("Charts saved as /tmp/ha_nostr_alert_charts.png")
