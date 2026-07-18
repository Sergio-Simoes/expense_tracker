from typing import List
class Solution:
    def removeDuplicates(self, nums: List[int]):
        if nums is None:
            return 0
        new_list=[]
        [new_list.append(i) for i in nums if i not in new_list]

        return new_list



if __name__ == "__main__":
    sol = Solution()
    print(sol.removeDuplicates([1,1,2]))
    print(sol.removeDuplicates([1,1,2,2,2,3]))
    print(sol.removeDuplicates([1,2,3,4,4]))




                