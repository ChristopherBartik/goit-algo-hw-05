def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (low + high) // 2

        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return (iterations, arr[mid])

    # If we exit the loop, we haven't found the exact value
    if low < len(arr):
        upper_bound = arr[low]
    else:
        upper_bound = None  # No element greater than or equal to x

    return (iterations, upper_bound)

# Example usage:
sorted_arr = [1.1, 2.2, 3.3, 4.4, 5.5]
value_to_find = 3.7

result = binary_search(sorted_arr, value_to_find)
print(f"Number of iterations: {result[0]}, Upper bound: {result[1]}")
