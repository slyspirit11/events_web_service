

# определяет на сколько подмножеств можно разделить множество так, что суммы полученных подмножеств бедут равны
def can_partition(nums, k):
    def has_ith_bit(x, i):
        return x & (1 << i)

    def set_ith_bit(x, i):
        return x | (1 << i)

    subset_tgt, remainder = divmod(sum(nums), k)
    if remainder != 0:
        return False

    num_subsets = 1 << len(nums)
    DP = [False for _ in range(num_subsets)]
    DP[0] = True

    subset_sums = [None for _ in range(num_subsets)]
    subset_sums[0] = 0

    for x in range(num_subsets):
        if DP[x]:
            for i, num in enumerate(nums):
                if not has_ith_bit(x, i):
                    x_with_num = set_ith_bit(x, i)
                    subset_sums[x_with_num] = subset_sums[x] + num
                    DP[x_with_num] = (
                            (subset_sums[x] % subset_tgt) + num <= subset_tgt
                    )

    return DP[-1]