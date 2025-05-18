import pandas as pd

# Read the file in binary mode
with open('dataset/Places.csv', 'rb') as f:
    content = f.read()

# Decode the content with a fallback encoding
try:
    content = content.decode('windows-1254')
except UnicodeDecodeError:
    content = content.decode('latin1')  # Fallback to a different encoding if needed

# Save the decoded content to a new file
with open('Places_decoded.csv', 'w', encoding='utf-8') as f:
    f.write(content)

# Now read the CSV with utf-8 encoding
df = pd.read_csv('Places_decoded.csv')
