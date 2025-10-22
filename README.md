### **Final Project for Data Structures and Algorithms**

### **Terminal-Based Bible App**

A simple terminal-based Bible application that allows users to:

- Search verses using the Boyer Moore algorithm
- Bookmark favorite passages
- Display a random "Verse of the Day"
- Maintain a search history using a queue
- Navigate a hierarchical Bible structure (Book → Chapter → Verse)

<hr>

### **Features**

| Feature | Algorithm / Data Structure |
|----------|----------------------------|
| Search | Boyer–Moore Algorithm |
| Structure | Tree (Book → Chapter → Verse) |
| Bookmark | Hash Table |
| Verse of the Day | Array/List + Random |
| Search History | Queue (Deque) |

<hr>

### **How to Run**

1. Clone the repository:
   ```bash
   git clone https://github.com/Denmark-DC-Bartolome/Group5-DSA_FinalProject.git
   ```
2. open the folder:
    cd bible-app-terminal/src
3. Run the main program:
    python main.py

<hr>

### **Generate Bible Text File**
If you want to recreate the plain text version of the Bible:
1. Download `en_kjv.json` from [thiagobodruk/bible](https://github.com/thiagobodruk/bible).
2. Place it in the `/data` folder.
3. Run:
   ```bash
   python src/json_to_txt.py
   ```