from typing import List

#冒泡排序
def bubble_sort(nums:List[int],):
    for i in range(len(nums)):
        is_sorted = True
        for j in range(len(nums) - i - 1):
            if nums[j] > nums[j + 1]:
                is_sorted = False
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
        if is_sorted:
            break
    return nums

#选择排序
def selection_sort(nums:List[int]):
    for i in range(len(nums)):
        min_index = i
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[min_index]:
                min_index = j
        nums[i], nums[min_index] = nums[min_index], nums[i]
    return nums

#插入排序
def insertion_sort(nums:List[int]):
    for i in range(1, len(nums)):
        for j in range(i, 0, -1):
            if nums[j] < nums[j - 1]:
                nums[j], nums[j - 1] = nums[j - 1], nums[j]
            else:
                break
    return nums

#希尔排序
def shell_sort(nums:List[int]):
    gap = len(nums) // 2
    while gap > 0:
        for i in range(gap, len(nums)):
            for j in range(i, 0, -gap):
                if nums[j] < nums[j - gap]:
                    nums[j], nums[j - gap] = nums[j - gap], nums[j]
                else:
                    break
        gap //= 2
    return nums

#归并排序
def merge_sort(nums:List[int]):
    if len(nums) <= 1:
        return nums
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])
    return merge_sort(left, right)

# 快速排序
def quick_sort(nums:List[int]):
    if len(nums) <= 1:
        return nums
    pivot = nums[0]
    left = [i for i in nums[1:] if i <= pivot]
    right = [i for i in nums[1:] if i > pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)
