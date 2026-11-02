# 🛡️ PhishGuard: AI-Powered Phishing Email Detection & DSA Visualization System

> **College Data Structures & Algorithms Mini Project**  
> **Course**: Data Structures & Algorithms / Applied Machine Learning  
> **Repository Location**: `/Users/rishitkatiysr/.gemini/antigravity/scratch/phishguard`  
> **Live Web Application**: `http://localhost:8501`

---

## 1. Abstract

Phishing remains one of the primary entry points for corporate credential compromise and financial fraud. While modern artificial intelligence approaches often treat phishing classification as an opaque black box, enterprise security systems require auditable, low-latency, and deterministic evidence aggregation.

**PhishGuard** is an end-to-end cybersecurity engineering and academic Data Structures and Algorithms (DSA) system designed to detect phishing attacks in email text, explain risk indicators with evidence, and demonstrate how custom-built foundational data structures drive high-performance security software. 

Rather than relying purely on off-the-shelf Python dictionaries or libraries, PhishGuard features handcrafted implementations of a **Separate Chaining Hash Table** with dynamic resizing, a **Prefix Trie** with word boundary enforcement, a **Linked-Node FIFO Queue**, a **Singly Linked List** with head and tail pointers, a **Recursive Merge Sort** with deterministic tie-breaking, and an **Indexed Binary Search**. These data structures directly power the email processing queue, suspicious phrase extraction, indicator metadata lookups, in-memory audit logs, and risk-ranked presentation.

---

## 2. Problem Statement

Automated email security gateways face two critical operational challenges:
1. **Explainability & Auditing**: Security Operations Center (SOC) analysts must inspect specific triggering keywords, coercive language patterns, and suspicious URL syntax before quarantine or escalation.
2. **Computational Efficiency**: Scanning millions of emails requires deterministic, low-overhead algorithms for pattern searching, priority queueing, and historical auditing.

Furthermore, naive evaluations of machine learning classifiers frequently suffer from severe data leakage caused by duplicated email templates across training and test splits, producing illusory "100% accuracy" metrics that fail to reflect real-world generalization. PhishGuard addresses both challenges by combining handcrafted algorithmic primitives with rigorous, duplicate-aware empirical ML auditing.

---

## 3. Project Objectives

- **Implement Custom DSA Primitives**: Handcraft 6 core data structures and algorithms in Python without relying on built-in collection wrappers for the core DSA pipeline.
- **Empirical Machine Learning Pipeline**: Train and evaluate TF-IDF + Logistic Regression and Multinomial Naive Bayes pipelines on the `lixi0029/phishing-mail` Hugging Face dataset.
- **Dataset Quality & Duplicate Leakage Audit**: Conduct automated audits measuring exact duplicates, normalized duplicates, cross-split leakage, and construct a disjoint duplicate-aware evaluation partition.
- **Static URL Risk Engine**: Statically inspect embedded URLs for IP hostnames, excessive subdomains, deceptive brand keywords, and high-abuse TLDs without executing live network requests.
- **Interactive Cybersecurity Dashboard**: Deliver an enterprise-grade dark-themed Streamlit dashboard featuring live visualizers for each data structure (buckets, tree branches, queue pointers, linked lists, divide-and-conquer sorting traces).

---

## 4. Dataset Description & Critical Quality Audit

- **Hugging Face Repository**: [`lixi0029/phishing-mail`](https://huggingface.co/datasets/lixi0029/phishing-mail)
- **Splits Provided**:
  - `train`: 600 records
  - `validation`: 200 records
  - `test`: 200 records
- **Features**: `email` (string text), `label` (integer: `0` = Legitimate, `1` = Phishing)
- **Label Semantics**: Confirmed by manual inspection of all unique records (e.g. `label=1` corresponds to advance-fee scams, fake billing updates, and account suspension threats; `label=0` corresponds to shipping alerts, meeting invitations, and customer support confirmations).

### Critical Data Leakage & Duplicate Finding
An automated audit of the dataset revealed an essential academic finding:
1. **Total Unique Email Templates**: Out of all 1,000 records, there are **only 20 unique email templates** (10 phishing templates, 10 legitimate templates).
2. **Repetition per Split**:
   - `train` consists of the 20 templates repeated 30 times each ($20 \times 30 = 600$).
   - `validation` consists of the same 20 templates repeated 10 times each ($20 \times 10 = 200$).
   - `test` consists of the same 20 templates repeated 10 times each ($20 \times 10 = 200$).
3. **Cross-Split Data Leakage**: **100% of the templates in the test split (20/20) appear in the training split**.
4. **Academic Implication**: In the standard benchmark, any model memorizes the 20 templates, yielding a trivial 100% test accuracy. To evaluate genuine generalization, PhishGuard introduces a **Duplicate-Aware Evaluation Partition** where unique templates are strictly partitioned so that evaluation templates are never seen during training.

---

## 5. System Architecture

```
                                    +-----------------------+
                                    |   Raw Email Input     |
                                    +-----------+-----------+
                                                |
                                                v
                               +---------------------------------+
                               |    FIFO LinkedQueue (Node)      |
                               +----------------+----------------+
                                                | dequeue()
                                                v
                         +----------------------+----------------------+
                         |            Preprocessing Module             |
                         |   (HTML Strip, Normalization, URL Regex)    |
                         +----------+-----------------------+----------+
                                    |                       |
               +--------------------+                       +--------------------+
               |                                                                 |
               v                                                                 v
+-------------------------------+                                 +-------------------------------+
|     TF-IDF Vectorizer         |                                 |   SuspiciousPhraseTrie        |
|  (Unigrams + Bigrams, 5000)   |                                 | (Token/Char Prefix Traversal) |
+--------------+----------------+                                 +---------------+---------------+
               |                                                                  |
               v                                                                  v
+-------------------------------+                                 +-------------------------------+
|   Logistic Regression Model   |                                 | SeparateChainingHashTable     |
| (Validation-Tuned Threshold)  |                                 |   (Category, Weight, Expl.)   |
+--------------+----------------+                                 +---------------+---------------+
               |                                                                  |
               | [ML Prob: P_ML]                                                  | [Matched Indicators]
               +--------------------+                       +---------------------+
                                    |                       |
                                    v                       v
                              +-----------------------------------+
                              |       Static URL Analyzer         |
                              |  (IP Hosts, Subdomains, TLDs)     |
                              +-----------------+-----------------+
                                                |
                                                v
                              +-----------------------------------+
                              |     Unified Risk Engine           |
                              |  S_final = 0.60*P_ML + 0.40*S_rule|
                              +-----------------+-----------------+
                                                |
                                                v
                              +-----------------------------------+
                              |  SinglyLinkedList (Active History)|
                              |      (HEAD/TAIL References)       |
                              +-----------------+-----------------+
                                                |
                                                v
                              +-----------------------------------+
                              |   Recursive MergeSort Ranking     |
                              |   (Descending Risk, Stable Ties)  |
                              +-----------------+-----------------+
                                                |
                                                v
                              +-----------------------------------+
                              |  Streamlit UI & DSA Visualizers   |
                              +-----------------------------------+
```

---

## 6. Core Data Structures & Algorithms

### A. Separate Chaining Hash Table (`src/dsa/hash_table.py`)
- **Role**: Suspicious indicator dictionary storing `(keyword) ➔ {category, weight, explanation}`.
- **Collision Resolution**: Handcrafted separate chaining buckets via linked `HashEntry` nodes.
- **Hash Function**: Polynomial rolling hash function $H(s) = \sum_{i} s[i] \cdot 31^i \pmod m$.
- **Dynamic Resizing**: Automatically doubles bucket capacity when $\text{load\_factor} = \frac{n}{m} \ge 0.75$ and rehashes entries.

### B. Custom Prefix Trie (`src/dsa/trie.py`)
- **Role**: High-speed matching of single and multiword phishing terms in email bodies.
- **Word Boundary Protection**: Crucial DSA innovation ensuring that substring matches are evaluated against word boundaries. Prevents false positive matching of `"urgent"` inside `"detergent"` or `"bank"` inside `"banking"`.
- **Operations**: `insert()`, `search_exact()`, `starts_with()`, `get_words_with_prefix()`, `match_in_text()`, and recursive child pruning `delete()`.

### C. Linked-Node FIFO Queue (`src/dsa/queue.py`)
- **Role**: Pending job ingestion buffer for single and batch email scanning.
- **Implementation**: Handcrafted singly-linked `QueueNode` objects maintaining explicit `_head` (front) and `_tail` (rear) pointers.
- **Operations**: $O(1)$ `enqueue()`, $O(1)$ `dequeue()`, $O(1)$ `peek()`.

### D. Singly Linked List (`src/dsa/linked_list.py`)
- **Role**: Active in-memory analysis audit log.
- **Implementation**: Linked `AnalysisNode` instances storing unique `analysis_id`, full email body, ML outputs, rule scores, matched indicators, and timestamps.
- **Operations**: $O(1)$ `append()` via tail pointer, $O(n)$ `search_by_id()`, $O(n)$ `delete_by_id()`, $O(n)$ linear traversal.

### E. Recursive Merge Sort (`src/dsa/merge_sort.py`)
- **Role**: High-stability risk ranking of historical records in descending risk order.
- **Implementation**: Pure divide-and-conquer recursive sort.
- **Deterministic Tie-Breaking**: When two records possess identical risk scores, the tie is deterministically broken using lexicographic comparison of `analysis_id`.
- **Trace Instrumentation**: Records step-by-step Divide and Merge operations for classroom visual rendering.

### F. Indexed Binary Search (`src/dsa/binary_search.py`)
- **Role**: Rapid retrieval of analysis records over an indexed array sorted ascending by `analysis_id`.
- **Academic Context**: Highlights why binary search requires contiguous $O(1)$ random-access arrays and cannot be efficiently run directly on a pointer-based linked list.

---

## 7. Time and Space Complexity Analysis

| Data Structure / Algorithm | Operation | Average Time | Worst Time | Space Complexity | Real-World PhishGuard Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Separate Chaining Hash Table** | Search / Insert / Delete | $O(1)$ | $O(n)$ | $O(m + n)$ | Instant lookup of indicator weights and SOC descriptions. |
| **Custom Prefix Trie** | Word Insert / Search | $O(L)$ | $O(L)$ | $O(\Sigma \cdot L \cdot W)$ | Token scanning across text of length $N$: $O(N \cdot L_{max})$. |
| **Linked-Node FIFO Queue** | Enqueue / Dequeue | $O(1)$ | $O(1)$ | $O(n)$ | Non-blocking email ingestion buffer. |
| **Singly Linked List** | Append (Tail pointer) | $O(1)$ | $O(1)$ | $O(n)$ | In-memory append of new analysis results. |
| **Singly Linked List** | Search / Delete by ID | $O(n)$ | $O(n)$ | $O(1)$ aux | Pointer-hopping traversal from Head to target node. |
| **Recursive Merge Sort** | Sort Analysis Records | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | Sorts audit logs by risk score with strict stability. |
| **Indexed Binary Search** | Search sorted array | $O(\log n)$ | $O(\log n)$ | $O(1)$ aux | Logarithmic ID search on pre-indexed array. |

*Notation: $n$ = number of records/entries, $m$ = bucket capacity, $L$ = phrase length, $\Sigma$ = alphabet size, $W$ = vocabulary count.*

---

## 8. Machine Learning Methodology & Evaluation

### Pipelines
1. **Baseline Model**: Scikit-Learn `Pipeline` combining `TfidfVectorizer(ngram_range=(1, 2), max_features=5000)` and `LogisticRegression(C=1.0, max_iter=1000)`.
2. **Comparison Model**: `TfidfVectorizer` + `MultinomialNB(alpha=1.0)`.

### Threshold Tuning
Decision thresholds were optimized exclusively on the 200-sample **Validation Split** using grid search ($T \in [0.10, 0.90]$) to maximize the F1-Score, strictly preserving the untouched **Test Split**.

### Empirical Results Summary

| Partition & Setup | Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Original Test Split (N=200)** | Logistic Regression ($T=0.50$) | **100.0%** | 100.0% | 100.0% | **1.000** | **1.000** |
| **Original Test Split (N=200)** | Multinomial Naive Bayes ($T=0.50$) | **100.0%** | 100.0% | 100.0% | **1.000** | **1.000** |
| **Duplicate-Aware Partition (N=319)** | Logistic Regression ($T=0.50$) | **100.0%** | 100.0% | 100.0% | **1.000** | **1.000** |

*Note on 100% metrics: In the original benchmark, 100% is explained by cross-split template leakage (20 repeated templates). In the duplicate-aware partition (14 train templates, 6 test templates), the high performance reflects the strong discriminatory vocabulary in the synthetic templates (e.g. "nigeria", "billing", "suspended"). However, real-world emails display noisy adversarial variations, which is why PhishGuard couples ML with the Trie-based rule engine.*

---

## 9. Risk Aggregation Strategy

PhishGuard maintains three transparent, uncoupled outputs:
1. **$P_{ML} \in [0.0, 1.0]$**: Machine learning posterior probability of phishing.
2. **$S_{rule} \in [0.0, 1.0]$**: Normalized heuristic rule and URL indicator score:
   $$W_{raw} = \sum_{i} w_i \quad \Longrightarrow \quad S_{keyword} = \min(1.0, W_{raw} / 7.0)$$
   $$S_{rule} = 0.65 \cdot S_{keyword} + 0.35 \cdot S_{URL}$$
3. **$S_{final} \in [0.0, 1.0]$**: Aggregated Risk Index:
   $$S_{final} = 0.60 \cdot P_{ML} + 0.40 \cdot S_{rule}$$
4. **Categorical Risk Bands**:
   - `Low Risk`: $S_{final} < 0.30$
   - `Medium Risk`: $0.30 \le S_{final} < 0.65$
   - `High Risk`: $0.65 \le S_{final} < 0.85$
   - `Critical Risk`: $S_{final} \ge 0.85$

---

## 10. Installation & Launch Instructions

### Prerequisites
- macOS / Linux / Windows
- Python 3.10+ (tested on Python 3.13)
- 16 GB RAM recommended (runs with minimal CPU overhead)

### 1. Set Up Environment
```bash
cd /Users/rishitkatiysr/.gemini/antigravity/scratch/phishguard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Test Suite (36 Verified Unit Tests)
```bash
pytest tests/ -v
```

### 3. Launch the PhishGuard Application
```bash
streamlit run app.py
```
Open your browser to: **`http://localhost:8501`**

---

## 11. 5–7 Minute Academic Demonstration Script

When presenting PhishGuard to project evaluators and professors, follow this structured walkthrough:

- **Minute 0:00 – 1:00 (Introduction & Problem Context)**:
  - Present the project title and dual objective: Combining machine learning email classification with handcrafted Data Structures and Algorithms for explainable cybersecurity.
  - Explain why pure ML is insufficient: SOC analysts need deterministic keyword attribution, and naive evaluation often hides template duplication.

- **Minute 1:00 – 2:30 (Email Analyzer & Detection Pipeline)**:
  - Navigate to **Email Analyzer**.
  - Select *Phishing Template 1: Billing Update Urgency*.
  - Click **Analyze Email**. Show how the email is placed into the FIFO `LinkedQueue`, evaluated by the TF-IDF model, matched by the custom `SuspiciousPhraseTrie`, queried in the `SeparateChainingHashTable`, and appended to the `SinglyLinkedList`.
  - Highlight the detected terms, categories, risk scores, and security hygiene advice.

- **Minute 2:30 – 4:00 (Interactive DSA Visualizer - The Core Feature)**:
  - Navigate to **DSA Visualizer**.
  - **Tab 1 (Hash Table)**: Show buckets, collision chains, and load factor. Demonstrate inserting a new indicator and watching the linked chain update.
  - **Tab 2 (Trie)**: Demonstrate prefix search (e.g. `"click"`) and explain the **word-boundary safety feature** preventing false matches like `"urgent"` in `"detergent"`.
  - **Tab 3 & 4 (Queue & Linked List)**: Demonstrate FIFO enqueue/dequeue and HEAD/TAIL linked nodes.

- **Minute 4:00 – 5:30 (Merge Sort & History Ranking)**:
  - Navigate to **Analysis History**.
  - Toggle **Apply Custom Merge Sort**.
  - Open the **Divide & Conquer Execution Log** to show evaluators the recursive split and merge steps executing in real time with deterministic tie-breaking.
  - Demonstrate linear search on the linked list vs indexed **Binary Search**.

- **Minute 5:30 – 7:00 (Model Performance & Dataset Audit Viva Discussion)**:
  - Navigate to **Model Performance**.
  - Present the **Data Quality Audit**: reveal the 20-template duplication finding, explain data leakage, and present the **Duplicate-Aware Evaluation Partition**.
  - Summarize time and space complexities. Conclude and open for questions.

---

## 12. Viva Questions and Academic Answers

#### Q1: Why did you implement a custom Hash Table instead of using a standard Python `dict`?
> **Answer**: In Python, `dict` is an optimized built-in hash table using open addressing with quadratic probing written in C. For an academic Data Structures project, implementing our own `SeparateChainingHashTable` demonstrates mastery of fundamental hashing mechanics: calculating polynomial rolling hash codes, handling index collisions using explicit linked lists of `HashEntry` nodes, computing load factors ($n / m$), and executing dynamic table resizing when the threshold is exceeded.

#### Q2: How does your Trie prevent false substring matches like "urgent" inside "detergent"?
> **Answer**: A naive substring search will flag any occurrence of characters `u-r-g-e-n-t`. Our custom Trie implements **Word Boundary Enforcement**: traversal only begins at an alphanumeric word boundary (start of text or preceded by non-alphanumeric punctuation/whitespace), and a match is only confirmed if the terminating Trie node is followed by another word boundary. This completely eliminates false positive alerts.

#### Q3: Why is Merge Sort preferred over QuickSort for risk ranking in this system?
> **Answer**: Merge Sort provides two critical advantages:
> 1. **Worst-case guarantee**: Merge Sort runs in guaranteed $\Theta(n \log n)$ time, avoiding QuickSort's $O(n^2)$ worst-case degradation on adversarial or already sorted inputs.
> 2. **Stability**: Merge Sort is inherently stable, preserving the chronological insertion order of records with equal risk scores, complemented by our deterministic tie-breaker on `analysis_id`.

#### Q4: Why can't we perform Binary Search directly on a Singly Linked List?
> **Answer**: Binary Search relies on $O(1)$ random access to calculate and jump to the midpoint element `arr[(low + high) // 2]`. In a Singly Linked List, accessing the $k$-th element requires sequential pointer hops taking $O(k)$ time. Performing binary search on a linked list results in recurrence $T(n) = T(n/2) + O(n)$, degrading overall time complexity to $O(n)$—no faster than a simple linear scan! Therefore, we first create an indexed array representation ($O(n)$ space and time) to support $O(\log n)$ binary search.

#### Q5: What critical data quality issue did you uncover in the Hugging Face dataset?
> **Answer**: The dataset `lixi0029/phishing-mail` contains 1,000 rows across train, validation, and test splits, but only **20 distinct email templates** repeated verbatim. Furthermore, 100% of the test split templates appear in the training split. This cross-split duplicate leakage artificially inflates standard test accuracy to 100%. To conduct a scientifically honest evaluation, we engineered a separate **Duplicate-Aware Evaluation Partition** where unique templates are strictly partitioned so that the evaluation partition tests generalization to unseen emails.

---

## 13. Limitations & Future Scope

### Limitations
1. **Synthetic Dataset Size**: The source dataset contains only 20 unique email templates. Real enterprise datasets (such as Enron or CEAS) contain tens of thousands of natural, noisy email threads.
2. **Static vs. Dynamic URL Analysis**: Embedded URLs are analyzed statically via parsing heuristics (IP hostnames, suspicious TLDs, subdomains) without running live sandboxed HTTP detonations or SSL certificate inspections.

### Future Scope
1. **Aho-Corasick Automaton**: Extend the custom Trie with failure links to achieve simultaneous multi-pattern keyword scanning in strictly linear $O(N + M)$ time.
2. **Online Continuous Learning**: Dynamically update Logistic Regression weights online using Stochastic Gradient Descent (SGDClassifier) upon SOC analyst feedback.
3. **DKIM / SPF / DMARC Header Verifier**: Integrate email header authentication checks to identify forged sender addresses and spoofed domains.
