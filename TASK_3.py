import timeit
import pandas as pd

# Boyer-Moore Algorithm
def boyer_moore(text, pattern):
    m = len(pattern)
    n = len(text)
    if m > n:
        return -1

    skip = [m] * 256
    for k in range(m - 1):
        skip[ord(pattern[k])] = m - k - 1

    k = m - 1
    while k < n:
        j = m - 1
        i = k
        while j >= 0 and text[i] == pattern[j]:
            j -= 1
            i -= 1
        if j == -1:
            return i + 1
        k += skip[ord(text[k])]
    return -1

# Knuth-Morris-Pratt Algorithm
def kmp_search(text, pattern):
    m = len(pattern)
    n = len(text)
    lps = [0] * m
    j = 0  # index for pattern[]

    compute_lps_array(pattern, m, lps)

    i = 0  # index for text[]
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            return i - j
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

def compute_lps_array(pattern, m, lps):
    length = 0  # length of the previous longest prefix suffix
    lps[0] = 0  # lps[0] is always 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

# Rabin-Karp Algorithm
def rabin_karp(text, pattern, d=256, q=101):
    m = len(pattern)
    n = len(text)
    p = 0  # hash value for pattern
    t = 0  # hash value for text
    h = 1

    if m > n:
        return -1

    for i in range(m-1):
        h = (h * d) % q

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            if text[i:i+m] == pattern:
                return i
        if i < n - m:
            t = (d*(t - ord(text[i])*h) + ord(text[i + m])) % q
            if t < 0:
                t = t + q
    return -1

# Sample text from articles
article1 = """Comparative Analysis between Selection Sort and Merge Sort Algorithms...
[Content truncated for brevity]
"""

article2 = """Surface Optimal Path Planning Using an Extended Dijkstra Algorithm...
[Content truncated for brevity]
"""

# Substrings
existing_substring = "algorithm"  # likely to exist in both articles
non_existing_substring = "nonexistentpattern123"  # unlikely to exist in both articles

# Function to measure execution time
def measure_time(text, pattern, algorithm):
    timer = timeit.Timer(lambda: algorithm(text, pattern))
    return timer.timeit(number=1000)

# Measuring times for article 1
bm_time_exist_article1 = measure_time(article1, existing_substring, boyer_moore)
bm_time_non_exist_article1 = measure_time(article1, non_existing_substring, boyer_moore)

kmp_time_exist_article1 = measure_time(article1, existing_substring, kmp_search)
kmp_time_non_exist_article1 = measure_time(article1, non_existing_substring, kmp_search)

rk_time_exist_article1 = measure_time(article1, existing_substring, rabin_karp)
rk_time_non_exist_article1 = measure_time(article1, non_existing_substring, rabin_karp)

# Measuring times for article 2
bm_time_exist_article2 = measure_time(article2, existing_substring, boyer_moore)
bm_time_non_exist_article2 = measure_time(article2, non_existing_substring, boyer_moore)

kmp_time_exist_article2 = measure_time(article2, existing_substring, kmp_search)
kmp_time_non_exist_article2 = measure_time(article2, non_existing_substring, kmp_search)

rk_time_exist_article2 = measure_time(article2, existing_substring, rabin_karp)
rk_time_non_exist_article2 = measure_time(article2, non_existing_substring, rabin_karp)

# Analyzing Results
results = {
    "Article 1": {
        "Boyer-Moore": {
            "Existing Substring": bm_time_exist_article1,
            "Non-Existing Substring": bm_time_non_exist_article1
        },
        "Knuth-Morris-Pratt": {
            "Existing Substring": kmp_time_exist_article1,
            "Non-Existing Substring": kmp_time_non_exist_article1
        },
        "Rabin-Karp": {
            "Existing Substring": rk_time_exist_article1,
            "Non-Existing Substring": rk_time_non_exist_article1
        }
    },
    "Article 2": {
        "Boyer-Moore": {
            "Existing Substring": bm_time_exist_article2,
            "Non-Existing Substring": bm_time_non_exist_article2
        },
        "Knuth-Morris-Pratt": {
            "Existing Substring": kmp_time_exist_article2,
            "Non-Existing Substring": kmp_time_non_exist_article2
        },
        "Rabin-Karp": {
            "Existing Substring": rk_time_exist_article2,
            "Non-Existing Substring": rk_time_non_exist_article2
        }
    }
}


# Convert results to DataFrame for better readability
df_results = pd.DataFrame(results).T
df_results = df_results.stack().apply(pd.Series).unstack(0)

# Display results
print("Execution Time Results (in seconds):")
print(df_results)