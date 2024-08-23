import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt

# Skapa en figur och en axel
fig, ax = plt.subplots()

# Rita en röd rektangel som bakgrund
ax.add_patch(plt.Rectangle((0, 0), 1, 1, color='red'))

# Lägg till texten "HMH" i vit text
ax.text(0.5, 0.6, 'HMH', fontsize=60, color='white',
        ha='center', va='center', fontweight='bold')

# Lägg till beskrivande text
ax.text(0.5, 0.3, 'Henrys Molok Hanterare', fontsize=18, color='white',
        ha='center', va='center', fontweight='normal')

ax.text(0.5, 0.15, 'Revolutionerande teknik för Remondis kunder', fontsize=12, color='white',
        ha='center', va='center', fontweight='normal')

# Lägg till "Patent Pending" som ett skämt
ax.text(0.5, 0.05, 'Patent Pending', fontsize=10, color='white',
        ha='center', va='center', fontstyle='italic')

# Ta bort axlarna
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# Spara logotypen som en bildfil
plt.savefig('hmh_logo.png', dpi=300, bbox_inches='tight', pad_inches=0.1)

# Visa logotypen
plt.show()
